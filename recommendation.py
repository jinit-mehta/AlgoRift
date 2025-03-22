import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
from multiprocessing import Pool
from random import uniform
import time

# Constants
WEIGHTS = {"location": 0.5, "prefs": 0.3, "collab": 0.2}
CITIES = ["New York", "London", "Tokyo", "Sydney", "Paris", "Berlin", "Toronto", "Mumbai", "São Paulo", "Cape Town",
          "Los Angeles", "Shanghai", "Singapore", "Dubai", "Moscow", "Mexico City", "Bangkok", "Istanbul", "Seoul", "Madrid"]

def load_data():
    return (pd.read_csv("data/users.csv"), pd.read_csv("data/events.csv"), 
            pd.read_csv("data/bookings.csv"), pd.read_csv("data/organizers.csv"))

def preprocess_data(users_df, events_df, bookings_df):
    # Parse list columns
    users_df["preferences"] = users_df["preferences"].apply(eval)
    users_df["social_connections"] = users_df["social_connections"].apply(eval)
    users_df["attended_events"] = users_df["attended_events"].apply(eval)
    users_df["city"] = users_df["location"].apply(lambda x: x.split(",")[0].strip())
    events_df["city"] = events_df["location"].apply(lambda x: x.split(",")[0].strip())
    events_df["date"] = pd.to_datetime(events_df["date"])
    
    # Precompute user interests, history, and collaborative data
    user_interests = bookings_df[bookings_df["interested"] == 1].groupby("user_id")["event_id"].apply(set).to_dict()
    user_history = bookings_df.groupby("user_id")["event_id"].apply(set).to_dict()
    event_users = bookings_df.groupby("event_id")["user_id"].apply(set).to_dict()
    event_categories = events_df.set_index("event_id")["category"].to_dict()
    
    return users_df, events_df, user_interests, user_history, event_users, event_categories

def collab_filtering(user_id, users_df, user_interests, user_history, event_users, event_categories):
    user = users_df[users_df["user_id"] == user_id].iloc[0]
    attended = user_history.get(user_id, set())
    friends = user["social_connections"]
    
    # Collaborative events from past attendance and friend interests
    collab_events = set()
    for event in attended:
        collab_events.update(event_users.get(event, set()))
    for friend in friends:
        collab_events.update(user_interests.get(friend, set()))
    
    # Map to categories of interest
    interested_categories = {event_categories.get(e) for e in user_interests.get(user_id, set()) if e in event_categories}
    return interested_categories

def recommend_events(user_id, users_df, events_df, user_interests, user_history, event_users, event_categories):
    user = users_df[users_df["user_id"] == user_id].iloc[0]
    user_city, user_prefs = user["city"], user["preferences"]
    exploration_score = user["exploration_score"]
    attended = user_history.get(user_id, set())
    collab_categories = collab_filtering(user_id, users_df, user_interests, user_history, event_users, event_categories)
    
    # Filter to future events
    future_events = events_df[events_df["date"] > pd.Timestamp("today")]
    
    # Vectorized scoring
    loc_scores = (future_events["city"] == user_city).astype(int)
    pref_scores = future_events["category"].isin(user_prefs).astype(int)
    collab_scores = future_events["category"].isin(collab_categories).astype(int)
    scores = (WEIGHTS["location"] * loc_scores + 
              WEIGHTS["prefs"] * pref_scores + 
              WEIGHTS["collab"] * collab_scores)
    
    # Exploration factor
    explore_mask = (pref_scores == 0) & (np.random.uniform(0, 1, len(future_events)) < exploration_score)
    scores += explore_mask * 0.1
    
    # Recommend top 5 un-attended future events
    mask = ~future_events["event_id"].isin(attended)
    top_indices = scores[mask].argsort()[-5:][::-1]
    return future_events["event_id"][mask].iloc[top_indices].tolist()

def evaluate_recommendations(user_id, recommendations, events_df, user_interests, event_categories):
    # Simulate future interest based on past interested categories
    interested_categories = {event_categories.get(e) for e in user_interests.get(user_id, set()) if e in event_categories}
    future_events = events_df[events_df["date"] > pd.Timestamp("today")]
    actual = set(future_events[future_events["category"].isin(interested_categories)]["event_id"])
    
    predicted = set(recommendations)
    if not actual or not predicted:
        return 0, 0, 0
    y_true = [1 if e in actual else 0 for e in predicted]
    y_pred = [1] * len(predicted)
    return (precision_score(y_true, y_pred, zero_division=0),
            recall_score(y_true, y_pred, zero_division=0),
            f1_score(y_true, y_pred, zero_division=0))

def organizer_insights(events_df, bookings_df, organizers_df):
    event_stats = bookings_df.groupby("event_id").agg({
        "total_price": "sum",
        "ticket_quantity": "sum",
        "rating": "mean"
    }).reset_index()
    insights = pd.merge(events_df[["event_id", "name", "popularity_score", "city"]], event_stats, on="event_id")
    insights = pd.merge(insights, organizers_df[["event_id", "pricing_strategy"]], on="event_id")
    return insights.rename(columns={"name": "event_name"})

def parallel_recommendations(args):
    user_id, users_df, events_df, user_interests, user_history, event_users, event_categories = args
    return user_id, recommend_events(user_id, users_df, events_df, user_interests, user_history, event_users, event_categories)

if __name__ == "__main__":
    start_time = time.time()
    
    # Load and preprocess
    print("Loading and preprocessing data...")
    users_df, events_df, bookings_df, organizers_df = load_data()
    users_df, events_df, user_interests, user_history, event_users, event_categories = preprocess_data(users_df, events_df, bookings_df)
    
    # Split data (for reference, not used in evaluation here)
    print("Splitting data...")
    train_bookings, test_bookings = train_test_split(bookings_df, test_size=0.2, random_state=42)
    
    # Generate recommendations
    print("Generating recommendations...")
    sample_users = users_df["user_id"].sample(10).tolist()
    with Pool() as pool:
        results = pool.map(parallel_recommendations, 
                          [(u, users_df, events_df, user_interests, user_history, event_users, event_categories) 
                           for u in sample_users])
    
    # Evaluate
    print("Evaluating recommendations...")
    for user_id, recs in results:
        precision, recall, f1 = evaluate_recommendations(user_id, recs, events_df, user_interests, event_categories)
        print(f"User {user_id}: Precision={precision:.2f}, Recall={recall:.2f}, F1={f1:.2f}")
    
    # Organizer insights
    print("Generating organizer insights...")
    insights = organizer_insights(events_df, bookings_df, organizers_df)
    print(insights.head())
    
    print(f"Total runtime: {time.time() - start_time:.2f} seconds")