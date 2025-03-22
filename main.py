import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import praw
from textblob import TextBlob
import re
from collections import Counter
import time
import random

# Set page config
st.set_page_config(
    page_title="EventPulse & Recommendation System",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants for Event Recommendation System
WEIGHTS = {"location": 0.5, "prefs": 0.3, "collab": 0.2}

# Reddit API credentials for Sentiment Analysis
REDDIT_CLIENT_ID = "a52bxahMT7Lx4UywI60_Pw"
REDDIT_CLIENT_SECRET = "RYHRBMj__yE1hS_6SGTPx3yxwyUUug"
REDDIT_USER_AGENT = "Eventscrape"

# Load data for Event Recommendation System
@st.cache_data
def load_data():
    try:
        users = pd.read_csv("data/users.csv")
        events = pd.read_csv("data/events.csv")
        bookings = pd.read_csv("data/bookings.csv")
        organizers = pd.read_csv("data/organizers.csv")
        return users, events, bookings, organizers
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

# Preprocessing for Event Recommendation System
@st.cache_data
def preprocess_data(users_df, events_df, bookings_df):
    users_df["preferences"] = users_df["preferences"].apply(eval)
    users_df["social_connections"] = users_df["social_connections"].apply(eval)
    users_df["attended_events"] = users_df["attended_events"].apply(eval)
    
    users_df["city"] = users_df["location"].apply(lambda x: x.split(",")[0].strip())
    events_df["city"] = events_df["location"].apply(lambda x: x.split(",")[0].strip())
    
    events_df["date"] = pd.to_datetime(events_df["date"])
    
    user_interests = bookings_df[bookings_df["interested"] == 1].groupby("user_id")["event_id"].apply(set).to_dict()
    user_history = bookings_df.groupby("user_id")["event_id"].apply(set).to_dict()
    event_users = bookings_df.groupby("event_id")["user_id"].apply(set).to_dict()
    event_categories = events_df.set_index("event_id")["category"].to_dict()
    
    return users_df, events_df, user_interests, user_history, event_users, event_categories

# Collaborative filtering for Event Recommendation System
def collab_filtering(user_id, users_df, user_history, event_users, user_interests, event_categories):
    user = users_df[users_df["user_id"] == user_id].iloc[0]
    attended = user_history.get(user_id, set())
    friends = user["social_connections"]
    
    collab_events = set()
    for event in attended:
        collab_events.update(event_users.get(event, set()))
    for friend in friends:
        collab_events.update(user_interests.get(friend, set()))
    
    interested_categories = {event_categories.get(e) for e in user_interests.get(user_id, set()) if e in event_categories}
    return interested_categories

# Event recommendation (personalized)
def recommend_events(user_id, users_df, events_df, user_history, event_categories, user_interests, event_users):
    try:
        user = users_df[users_df["user_id"] == user_id].iloc[0]
    except IndexError:
        st.error(f"User ID {user_id} not found")
        return [], None
    
    user_city, user_prefs = user["city"], user["preferences"]
    attended = user_history.get(user_id, set())
    collab_categories = collab_filtering(user_id, users_df, user_history, event_users, user_interests, event_categories)
    
    future_events = events_df[events_df["date"] > pd.Timestamp(datetime.now())]
    
    loc_scores = np.where(future_events["city"] == user_city, 1.0, 0.0)
    pref_scores = future_events["category"].isin(user_prefs).astype(float)
    collab_scores = future_events["category"].isin(collab_categories).astype(float)
    
    scores = (WEIGHTS["location"] * loc_scores + 
              WEIGHTS["prefs"] * pref_scores + 
              WEIGHTS["collab"] * collab_scores)
    
    mask = ~future_events["event_id"].isin(attended)
    
    future_events_with_scores = future_events[mask].copy()
    future_events_with_scores["score"] = scores[mask]
    future_events_with_scores["location_score"] = loc_scores[mask] * WEIGHTS["location"]
    future_events_with_scores["preference_score"] = pref_scores[mask] * WEIGHTS["prefs"]
    future_events_with_scores["collaborative_score"] = collab_scores[mask] * WEIGHTS["collab"]
    
    top_indices = scores[mask].argsort()[-5:][::-1]
    recommended_events = future_events[mask].iloc[top_indices][["event_id", "name", "type", "category", "location", "date", "time", "popularity_score"]]
    
    return recommended_events, future_events_with_scores

# General events (non-personalized)
def get_general_events(events_df):
    future_events = events_df[events_df["date"] > pd.Timestamp(datetime.now())]
    general_events = future_events.sort_values(by="popularity_score", ascending=False).head(10)
    return general_events[["event_id", "name", "type", "category", "location", "date", "time", "popularity_score"]]

# Evaluate recommendations
def evaluate_recommendations(user_id, recommendations, user_interests, event_categories, events_df):
    interested_categories = {event_categories.get(e) for e in user_interests.get(user_id, set()) if e in event_categories}
    future_events = events_df[events_df["date"] > pd.Timestamp(datetime.now())]
    actual = set(future_events[future_events["category"].isin(interested_categories)]["event_id"])
    
    predicted = {event["event_id"] for _, event in recommendations.iterrows()}
    if not actual or not predicted:
        return 0, 0, 0
    
    y_true = [1 if e in actual else 0 for e in predicted]
    y_pred = [1] * len(predicted)
    
    return (precision_score(y_true, y_pred, zero_division=0),
            recall_score(y_true, y_pred, zero_division=0),
            f1_score(y_true, y_pred, zero_division=0))

# Organizer insights
def organizer_insights(events_df, bookings_df, organizers_df):
    event_stats = bookings_df.groupby("event_id").agg({
        "total_price": "sum",
        "ticket_quantity": "sum",
        "rating": "mean"
    }).reset_index()
    
    insights = pd.merge(events_df[["event_id", "name", "popularity_score", "city"]], event_stats, on="event_id")
    insights = pd.merge(insights, organizers_df[["event_id", "pricing_strategy"]], on="event_id")
    
    return insights.rename(columns={"name": "event_name"})

# Sentiment Analysis Functions
def extract_event_info(title, text, location):
    combined_text = f"{title} {text}".lower()
    location_lower = location.lower()
    
    event_indicators = ["event", "festival", "concert", "show", "performance", "exhibition", 
                        "convention", "meetup", "gathering", "party", "celebration"]
    
    is_event = False
    for indicator in event_indicators:
        if indicator in combined_text:
            is_event = True
            break
    
    if location_lower not in combined_text and not is_event:
        return {"is_event": False}
    
    event_name = None
    name_match = re.search(r'"([^"]+)"', title)
    if name_match:
        event_name = name_match.group(1)
    else:
        cap_matches = re.findall(r'\b([A-Z][a-z]+ [A-Z][a-z]+( [A-Z][a-z]+)*)\b', title)
        if cap_matches:
            event_name = cap_matches[0][0]
    
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}(st|nd|rd|th)?\b',
        r'\b\d{1,2}(st|nd|rd|th)? (of )?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b',
        r'\b(next|this) (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b',
        r'\btonight\b', r'\btomorrow\b', r'\bweekend\b'
    ]
    
    event_date = None
    for pattern in date_patterns:
        date_match = re.search(pattern, combined_text, re.IGNORECASE)
        if date_match:
            event_date = date_match.group(0)
            break
    
    event_types = {
        "music": ["concert", "music", "band", "performance", "gig", "show", "festival"],
        "food": ["food", "dining", "restaurant", "taste", "culinary", "chef"],
        "art": ["exhibition", "gallery", "art", "museum", "display"],
        "sports": ["game", "match", "sports", "competition", "tournament", "championship"],
        "technology": ["tech", "hackathon", "coding", "startup", "digital"],
        "community": ["meetup", "gathering", "community", "networking", "social"],
        "educational": ["lecture", "seminar", "workshop", "class", "conference"],
        "entertainment": ["comedy", "theater", "movie", "film", "play", "entertainment"],
        "outdoor": ["hike", "outdoor", "nature", "park", "trail", "adventure"],
        "nightlife": ["club", "bar", "nightlife", "party", "dancing"]
    }
    
    event_type = "general"
    for type_name, keywords in event_types.items():
        for keyword in keywords:
            if keyword in combined_text:
                event_type = type_name
                break
        if event_type != "general":
            break
    
    return {
        "is_event": is_event,
        "name": event_name,
        "date": event_date,
        "type": event_type
    }

def detailed_sentiment_analysis(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity
    
    if polarity >= 0.5:
        sentiment = "very positive"
    elif 0.1 <= polarity < 0.5:
        sentiment = "positive"
    elif -0.1 < polarity < 0.1:
        sentiment = "neutral"
    elif -0.5 < polarity <= -0.1:
        sentiment = "negative"
    else:
        sentiment = "very negative"
    
    emotion_keywords = {
        "excited": ["excited", "amazing", "awesome", "incredible", "pumped", "can't wait", "stoked"],
        "happy": ["happy", "glad", "joy", "pleased", "delighted", "enjoy"],
        "interested": ["interesting", "curious", "intrigued", "fascinating"],
        "disappointed": ["disappointed", "sad", "unfortunate", "letdown", "bummer"],
        "angry": ["angry", "mad", "furious", "upset", "outraged"],
        "concerned": ["concerned", "worried", "anxious", "fear", "scared"]
    }
    
    emotion_type = "neutral"
    emotion_strength = 0
    
    text_lower = text.lower()
    for emotion, keywords in emotion_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                count = text_lower.count(keyword)
                if count > emotion_strength:
                    emotion_type = emotion
                    emotion_strength = count
    
    return sentiment, round(polarity, 2), emotion_type

def extract_keywords(text):
    stopwords = ["the", "and", "or", "in", "on", "at", "to", "a", "an", "is", "are", "was", "were", 
                "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", 
                "shall", "should", "may", "might", "must", "can", "could", "of", "for", "with", 
                "about", "against", "between", "into", "through", "during", "before", "after", 
                "above", "below", "from", "up", "down", "this", "that", "these", "those", "my", 
                "your", "his", "her", "its", "our", "their", "what", "which", "who", "whom", 
                "whose", "when", "where", "why", "how", "all", "any", "both", "each", "more"]
    
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
    words = cleaned_text.split()
    
    keywords = [word for word in words if word not in stopwords and len(word) > 2]
    
    return keywords

def fetch_location_events(location, radius_km=50, use_demo_data=False):
    if use_demo_data:
        return generate_demo_data(location)
        
    if not (REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET and REDDIT_USER_AGENT):
        return {"error": "Reddit API credentials missing!"}

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID, 
            client_secret=REDDIT_CLIENT_SECRET, 
            user_agent=REDDIT_USER_AGENT
        )
    except Exception as e:
        return {"error": f"Reddit API connection failed: {str(e)}"}
    
    search_queries = [
        f"{location} event", 
        f"{location} festival", 
        f"{location} concert",
        f"{location} meetup",
        f"{location} happening",
        f"events in {location}",
        f"what's happening in {location}"
    ]
    
    all_events = []
    event_keywords = []
    event_names = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, query in enumerate(search_queries):
        progress = int((i / len(search_queries)) * 100)
        progress_bar.progress(progress)
        status_text.text(f"Searching for: {query}")
        
        try:
            subreddits = [
                location.lower(),
                f"events",
                "festivals",
                "concerts",
                "all"
            ]
            
            for subreddit in subreddits:
                try:
                    for submission in reddit.subreddit(subreddit).search(
                        query, 
                        sort="new", 
                        time_filter="week", 
                        limit=15
                    ):
                        event_info = extract_event_info(submission.title, submission.selftext, location)
                        
                        if event_info["is_event"]:
                            sentiment, score, emotion_type = detailed_sentiment_analysis(
                                f"{submission.title} {submission.selftext}"
                            )
                            
                            popularity = submission.score + (submission.num_comments * 3)
                            
                            event_data = {
                                "title": submission.title,
                                "text": submission.selftext[:200] + "..." if len(submission.selftext) > 200 else submission.selftext,
                                "url": f"https://reddit.com{submission.permalink}",
                                "created_utc": datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                                "sentiment": sentiment,
                                "sentiment_score": score,
                                "emotion_type": emotion_type,
                                "event_date": event_info["date"],
                                "event_type": event_info["type"],
                                "popularity": popularity,
                                "upvotes": submission.score,
                                "num_comments": submission.num_comments
                            }
                            
                            all_events.append(event_data)
                            
                            keywords = extract_keywords(submission.title + " " + submission.selftext)
                            event_keywords.extend(keywords)
                            
                            if event_info["name"]:
                                event_names.append(event_info["name"])
                            
                            submission.comments.replace_more(limit=0)
                            for comment in list(submission.comments)[:5]:
                                comment_sentiment, comment_score, comment_emotion = detailed_sentiment_analysis(comment.body)
                                
                                comment_data = {
                                    "type": "comment",
                                    "text": comment.body[:150] + "..." if len(comment.body) > 150 else comment.body,
                                    "sentiment": comment_sentiment,
                                    "sentiment_score": comment_score,
                                    "emotion_type": comment_emotion,
                                    "upvotes": comment.score,
                                    "event_reference": submission.title
                                }
                                all_events.append(comment_data)
                except Exception as e:
                    continue
        except Exception as e:
            continue
    
    progress_bar.progress(100)
    status_text.text("Analysis complete!")
    time.sleep(0.5)
    status_text.empty()
    progress_bar.empty()
    
    trending_events = analyze_trending_events(event_keywords, event_names, all_events)
    sentiment_stats = calculate_sentiment_stats(all_events)
    
    result = {
        "location": location,
        "total_events_found": len([e for e in all_events if e.get("type") != "comment"]),
        "trending_events": trending_events,
        "sentiment_breakdown": sentiment_stats,
        "event_details": sort_events_by_relevance(all_events)[:20]
    }
    
    if not all_events:
        result["message"] = f"No events found for {location}. Try a larger city or check your spelling."
    
    return result

def analyze_trending_events(keywords, event_names, events):
    keyword_counter = Counter(keywords)
    event_name_counter = Counter(event_names)
    event_types = [event.get("event_type") for event in events if event.get("event_type")]
    event_type_counter = Counter(event_types)
    
    top_keywords = [kw for kw, count in keyword_counter.most_common(20) if count > 1]
    top_event_names = [name for name, count in event_name_counter.most_common(5) if count > 1]
    top_event_types = [t for t, count in event_type_counter.most_common(3) if count > 1]
    
    event_popularity = {}
    for event in events:
        if "title" in event:
            title = event["title"]
            if title not in event_popularity:
                event_popularity[title] = {
                    "title": title,
                    "upvotes": event.get("upvotes", 0),
                    "comments": event.get("num_comments", 0),
                    "sentiment_score": event.get("sentiment_score", 0),
                    "popularity_score": 0
                }
            else:
                event_popularity[title]["upvotes"] += event.get("upvotes", 0)
                event_popularity[title]["comments"] += event.get("num_comments", 0)
    
    for title in event_popularity:
        event_popularity[title]["popularity_score"] = (
            event_popularity[title]["upvotes"] * 1 + 
            event_popularity[title]["comments"] * 3
        )
    
    top_events = sorted(
        event_popularity.values(), 
        key=lambda x: x["popularity_score"], 
        reverse=True
    )[:5]
    
    return {
        "top_keywords": top_keywords,
        "top_event_names": top_event_names,
        "top_event_types": top_event_types,
        "most_popular_events": top_events
    }

def calculate_sentiment_stats(events):
    sentiments = [event.get("sentiment") for event in events if "sentiment" in event]
    sentiment_counter = Counter(sentiments)
    
    emotions = [event.get("emotion_type") for event in events if "emotion_type" in event]
    emotion_counter = Counter(emotions)
    
    sentiment_scores = [event.get("sentiment_score", 0) for event in events if "sentiment_score" in event]
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    
    return {
        "sentiment_counts": dict(sentiment_counter),
        "emotion_counts": dict(emotion_counter),
        "average_sentiment_score": round(avg_sentiment, 2),
        "overall_mood": "positive" if avg_sentiment > 0.1 else 
                        "negative" if avg_sentiment < -0.1 else "neutral"
    }

def sort_events_by_relevance(events):
    def get_relevance_score(event):
        base_score = 0
        if event.get("type") != "comment":
            base_score += 50
            base_score += event.get("upvotes", 0) * 0.5
            base_score += event.get("num_comments", 0) * 2
            if event.get("event_date"):
                base_score += 20
            if "created_utc" in event:
                try:
                    created_date = datetime.strptime(event["created_utc"], '%Y-%m-%d %H:%M:%S')
                    now = datetime.now()
                    days_old = (now - created_date).days
                    if days_old <= 1:
                        base_score += 30
                    elif days_old <= 3:
                        base_score += 15
                    elif days_old <= 7:
                        base_score += 5
                except:
                    pass
        else:
            base_score += event.get("upvotes", 0) * 0.5
        return base_score
    
    return sorted(events, key=get_relevance_score, reverse=True)

def generate_demo_data(location):
    event_types = ["music", "food", "art", "sports", "technology", "community", 
                  "educational", "entertainment", "outdoor", "nightlife"]
    sentiments = ["very positive", "positive", "neutral", "negative", "very negative"]
    emotions = ["excited", "happy", "interested", "disappointed", "angry", "concerned", "neutral"]
    
    event_names = [
        f"{location} Music Festival",
        f"Downtown {location} Art Walk",
        f"{location} Food & Wine Festival",
        f"{location} Tech Meetup",
        f"Annual {location} Marathon",
        f"{location} Comic Convention",
        f"Jazz in {location}",
        f"{location} Film Festival",
        f"Taste of {location}",
        f"{location} Street Fair"
    ]
    
    events = []
    for i in range(15):
        event_type = random.choice(event_types)
        sentiment = random.choice(sentiments)
        sentiment_score = random.uniform(-0.8, 0.8)
        if sentiment == "very positive":
            sentiment_score = random.uniform(0.5, 0.9)
        elif sentiment == "positive":
            sentiment_score = random.uniform(0.1, 0.5)
        elif sentiment == "neutral":
            sentiment_score = random.uniform(-0.1, 0.1)
        elif sentiment == "negative":
            sentiment_score = random.uniform(-0.5, -0.1)
        else:
            sentiment_score = random.uniform(-0.9, -0.5)
        
        upvotes = random.randint(5, 500)
        comments = random.randint(2, 50)
        event_date_offset = random.randint(1, 14)
        event_date = (datetime.now() + timedelta(days=event_date_offset)).strftime("%b %d")
        
        if random.random() < 0.7:
            title = random.choice(event_names)
        else:
            descriptors = ["Amazing", "Annual", "Incredible", "Official", "Community"]
            title = f"{random.choice(descriptors)} {location} {event_type.capitalize()} Event"
        
        event = {
            "title": title,
            "text": f"Join us for this exciting {event_type} event in {location}! Happening on {event_date}.",
            "url": "https://reddit.com/r/events",
            "created_utc": (datetime.now() - timedelta(days=random.randint(0, 5))).strftime('%Y-%m-%d %H:%M:%S'),
            "sentiment": sentiment,
            "sentiment_score": round(sentiment_score, 2),
            "emotion_type": random.choice(emotions),
            "event_date": event_date,
            "event_type": event_type,
            "popularity": upvotes + (comments * 3),
            "upvotes": upvotes,
            "num_comments": comments
        }
        events.append(event)
    return {"event_details": events}

# Main App
def main():
    st.title("🎭 EventPulse & Recommendation System")
    
    # Sidebar navigation with radio button
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["User Recommendations", "General Events", "Organizer Insights", "Sentiment Analysis"])
    
    # Load data for recommendation system pages
    if page in ["User Recommendations", "General Events", "Organizer Insights"]:
        users_df, events_df, bookings_df, organizers_df = load_data()
        if users_df is None:
            st.stop()
        users_df, events_df, user_interests, user_history, event_users, event_categories = preprocess_data(users_df, events_df, bookings_df)
    
    # Page routing
    if page == "User Recommendations":
        st.header("Personalized Event Recommendations")
        
        user_ids = users_df["user_id"].tolist()
        user_id = st.selectbox("Select a user", user_ids)
        
        if user_id:
            user_info = users_df[users_df["user_id"] == user_id].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("User Information")
                st.write(f"**Name:** {user_info['name']}")
                st.write(f"**Location:** {user_info['location']}")
                st.write(f"**Preferences:** {', '.join(user_info['preferences'])}")
            
            with col2:
                st.subheader("Social Connections")
                connections = user_info['social_connections']
                if connections:
                    connection_names = users_df[users_df['user_id'].isin(connections)]['name'].tolist()
                    st.write(", ".join(connection_names))
                else:
                    st.write("No social connections")
            
            recommended_events, all_scored_events = recommend_events(
                user_id, users_df, events_df, user_history, 
                event_categories, user_interests, event_users
            )
            
            if not recommended_events.empty:
                st.subheader("Top Recommendations")
                display_df = recommended_events.copy()
                display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
                st.table(display_df[["name", "category", "location", "date", "time", "popularity_score"]])
                
                st.subheader("Recommendation Scores Breakdown")
                top_events = all_scored_events.sort_values("score", ascending=False).head(10)
                fig = px.bar(
                    top_events,
                    x="name",
                    y=["location_score", "preference_score", "collaborative_score"],
                    title="Top Events Score Breakdown",
                    labels={"value": "Score", "name": "Event", "variable": "Factor"},
                    color_discrete_map={
                        "location_score": "blue",
                        "preference_score": "green",
                        "collaborative_score": "orange"
                    }
                )
                st.plotly_chart(fig)
                
                precision, recall, f1 = evaluate_recommendations(
                    user_id, recommended_events, user_interests, 
                    event_categories, events_df
                )
                
                st.subheader("Recommendation Quality")
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                metrics_col1.metric("Precision", f"{precision:.2f}")
                metrics_col2.metric("Recall", f"{recall:.2f}")
                metrics_col3.metric("F1 Score", f"{f1:.2f}")
            else:
                st.warning("No recommendations found for this user")
    
    elif page == "General Events":
        st.header("Popular Upcoming Events")
        general_events = get_general_events(events_df)
        
        display_df = general_events.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        
        st.subheader("Event Locations")
        np.random.seed(42)
        map_data = pd.DataFrame({
            'lat': np.random.uniform(37.7, 38.0, size=len(general_events)),
            'lon': np.random.uniform(-122.5, -122.3, size=len(general_events)),
            'name': general_events['name'],
            'category': general_events['category']
        })
        st.map(map_data)
        
        st.subheader("Top Popular Events")
        st.table(display_df[["name", "category", "location", "date", "time", "popularity_score"]])
        
        st.subheader("Events by Category")
        category_counts = general_events["category"].value_counts().reset_index()
        category_counts.columns = ["Category", "Count"]
        fig = px.pie(category_counts, values="Count", names="Category", title="Event Categories")
        st.plotly_chart(fig)
    
    elif page == "Organizer Insights":
        st.header("Organizer Insights Dashboard")
        
        insights_df = organizer_insights(events_df, bookings_df, organizers_df)
        
        st.subheader("Key Performance Metrics")
        total_revenue = insights_df["total_price"].sum()
        total_tickets = insights_df["ticket_quantity"].sum()
        avg_rating = insights_df["rating"].mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${total_revenue:,.2f}")
        col2.metric("Total Tickets Sold", f"{total_tickets:,}")
        col3.metric("Average Rating", f"{avg_rating:.1f}/5.0")
        
        st.subheader("Event Performance")
        top_revenue_events = insights_df.sort_values("total_price", ascending=False).head(10)
        fig1 = px.bar(
            top_revenue_events,
            x="event_name",
            y="total_price",
            title="Top Events by Revenue",
            labels={"total_price": "Revenue ($)", "event_name": "Event"}
        )
        st.plotly_chart(fig1)
        
        st.subheader("Pricing Strategy Analysis")
        strategy_perf = insights_df.groupby("pricing_strategy").agg({
            "total_price": "sum",
            "ticket_quantity": "sum",
            "rating": "mean"
        }).reset_index()
        strategy_perf["average_ticket_price"] = strategy_perf["total_price"] / strategy_perf["ticket_quantity"]
        fig2 = px.bar(
            strategy_perf,
            x="pricing_strategy",
            y=["total_price", "ticket_quantity"],
            title="Performance by Pricing Strategy",
            barmode="group",
            labels={"pricing_strategy": "Strategy", "value": "Value", "variable": "Metric"}
        )
        st.plotly_chart(fig2)
        
        if st.checkbox("Show Raw Data"):
            st.dataframe(insights_df)
    
    elif page == "Sentiment Analysis":
        st.header("EventPulse: Location-Based Event Analyzer")
        st.markdown("Analyze social media sentiment and trends to discover events happening in your area.")
        
        st.sidebar.header("Search Parameters")
        location = st.sidebar.text_input("Location", "Los Angeles")
        use_demo_data = st.sidebar.checkbox("Use Demo Data (No API calls)", value=True)
        
        if st.sidebar.button("Find Events"):
            with st.spinner(f"Analyzing events in {location}..."):
                results = fetch_location_events(location, use_demo_data=use_demo_data)
                
                if "error" in results:
                    st.error(results["error"])
                else:
                    st.success(f"Found {results['total_events_found']} events in {location}")
                    
                    for event in results["event_details"]:
                        if "title" not in event:
                            continue
                        st.subheader(event["title"])
                        st.write(f"📅 Date: {event['event_date']}")
                        st.write(f"📢 Type: {event['event_type'].capitalize()}")
                        st.write(f"📊 Sentiment: {event['sentiment']} (Score: {event['sentiment_score']})")
                        st.write(f"💬 Emotion: {event['emotion_type']}")
                        st.write(f"🔥 Popularity Score: {event['popularity']} (Upvotes: {event['upvotes']}, Comments: {event['num_comments']})")
                        st.markdown("---")

if __name__ == "__main__":
    main()