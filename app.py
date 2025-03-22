import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json
from textblob import TextBlob
import random
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

# Configuration
st.set_page_config(
    page_title="TufanTicket - AI Event Platform",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #FF8C00;
        font-weight: 500;
    }
    .card {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .insight-card {
        background-color: #E6F3FF;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .positive {color: green;}
    .negative {color: red;}
    .neutral {color: gray;}
</style>
""", unsafe_allow_html=True)

# Mock API functions
def fetch_events_api(category=None, location=None, date_range=None):
    """Simulate fetching events from an API like Ticketmaster or Eventbrite"""
    # In a real app, this would make API calls to event platforms
    
    event_categories = ['Music', 'Sports', 'Arts & Theater', 'Food & Drink', 'Tech', 'Wellness']
    locations = ['New York', 'Los Angeles', 'Chicago', 'Miami', 'Austin', 'Seattle']
    artists = [
        'Taylor Swift', 'Bad Bunny', 'The Weeknd', 'Billie Eilish', 'BTS', 
        'Dua Lipa', 'Kendrick Lamar', 'Olivia Rodrigo', 'Post Malone', 'Harry Styles'
    ]
    venues = ['Madison Square Garden', 'Hollywood Bowl', 'United Center', 'Barclays Center', 'Moody Center']
    
    # Filter based on inputs
    if category:
        filtered_categories = [category]
    else:
        filtered_categories = event_categories
    
    if location:
        filtered_locations = [location]
    else:
        filtered_locations = locations
    
    events = []
    for i in range(50):  # Generate 50 mock events
        event_date = datetime.now() + timedelta(days=random.randint(1, 90))
        
        # Only include if in date range (if specified)
        if date_range and (event_date.date() < date_range[0] or event_date.date() > date_range[1]):
            continue
            
        price_base = random.randint(30, 200)
        event = {
            'id': f'evt-{i}',
            'name': f"{random.choice(['Live', 'Festival', 'Tour', 'Experience', 'Summit'])} {random.randint(2023, 2025)}",
            'category': random.choice(filtered_categories),
            'artist': random.choice(artists),
            'venue': random.choice(venues),
            'location': random.choice(filtered_locations),
            'date': event_date.strftime('%Y-%m-%d'),
            'time': f"{random.randint(12, 22)}:00",
            'base_price': price_base,
            'vip_price': price_base * 2.5,
            'capacity': random.randint(500, 25000),
            'tickets_sold': random.randint(100, 24000),
            'popularity_score': random.randint(50, 100),
            'trending_score': random.randint(1, 100) / 100,
        }
        events.append(event)
    
    return events

def fetch_social_sentiment(keyword):
    """Simulate fetching social media sentiment for a keyword"""
    # In a real app, use APIs like Twitter API, Reddit API, etc.
    sentiments = ['positive', 'negative', 'neutral']
    weights = [0.6, 0.2, 0.2]  # Biased toward positive for demo
    
    results = []
    for _ in range(100):
        sentiment = random.choices(sentiments, weights=weights)[0]
        if sentiment == 'positive':
            score = random.uniform(0.5, 1.0)
        elif sentiment == 'negative':
            score = random.uniform(-1.0, -0.3)
        else:
            score = random.uniform(-0.3, 0.3)
            
        results.append({
            'text': f"Sample comment about {keyword}",
            'sentiment': sentiment,
            'score': score,
            'platform': random.choice(['Twitter', 'Instagram', 'TikTok', 'Reddit'])
        })
    
    return results

def predict_ticket_sales(event_data):
    """Use ML to predict ticket sales based on event attributes"""
    # This would be a real ML model in production
    
    X = np.array([
        event_data['popularity_score'], 
        event_data['base_price'],
        event_data['trending_score'] * 100
    ]).reshape(1, -1)
    
    # Mock linear model
    coef = np.array([150, -5, 50])
    intercept = 1000
    
    predicted_sales = np.dot(X, coef) + intercept + random.uniform(-500, 500)
    predicted_sales = min(predicted_sales[0], event_data['capacity'])
    predicted_sales = max(predicted_sales, 0)
    
    return int(predicted_sales)

def generate_budget_estimate(event_data):
    """Generate an AI-based budget estimate for event organizers"""
    capacity = event_data['capacity']
    
    # Basic cost calculations
    venue_cost = capacity * random.uniform(5, 15)
    artist_cost = capacity * random.uniform(10, 30)
    staff_cost = capacity / 100 * random.uniform(150, 250)
    marketing_cost = capacity * random.uniform(2, 8)
    equipment_cost = capacity * random.uniform(3, 10)
    insurance_cost = capacity * random.uniform(1, 3)
    
    # Expected revenue
    expected_sales = event_data.get('predicted_sales', event_data['capacity'] * 0.7)
    revenue = expected_sales * event_data['base_price']
    
    # Calculate profit margin
    total_cost = venue_cost + artist_cost + staff_cost + marketing_cost + equipment_cost + insurance_cost
    profit = revenue - total_cost
    profit_margin = (profit / revenue) * 100 if revenue > 0 else 0
    
    budget = {
        'venue_cost': int(venue_cost),
        'artist_cost': int(artist_cost),
        'staff_cost': int(staff_cost),
        'marketing_cost': int(marketing_cost),
        'equipment_cost': int(equipment_cost),
        'insurance_cost': int(insurance_cost),
        'total_cost': int(total_cost),
        'expected_revenue': int(revenue),
        'expected_profit': int(profit),
        'profit_margin': round(profit_margin, 2)
    }
    
    return budget

def detect_anomalies(sales_data):
    """Detect anomalies in ticket sales data"""
    if len(sales_data) < 10:
        return [False] * len(sales_data)
    
    # Use Isolation Forest for anomaly detection
    model = IsolationForest(contamination=0.05, random_state=42)
    
    # Reshape for scikit-learn
    X = np.array(sales_data).reshape(-1, 1)
    
    # Fit and predict
    anomalies = model.fit_predict(X)
    
    # Convert to boolean (True means anomaly)
    return [pred == -1 for pred in anomalies]

def get_optimal_price(event_data):
    """Calculate optimal ticket price based on demand and capacity"""
    # This would use more sophisticated price elasticity models in production
    base_price = event_data['base_price']
    popularity = event_data['popularity_score'] / 100
    trending = event_data['trending_score']
    
    # Simple price optimization model
    if popularity > 0.8 and trending > 0.7:
        # High demand, can increase price
        optimal_price = base_price * random.uniform(1.1, 1.3)
    elif popularity < 0.6 or trending < 0.4:
        # Low demand, should decrease price
        optimal_price = base_price * random.uniform(0.8, 0.95)
    else:
        # Moderate demand, slight adjustment
        optimal_price = base_price * random.uniform(0.95, 1.05)
    
    return round(optimal_price, 2)

def generate_event_ideas(location, category):
    """Generate AI-powered event ideas based on location and category"""
    # This would use an AI model or LLM API in production
    
    music_ideas = [
        "K-Pop Fan Festival", 
        "Indie Music Showcase", 
        "Electronic Music Night", 
        "90s Throwback Concert",
        "Hip-Hop Battle"
    ]
    
    sports_ideas = [
        "E-Sports Tournament", 
        "Urban Basketball Competition", 
        "Extreme Sports Exhibition", 
        "College Sports Fan Day",
        "Mixed Martial Arts Showcase"
    ]
    
    arts_ideas = [
        "Digital Art Exhibition", 
        "Immersive Theater Experience", 
        "Street Art Festival", 
        "Modern Dance Showcase",
        "Interactive Art Installation"
    ]
    
    tech_ideas = [
        "Tech Startup Pitch Night", 
        "Coding Hackathon", 
        "AI Innovation Conference", 
        "Gaming Convention",
        "Blockchain Workshop"
    ]
    
    food_ideas = [
        "International Food Festival", 
        "Craft Beer Tasting", 
        "Vegan Food Fair", 
        "Food Truck Rally",
        "Celebrity Chef Cook-Off"
    ]
    
    ideas_map = {
        "Music": music_ideas,
        "Sports": sports_ideas,
        "Arts & Theater": arts_ideas,
        "Tech": tech_ideas,
        "Food & Drink": food_ideas
    }
    
    selected_ideas = ideas_map.get(category, music_ideas)
    return [f"{idea} in {location}" for idea in selected_ideas]

# Sidebar navigation
st.sidebar.markdown("<div class='main-header'>TufanTicket 🎭</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

app_mode = st.sidebar.selectbox(
    "Select Dashboard",
    ["Event Discovery", "Organizer Analytics", "Budget Estimator", "Trend Analysis"]
)

# Main content
if app_mode == "Event Discovery":
    st.markdown("<div class='main-header'>AI-Powered Event Discovery</div>", unsafe_allow_html=True)
    st.markdown("Find your next unforgettable experience with personalized recommendations")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox(
            "Event Category",
            [None, "Music", "Sports", "Arts & Theater", "Food & Drink", "Tech", "Wellness"]
        )
    with col2:
        location = st.selectbox(
            "Location",
            [None, "New York", "Los Angeles", "Chicago", "Miami", "Austin", "Seattle"]
        )
    with col3:
        date_range = st.date_input(
            "Date Range",
            value=[datetime.now().date(), (datetime.now() + timedelta(days=90)).date()],
            min_value=datetime.now().date(),
            max_value=(datetime.now() + timedelta(days=365)).date()
        )
    
    st.markdown("---")
    
    # Fetch events based on filters
    events = fetch_events_api(category, location, date_range)
    
    if not events:
        st.warning("No events found matching your criteria. Try changing your filters.")
    else:
        # Convert to DataFrame for easier manipulation
        events_df = pd.DataFrame(events)
        
        # Add predictions to each event
        for i, event in events_df.iterrows():
            events_df.at[i, 'predicted_sales'] = predict_ticket_sales(event)
            events_df.at[i, 'optimal_price'] = get_optimal_price(event)
        
        # Calculate additional metrics
        events_df['tickets_remaining'] = events_df['capacity'] - events_df['tickets_sold']
        events_df['percent_sold'] = (events_df['tickets_sold'] / events_df['capacity'] * 100).round(1)
        events_df['sell_out_prediction'] = events_df['predicted_sales'] >= events_df['capacity']
        
        # Personalized recommendations
        st.markdown("<div class='sub-header'>🔥 Trending Events</div>", unsafe_allow_html=True)
        trending_events = events_df.sort_values('trending_score', ascending=False).head(3)
        
        trending_cols = st.columns(3)
        for i, (_, event) in enumerate(trending_events.iterrows()):
            with trending_cols[i]:
                st.markdown(f"<div class='card'>"
                            f"<h3>{event['name']}</h3>"
                            f"<p><strong>{event['artist']}</strong> at {event['venue']}</p>"
                            f"<p>📍 {event['location']} | 📅 {event['date']} {event['time']}</p>"
                            f"<p>🎟️ ${event['base_price']} | "
                            f"<span class='{'positive' if event['percent_sold'] > 75 else 'neutral'}'>📊 {event['percent_sold']}% Sold</span></p>"
                            f"</div>", unsafe_allow_html=True)
        
        # Event listing
        st.markdown("<div class='sub-header'>Discover Events</div>", unsafe_allow_html=True)
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["List View", "Map View"])
        
        with tab1:
            # Add pagination
            page_size = 10
            total_pages = len(events_df) // page_size + (1 if len(events_df) % page_size > 0 else 0)
            page = st.selectbox("Page", range(1, total_pages + 1)) if total_pages > 1 else 1
            
            start_idx = (page - 1) * page_size
            end_idx = min(start_idx + page_size, len(events_df))
            
            page_events = events_df.iloc[start_idx:end_idx]
            
            for _, event in page_events.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"### {event['name']}")
                    st.markdown(f"**Artist:** {event['artist']} | **Category:** {event['category']}")
                    st.markdown(f"📍 {event['venue']}, {event['location']} | 📅 {event['date']} {event['time']}")
                
                with col2:
                    st.markdown(f"**Base Price:** ${event['base_price']}")
                    st.markdown(f"**VIP Price:** ${event['vip_price']}")
                    st.markdown(f"**Sold:** {event['percent_sold']}%")
                
                with col3:
                    # For a real app, this would be a button that links to purchase
                    st.button(f"View Details", key=f"btn_{event['id']}")
                
                st.markdown("---")
                
        with tab2:
            st.info("Map view would show events geographically using Streamlit's map function with real venue coordinates")
            
            # In a real app, this would use st.map with actual venue coordinates
            # st.map(events_df[['latitude', 'longitude']])

elif app_mode == "Organizer Analytics":
    st.markdown("<div class='main-header'>Event Organizer Analytics</div>", unsafe_allow_html=True)
    st.markdown("Advanced AI insights to optimize your events and maximize attendance")
    
    # Mock event selection for organizers
    events = fetch_events_api()
    event_names = [e['name'] for e in events]
    
    selected_event_name = st.selectbox("Select Event to Analyze", event_names)
    selected_event = next(e for e in events if e['name'] == selected_event_name)
    
    # Add prediction data
    selected_event['predicted_sales'] = predict_ticket_sales(selected_event)
    selected_event['optimal_price'] = get_optimal_price(selected_event)
    
    # Display event metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tickets Sold", f"{selected_event['tickets_sold']:,}", 
                  f"{selected_event['tickets_sold'] - selected_event['capacity'] // 2:+,}")
    with col2:
        st.metric("Capacity", f"{selected_event['capacity']:,}")
    with col3:
        current_price = selected_event['base_price']
        optimal_price = selected_event['optimal_price']
        price_diff = ((optimal_price / current_price) - 1) * 100
        
        st.metric("Current Price", f"${current_price}", 
                  f"{price_diff:.1f}% to optimal" if abs(price_diff) > 5 else "Optimal")
    with col4:
        sell_through = (selected_event['tickets_sold'] / selected_event['capacity']) * 100
        st.metric("Sell-through Rate", f"{sell_through:.1f}%", 
                  f"{sell_through - 70:.1f}%" if sell_through > 70 else f"{sell_through - 70:.1f}%")
    
    st.markdown("---")
    
    # Generate simulated sales data
    days_to_event = 60
    current_day = random.randint(20, 40)
    
    dates = [(datetime.now() - timedelta(days=current_day-i)).strftime("%Y-%m-%d") for i in range(current_day)]
    sales_velocity = [int(selected_event['capacity'] * random.uniform(0.005, 0.02)) for _ in range(current_day)]
    cumulative_sales = np.cumsum(sales_velocity)
    
    # Detect sales anomalies
    anomalies = detect_anomalies(sales_velocity)
    anomaly_indices = [i for i, is_anomaly in enumerate(anomalies) if is_anomaly]
    anomaly_dates = [dates[i] for i in anomaly_indices]
    anomaly_sales = [sales_velocity[i] for i in anomaly_indices]
    
    # Generate future sales projection
    future_dates = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, days_to_event - current_day + 1)]
    
    # Simple regression for prediction
    X = np.array(range(current_day)).reshape(-1, 1)
    y = np.array(sales_velocity)
    
    model = LinearRegression()
    model.fit(X, y)
    
    future_X = np.array(range(current_day, days_to_event)).reshape(-1, 1)
    future_sales = model.predict(future_X)
    future_sales = [max(0, int(sale)) for sale in future_sales]
    
    all_dates = dates + future_dates
    all_sales = sales_velocity + future_sales
    all_cumulative = list(np.cumsum(all_sales))
    
    # Create sales velocity chart
    st.markdown("<div class='sub-header'>Ticket Sales Velocity</div>", unsafe_allow_html=True)
    
    # Setup a two-tab view
    tab1, tab2 = st.tabs(["Sales by Day", "Cumulative Sales"])
    
    with tab1:
        fig = go.Figure()
        
        # Current sales
        fig.add_trace(go.Bar(
            x=dates,
            y=sales_velocity,
            name="Actual Sales",
            marker_color="royalblue"
        ))
        
        # Projected sales
        fig.add_trace(go.Bar(
            x=future_dates,
            y=future_sales,
            name="Projected Sales",
            marker_color="lightblue"
        ))
        
        # Highlight anomalies
        if anomaly_indices:
            fig.add_trace(go.Scatter(
                x=anomaly_dates,
                y=anomaly_sales,
                mode="markers",
                marker=dict(color="red", size=10, symbol="circle"),
                name="Sales Anomaly"
            ))
        
        fig.update_layout(
            title="Daily Ticket Sales",
            xaxis_title="Date",
            yaxis_title="Tickets Sold",
            legend_title="Data",
            hovermode="x"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Anomaly insights
        if anomaly_indices:
            st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
            st.markdown("### 🔍 Sales Anomaly Detected")
            
            for date, sales in zip(anomaly_dates, anomaly_sales):
                direction = "spike" if sales > np.mean(sales_velocity) * 1.5 else "drop"
                st.markdown(f"- **{date}**: Unusual {direction} in sales ({sales} tickets)")
                
                # Generate possible explanation
                if direction == "spike":
                    reason = random.choice([
                        "social media mention by influencer", 
                        "promotional discount ended soon", 
                        "artist released new content",
                        "competing event canceled"
                    ])
                else:
                    reason = random.choice([
                        "technical issue with ticketing system", 
                        "negative press coverage", 
                        "competing event announced",
                        "holiday weekend"
                    ])
                
                st.markdown(f"  *Possible reason: {reason}*")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        fig = go.Figure()
        
        # Actual cumulative sales
        fig.add_trace(go.Scatter(
            x=dates,
            y=cumulative_sales,
            name="Actual Sales",
            line=dict(color="royalblue", width=3)
        ))
        
        # Projected cumulative sales
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=all_cumulative[current_day:],
            name="Projected Sales",
            line=dict(color="lightblue", width=3, dash="dash")
        ))
        
        # Capacity line
        fig.add_shape(
            type="line",
            x0=all_dates[0],
            y0=selected_event['capacity'],
            x1=all_dates[-1],
            y1=selected_event['capacity'],
            line=dict(color="red", width=2, dash="dot"),
        )
        
        fig.add_annotation(
            x=all_dates[len(all_dates)//2],
            y=selected_event['capacity'] * 1.05,
            text="Venue Capacity",
            showarrow=False,
            font=dict(color="red")
        )
        
        fig.update_layout(
            title="Cumulative Ticket Sales",
            xaxis_title="Date",
            yaxis_title="Total Tickets Sold",
            legend_title="Data",
            hovermode="x"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Sentiment analysis
    st.markdown("---")
    st.markdown("<div class='sub-header'>Social Media Sentiment Analysis</div>", unsafe_allow_html=True)
    
    # Get sentiment data
    sentiment_data = fetch_social_sentiment(selected_event['artist'])
    sentiment_counts = {
        'positive': sum(1 for item in sentiment_data if item['sentiment'] == 'positive'),
        'negative': sum(1 for item in sentiment_data if item['sentiment'] == 'negative'),
        'neutral': sum(1 for item in sentiment_data if item['sentiment'] == 'neutral')
    }
    
    # Calculate percentages
    total_sentiments = len(sentiment_data)
    sentiment_percentages = {
        key: value / total_sentiments * 100 
        for key, value in sentiment_counts.items()
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Pie chart of sentiment
        labels = list(sentiment_percentages.keys())
        values = list(sentiment_percentages.values())
        colors = ['#4CAF50', '#F44336', '#9E9E9E']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.4,
            marker_colors=colors
        )])
        
        fig.update_layout(
            title="Sentiment Distribution"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Platform breakdown
        platforms = ['Twitter', 'Instagram', 'TikTok', 'Reddit']
        platform_sentiments = {}
        
        for platform in platforms:
            platform_data = [item for item in sentiment_data if item['platform'] == platform]
            if not platform_data:
                continue
                
            platform_sentiments[platform] = {
                'positive': sum(1 for item in platform_data if item['sentiment'] == 'positive') / len(platform_data) * 100,
                'negative': sum(1 for item in platform_data if item['sentiment'] == 'negative') / len(platform_data) * 100,
                'neutral': sum(1 for item in platform_data if item['sentiment'] == 'neutral') / len(platform_data) * 100
            }
        
        # Create horizontal stacked bar chart
        fig = go.Figure()
        
        for sentiment, color in zip(['positive', 'neutral', 'negative'], colors):
            fig.add_trace(go.Bar(
                y=list(platform_sentiments.keys()),
                x=[platform_sentiments[platform][sentiment] for platform in platform_sentiments],
                name=sentiment.capitalize(),
                orientation='h',
                marker=dict(color=color)
            ))
        
        fig.update_layout(
            barmode='stack',
            title="Sentiment by Platform",
            xaxis_title="Percentage",
            yaxis_title="Platform",
            legend_title="Sentiment"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # AI Recommendations section
    st.markdown("---")
    st.markdown("<div class='sub-header'>AI-Powered Recommendations</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
        st.markdown("### 💰 Pricing Optimization")
        
        current_price = selected_event['base_price']
        optimal_price = selected_event['optimal_price']
        
        if optimal_price > current_price * 1.05:
            st.markdown(f"⬆️ **Recommendation: Increase ticket price to ${optimal_price}**")
            st.markdown(f"Current price (${current_price}) is below optimal based on demand analysis.")
            st.markdown(f"Projected revenue increase: ${(optimal_price - current_price) * selected_event['predicted_sales']:,.2f}")
        elif optimal_price < current_price * 0.95:
            st.markdown(f"⬇️ **Recommendation: Decrease ticket price to ${optimal_price}**")
            st.markdown(f"Current price (${current_price}) may be limiting attendance.")
            st.markdown(f"Projected attendance increase: {int((selected_event['capacity'] * 0.1))} tickets")
        else:
            st.markdown(f"✅ **Current price (${current_price}) is optimal**")
            st.markdown("Price is within the ideal range based on current demand signals.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
        st.markdown("### 📈 Marketing Recommendations")
        
        # Generate mock recommendations based on event data
        remaining_capacity = selected_event['capacity'] - selected_event['tickets_sold']
        days_left = days_to_event - current_day
        
        if remaining_capacity / selected_event['capacity'] > 0.4 and days_left < 30:
            st.markdown("🚨 **Recommendation: Increase marketing spend**")
            st.markdown(f"With {days_left} days left and {remaining_capacity} tickets unsold, consider:")
            st.markdown("- Targeted social media campaign focused on TikTok and Instagram")
            st.markdown("- Limited-time promotional discount")
            st.markdown("- Influencer partnerships")
        elif sentiment_percentages['negative'] > 25:
            st.markdown("⚠️ **Recommendation: Address negative sentiment**")
            st.markdown("Negative sentiment is higher than normal. Consider:")
            st.markdown("- Community engagement to address concerns")
            st.markdown("- Value-add announcements (special guests, experiences)")
            st.markdown("- Targeted PR to highlight positive aspects")
        else:
            st.markdown("✅ **Current marketing strategy is effective**")
            st.markdown("Continue current approach with minor adjustments:")
            st.markdown("- Maintain social media presence")
            st.markdown("- Focus on highlighting artist's recent content")
            st.markdown("- Consider early-bird referral incentives")
        
        st.markdown("</div>", unsafe_allow_html=True)

elif app_mode == "Budget Estimator":
    st.markdown("<div class='main-header'>AI Budget Estimator</div>", unsafe_allow_html=True)
    st.markdown("Generate intelligent budget projections for your events")
    
    # Form for event details
    with st.form("budget_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            event_name = st.text_input("Event Name", "My Amazing Event")
            event_type = st.selectbox(
                "Event Type",
                ["Music Concert", "Festival", "Conference", "Sports Event", "Comedy Show", "Theater"]
            )
            city = st.selectbox(
                "City",
                ["New York", "Los Angeles", "Chicago", "Miami", "Austin", "Seattle"]
            )
        with col2:
            capacity = st.number_input("Venue Capacity", min_value=100, max_value=50000, value=1000, step=100)
            ticket_price = st.number_input("Base Ticket Price ($)", min_value=10, max_value=500, value=50, step=5)
            date = st.date_input("Event Date", value=datetime.now() + timedelta(days=90))
        
        submit_button = st.form_submit_button("Generate Budget Estimate")
    
    if submit_button:
        # Create event data structure
        event_data = {
            'name': event_name,
            'category': event_type.split()[0],
            'location': city,
            'date': date.strftime('%Y-%m-%d'),
            'capacity': capacity,
            'base_price': ticket_price,
            'popularity_score': random.randint(60, 95),  # Mock data
            'trending_score': random.uniform(0.4, 0.9),  # Mock data
            'tickets_sold': int(capacity * 0.2)  # Assuming early stage with 20% tickets sold
        }
        
        # Generate predictions
        event_data['predicted_sales'] = predict_ticket_sales(event_data)
        event_data['optimal_price'] = get_optimal_price(event_data)
        
        # Generate budget estimate
        budget = generate_budget_estimate(event_data)
        
        # Display budget breakdown
        st.markdown("### Budget Breakdown")
        
        cost_col, revenue_col = st.columns(2)
        
        with cost_col:
            st.markdown("#### Estimated Costs")
            
            fig = go.Figure(go.Bar(
                x=['Venue', 'Artist', 'Staff', 'Marketing', 'Equipment', 'Insurance'],
                y=[budget['venue_cost'], budget['artist_cost'], budget['staff_cost'], 
                   budget['marketing_cost'], budget['equipment_cost'], budget['insurance_cost']],
                marker_color='indianred'
            ))
            
            fig.update_layout(title="Cost Breakdown")
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost table
            cost_data = {
                'Category': ['Venue Rental', 'Artist/Talent', 'Staff & Labor', 'Marketing', 'Equipment', 'Insurance', 'Total'],
                'Amount': [
                    f"${budget['venue_cost']:,}",
                    f"${budget['artist_cost']:,}",
                    f"${budget['staff_cost']:,}",
                    f"${budget['marketing_cost']:,}",
                    f"${budget['equipment_cost']:,}",
                    f"${budget['insurance_cost']:,}",
                    f"${budget['total_cost']:,}"
                ],
                'Percentage': [
                    f"{budget['venue_cost'] / budget['total_cost'] * 100:.1f}%",
                    f"{budget['artist_cost'] / budget['total_cost'] * 100:.1f}%",
                    f"{budget['staff_cost'] / budget['total_cost'] * 100:.1f}%",
                    f"{budget['marketing_cost'] / budget['total_cost'] * 100:.1f}%",
                    f"{budget['equipment_cost'] / budget['total_cost'] * 100:.1f}%",
                    f"{budget['insurance_cost'] / budget['total_cost'] * 100:.1f}%",
                    "100%"
                ]
            }
            
            st.table(pd.DataFrame(cost_data))
        
        with revenue_col:
            st.markdown("#### Projected Revenue & Profit")
            
            # Revenue projection chart
            sales_percentage = event_data['predicted_sales'] / capacity * 100
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = sales_percentage,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Projected Ticket Sales"},
                delta = {'reference': 75, 'increasing': {'color': 'green'}, 'decreasing': {'color': 'red'}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickformat': '.0f'},
                    'bar': {'color': "royalblue"},
                    'steps': [
                        {'range': [0, 50], 'color': 'lightgray'},
                        {'range': [50, 75], 'color': 'gray'},
                        {'range': [75, 100], 'color': 'darkgray'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
            # Revenue table
            revenue_data = {
                'Category': ['Expected Ticket Sales', 'Ticket Price', 'Total Revenue', 'Total Costs', 'Projected Profit', 'Profit Margin'],
                'Value': [
                    f"{event_data['predicted_sales']} of {capacity} ({sales_percentage:.1f}%)",
                    f"${ticket_price}",
                    f"${budget['expected_revenue']:,}",
                    f"${budget['total_cost']:,}",
                    f"${budget['expected_profit']:,}",
                    f"{budget['profit_margin']}%"
                ]
            }
            
            st.table(pd.DataFrame(revenue_data))
            
            # Profit indicator
            if budget['profit_margin'] > 20:
                st.success(f"✅ This event is projected to be highly profitable with a {budget['profit_margin']}% margin.")
            elif budget['profit_margin'] > 0:
                st.info(f"ℹ️ This event is projected to be profitable with a {budget['profit_margin']}% margin.")
            else:
                st.error(f"⚠️ This event is projected to lose money with a {budget['profit_margin']}% margin.")
        
        # Optimization suggestions
        st.markdown("### Optimization Suggestions")
        opt_col1, opt_col2 = st.columns(2)
        
        with opt_col1:
            st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
            st.markdown("#### 💰 Price Optimization")
            
            if event_data['optimal_price'] > ticket_price * 1.1:
                st.markdown(f"⬆️ **Consider increasing ticket price to ${event_data['optimal_price']}**")
                additional_revenue = (event_data['optimal_price'] - ticket_price) * event_data['predicted_sales']
                st.markdown(f"This could generate additional revenue of approximately **${additional_revenue:,.2f}**.")
                
                # Show impact on sales
                new_sales_estimate = int(event_data['predicted_sales'] * 0.9)  # Assuming 10% sales drop with higher price
                st.markdown(f"Estimated impact: Sales may decrease to {new_sales_estimate} tickets, but revenue would still increase.")
            
            elif event_data['optimal_price'] < ticket_price * 0.9:
                st.markdown(f"⬇️ **Consider decreasing ticket price to ${event_data['optimal_price']}**")
                st.markdown("A lower price point could attract more attendees and potentially increase overall revenue.")
                
                # Show impact on sales
                new_sales_estimate = int(event_data['predicted_sales'] * 1.2)  # Assuming 20% sales increase with lower price
                new_revenue = event_data['optimal_price'] * new_sales_estimate
                st.markdown(f"Estimated impact: Sales could increase to {new_sales_estimate} tickets with potential revenue of ${new_revenue:,.2f}.")
            
            else:
                st.markdown(f"✅ Your current price point of ${ticket_price} appears to be optimal.")
                st.markdown("It balances revenue maximization with expected attendance.")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with opt_col2:
            st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
            st.markdown("#### 📊 Cost Reduction Opportunities")
            
            # Identify highest cost categories
            cost_categories = ['venue_cost', 'artist_cost', 'staff_cost', 'marketing_cost', 'equipment_cost', 'insurance_cost']
            highest_cost = max(cost_categories, key=lambda x: budget[x])
            highest_cost_name = highest_cost.replace('_cost', '').capitalize()
            
            st.markdown(f"Your highest cost category is **{highest_cost_name}** at ${budget[highest_cost]:,}.")
            
            if highest_cost == 'venue_cost':
                st.markdown("Consider these options to reduce venue costs:")
                st.markdown("- Negotiate a multi-event contract with the venue")
                st.markdown("- Consider alternative venues with similar capacity")
                st.markdown("- Book on weekdays instead of weekends if possible")
            
            elif highest_cost == 'artist_cost':
                st.markdown("Consider these options to optimize artist/talent costs:")
                st.markdown("- Explore revenue sharing models with artists")
                st.markdown("- Package multiple similar artists together")
                st.markdown("- Consider up-and-coming talent with growing followings")
            
            elif highest_cost == 'marketing_cost':
                st.markdown("Consider these options to optimize marketing spend:")
                st.markdown("- Focus on organic social media and influencer partnerships")
                st.markdown("- Use targeted ads on platforms popular with your audience")
                st.markdown("- Create a referral program for existing ticket holders")
                
            # Show potential savings
            potential_savings = budget[highest_cost] * 0.15
            adjusted_profit = budget['expected_profit'] + potential_savings
            adjusted_margin = (adjusted_profit / budget['expected_revenue']) * 100
            
            st.markdown(f"A 15% reduction in {highest_cost_name} costs could save **${potential_savings:,.2f}** and increase profit margin to **{adjusted_margin:.1f}%**.")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Estimated timeline
        st.markdown("### Event Planning Timeline")
        
        days_until_event = (date - datetime.now().date()).days
        
        timeline_data = {
            'Task': [
                'Finalize venue contract',
                'Confirm talent/performers',
                'Order equipment',
                'Launch marketing campaign',
                'Begin ticket sales',
                'Hire staff',
                'Final logistics meeting',
                'Event day'
            ],
            'Days Before Event': [90, 75, 60, 60, 60, 30, 7, 0],
            'Status': ['Upcoming'] * 8
        }
        
        for i, days in enumerate(timeline_data['Days Before Event']):
            if days_until_event > days:
                timeline_data['Status'][i] = '✅ Complete'
            elif days_until_event == days:
                timeline_data['Status'][i] = '🔄 In Progress'
            else:
                timeline_data['Status'][i] = '⏳ Upcoming'
        
        timeline_df = pd.DataFrame(timeline_data)
        st.table(timeline_df)

elif app_mode == "Trend Analysis":
    st.markdown("<div class='main-header'>Industry Trend Analysis</div>", unsafe_allow_html=True)
    st.markdown("AI-powered insights into market trends and emerging opportunities")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        trend_category = st.selectbox(
            "Category",
            ["Music", "Sports", "Arts & Theater", "Food & Drink", "Tech", "Wellness"]
        )
    with col2:
        trend_location = st.selectbox(
            "Location",
            ["All Locations", "New York", "Los Angeles", "Chicago", "Miami", "Austin", "Seattle"]
        )
    with col3:
        trend_timeframe = st.selectbox(
            "Timeframe",
            ["Last 30 days", "Last 90 days", "Last 6 months", "Last year"]
        )
    
    st.markdown("---")
    
    # Generate sample data for trends
    def generate_trend_data(category, timeframe_days):
        artists = []
        
        if category == "Music":
            artists = ["Taylor Swift", "Bad Bunny", "The Weeknd", "Billie Eilish", "BTS", 
                       "Dua Lipa", "Kendrick Lamar", "Olivia Rodrigo", "Post Malone", "Harry Styles"]
        elif category == "Sports":
            artists = ["NBA Games", "NFL Games", "Soccer Matches", "Tennis Tournaments", "Golf Tournaments",
                       "Baseball Games", "Hockey Games", "Boxing Matches", "MMA Events", "College Sports"]
        elif category == "Arts & Theater":
            artists = ["Broadway Shows", "Art Exhibitions", "Dance Performances", "Comedy Shows", "Plays",
                       "Musicals", "Opera", "Symphony", "Film Festivals", "Cultural Festivals"]
        elif category == "Food & Drink":
            artists = ["Food Festivals", "Wine Tastings", "Beer Festivals", "Chef Events", "Cooking Classes",
                       "Farmers Markets", "Restaurant Weeks", "Cocktail Events", "Food Tours", "Pop-up Dinners"]
        elif category == "Tech":
            artists = ["Tech Conferences", "Hackathons", "Gaming Conventions", "Developer Meetups", "Startup Events",
                       "Tech Workshops", "Innovation Summits", "AI Conferences", "Blockchain Events", "Digital Summits"]
        else:
            artists = ["Yoga Retreats", "Fitness Challenges", "Meditation Workshops", "Wellness Conferences", "Health Expos",
                       "Running Events", "Mindfulness Retreats", "Nutrition Seminars", "Outdoor Activities", "Spa Events"]
        
        # Generate time series data for each artist
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(timeframe_days, 0, -1)]
        
        trend_data = []
        for artist in artists:
            # Base popularity
            base_popularity = random.randint(50, 90)
            
            # Add some randomness
            popularity_series = [max(10, min(100, base_popularity + random.randint(-10, 10))) for _ in dates]
            
            # Add trend for some artists
            if random.random() > 0.7:
                # Trending up
                for i in range(len(popularity_series)):
                    popularity_series[i] += int(i * 20 / len(popularity_series))
            elif random.random() > 0.7:
                # Trending down
                for i in range(len(popularity_series)):
                    popularity_series[i] -= int(i * 15 / len(popularity_series))
            
            # Cap values
            popularity_series = [max(10, min(100, p)) for p in popularity_series]
            
            for date, popularity in zip(dates, popularity_series):
                trend_data.append({
                    'date': date,
                    'artist': artist,
                    'popularity': popularity,
                    'searches': int(popularity * random.randint(50, 200)),
                    'ticket_demand': int(popularity * random.randint(30, 100))
                })
        
        return pd.DataFrame(trend_data)
    
    # Get trend data based on selections
    timeframe_days = {
        "Last 30 days": 30,
        "Last 90 days": 90,
        "Last 6 months": 180,
        "Last year": 365
    }[trend_timeframe]
    
    trend_df = generate_trend_data(trend_category, timeframe_days)
    
    # Calculate artist popularity over time
    pivot_df = trend_df.pivot_table(
        index='date', 
        columns='artist', 
        values='popularity', 
        aggfunc='mean'
    ).reset_index()
    
    # Convert date column to datetime
    pivot_df['date'] = pd.to_datetime(pivot_df['date'])
    pivot_df = pivot_df.sort_values('date')
    
    # Get the top trending artists (highest positive slope)
    slopes = {}
    for artist in pivot_df.columns[1:]:
        y = pivot_df[artist].values
        x = np.arange(len(y))
        slope, _, _, _, _ = np.polyfit(x, y, 1, full=True)
        slopes[artist] = slope[0]
    
    trending_artists = sorted(slopes.items(), key=lambda x: x[1], reverse=True)
    
    # Display popularity trends chart
    st.markdown("<div class='sub-header'>🔥 Popularity Trends</div>", unsafe_allow_html=True)
    
    fig = go.Figure()
    
    for artist in pivot_df.columns[1:]:
        fig.add_trace(go.Scatter(
            x=pivot_df['date'],
            y=pivot_df[artist],
            mode='lines',
            name=artist
        ))
    
    fig.update_layout(
        title=f"{trend_category} Popularity Trends ({trend_timeframe})",
        xaxis_title="Date",
        yaxis_title="Popularity Score",
        legend_title="Artists/Events",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Trending artists section
    st.markdown("<div class='sub-header'>📈 Most Trending</div>", unsafe_allow_html=True)
    
    trending_col1, trending_col2 = st.columns([1, 2])
    
    with trending_col1:
        top_5_trending = trending_artists[:5]
        st.markdown("### Fastest Rising")
        
        # Bar chart of trending slopes
        fig = go.Figure(go.Bar(
            x=[slope for _, slope in top_5_trending],
            y=[artist for artist, _ in top_5_trending],
            orientation='h',
            marker_color='lightgreen',
            text=[f"+{slope:.2f}/day" for _, slope in top_5_trending],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Daily Growth Rate",
            xaxis_title="Growth Rate",
            yaxis_title="Artist/Event",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Declining trends
        bottom_5_trending = trending_artists[-5:]
        bottom_5_trending.reverse()  # Show most declining first
        
        st.markdown("### Declining Interest")
        
        fig = go.Figure(go.Bar(
            x=[slope for _, slope in bottom_5_trending],
            y=[artist for artist, _ in bottom_5_trending],
            orientation='h',
            marker_color='salmon',
            text=[f"{slope:.2f}/day" for _, slope in bottom_5_trending],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Daily Decline Rate",
            xaxis_title="Decline Rate",
            yaxis_title="Artist/Event",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with trending_col2:
        # Get most popular artist currently
        last_day = pivot_df.iloc[-1].drop('date')
        current_popularity = last_day.sort_values(ascending=False)
        
        # Create heatmap of popularity over time
        pivot_df_for_heatmap = pivot_df.copy()
        pivot_df_for_heatmap['date'] = pivot_df_for_heatmap['date'].dt.strftime('%Y-%m-%d')
        pivot_df_for_heatmap = pivot_df_for_heatmap.set_index('date')
        
        # Select top artists only for clarity
        top_artists = current_popularity.index[:10]
        heatmap_df = pivot_df_for_heatmap[top_artists]
        
        # Downsample for cleaner display if many dates
        if len(heatmap_df) > 20:
            heatmap_df = heatmap_df.iloc[::len(heatmap_df) // 20 + 1]
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_df.values,
            x=heatmap_df.columns,
            y=heatmap_df.index,
            colorscale='Blues',
            colorbar=dict(title='Popularity')
        ))
        
        fig.update_layout(
            title="Popularity Heatmap Over Time",
            xaxis_title="Artist/Event",
            yaxis_title="Date",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Seasonal patterns section
    st.markdown("---")
    st.markdown("<div class='sub-header'>🗓️ Seasonal Patterns</div>", unsafe_allow_html=True)
    
    # Generate seasonal pattern data (in a real app, this would use historical data)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Different patterns for different categories
    pattern_data = {}
    
    if trend_category == "Music":
        pattern_data = {
            "Festivals": [50, 55, 65, 75, 85, 95, 100, 95, 85, 70, 60, 55],
            "Concerts": [80, 75, 70, 75, 85, 90, 85, 80, 90, 95, 90, 85],
            "DJ Events": [75, 80, 80, 70, 75, 90, 95, 100, 90, 85, 90, 95]
        }
    elif trend_category == "Sports":
        pattern_data = {
            "Baseball": [60, 65, 75, 90, 95, 100, 95, 90, 85, 80, 65, 60],
            "Basketball": [95, 100, 95, 90, 85, 70, 65, 60, 65, 75, 85, 90],
            "Football": [65, 60, 55, 50, 50, 55, 60, 75, 85, 95, 100, 90]
        }
    elif trend_category == "Arts & Theater":
        pattern_data = {
            "Theater": [85, 80, 85, 90, 95, 90, 85, 80, 85, 90, 95, 100],
            "Art Shows": [75, 80, 90, 95, 100, 95, 85, 80, 85, 90, 85, 80],
            "Film Festivals": [65, 70, 80, 90, 95, 100, 90, 85, 80, 75, 70, 65]
        }
    else:
        pattern_data = {
            "Conferences": [80, 85, 90, 95, 100, 90, 80, 75, 85, 90, 85, 75],
            "Workshops": [85, 90, 95, 100, 95, 90, 85, 80, 90, 95, 90, 85],
            "Expos": [75, 80, 85, 90, 95, 100, 90, 85, 90, 95, 90, 80]
        }
    
    # Create seasonal pattern chart
    fig = go.Figure()
    
    for event_type, values in pattern_data.items():
        fig.add_trace(go.Scatter(
            x=months,
            y=values,
            mode='lines+markers',
            name=event_type
        ))
    
    fig.update_layout(
        title=f"Seasonal Popularity Patterns for {trend_category}",
        xaxis_title="Month",
        yaxis_title="Relative Popularity",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Get current month index (0-based)
    current_month_idx = datetime.now().month - 1
    
    # Find best event types for current month
    current_month_popularity = {event: values[current_month_idx] for event, values in pattern_data.items()}
    best_events = sorted(current_month_popularity.items(), key=lambda x: x[1], reverse=True)
    
    # Create recommendation cards
    st.markdown("<div class='sub-header'>🔮 Event Recommendations</div>", unsafe_allow_html=True)
    
    rec_cols = st.columns(3)
    
    for i, (event_type, popularity) in enumerate(best_events):
        with rec_cols[i]:
            st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
            st.markdown(f"### {event_type}")
            
            current_month = months[current_month_idx]
            next_month = months[(current_month_idx + 1) % 12]
            
            current_pop = pattern_data[event_type][current_month_idx]
            next_pop = pattern_data[event_type][(current_month_idx + 1) % 12]
            
            trend = "rising" if next_pop > current_pop else "declining"
            icon = "📈" if next_pop > current_pop else "📉"
            
            st.markdown(f"**Current Popularity:** {current_pop}%")
            st.markdown(f"**Trend:** {icon} {trend.capitalize()} ({next_pop}% in {next_month})")
            
            # Generate event ideas
            st.markdown("#### Suggested Event Ideas:")
            for idea in generate_event_ideas(trend_location if trend_location != "All Locations" else "your city", trend_category)[:3]:
                st.markdown(f"- {idea}")
            
            # Best time to schedule
            best_month_idx = pattern_data[event_type].index(max(pattern_data[event_type]))
            best_month = months[best_month_idx]
            
            st.markdown(f"**Best timing:** {best_month}")
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Price sensitivity analysis
    st.markdown("---")
    st.markdown("<div class='sub-header'>💰 Price Sensitivity Analysis</div>", unsafe_allow_html=True)
    
    # Generate price elasticity data
    price_points = list(range(50, 251, 25))
    
    elasticity_data = {
        "Low Elasticity (Premium Events)": [100, 98, 95, 90, 87, 85, 83, 80, 78],
        "Medium Elasticity (Standard Events)": [100, 95, 88, 80, 72, 65, 58, 50, 42],
        "High Elasticity (Value Events)": [100, 90, 78, 65, 52, 40, 30, 22, 15]
    }
    
    # Calculate revenue index (price * demand)
    revenue_data = {}
    for category, demand in elasticity_data.items():
        revenue = [price * dem / 100 for price, dem in zip(price_points, demand)]
        # Normalize to make the first point = 100
        revenue = [rev * 100 / revenue[0] for rev in revenue]
        revenue_data[category] = revenue
    
    # Find optimal price points
    optimal_prices = {}
    for category, revenue in revenue_data.items():
        optimal_idx = revenue.index(max(revenue))
        optimal_prices[category] = price_points[optimal_idx]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Demand elasticity chart
        fig = go.Figure()
        
        for category, demand in elasticity_data.items():
            fig.add_trace(go.Scatter(
                x=price_points,
                y=demand,
                mode='lines+markers',
                name=category
            ))
        
        fig.update_layout(
            title="Price Sensitivity by Event Type",
            xaxis_title="Ticket Price ($)",
            yaxis_title="Relative Demand (%)",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue optimization chart
        fig = go.Figure()
        
        for category, revenue in revenue_data.items():
            optimal_price = optimal_prices[category]
            
            fig.add_trace(go.Scatter(
                x=price_points,
                y=revenue,
                mode='lines+markers',
                name=category
            ))
            
            # Add marker for optimal price
            optimal_idx = price_points.index(optimal_price)
            fig.add_trace(go.Scatter(
                x=[optimal_price],
                y=[revenue[optimal_idx]],
                mode='markers',
                marker=dict(size=12, color='red', symbol='star'),
                name=f"{category} Optimal",
                showlegend=False
            ))
            
            # Add annotation for optimal price
            fig.add_annotation(
                x=optimal_price,
                y=revenue[optimal_idx],
                text=f"${optimal_price}",
                showarrow=True,
                arrowhead=1
            )
        
        fig.update_layout(
            title="Revenue Optimization by Price Point",
            xaxis_title="Ticket Price ($)",
            yaxis_title="Relative Revenue (%)",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Pricing recommendations
    st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
    st.markdown("### 🏷️ Pricing Strategy Recommendations")
    
    st.markdown(f"Based on the analysis for {trend_category} events:")

    for category, optimal_price in optimal_prices.items():
        event_type = category.split("(")[1].replace(")", "")
        st.markdown(f"- **{event_type}**: Optimal price point is **${optimal_price}**")
        
        if "Premium" in event_type:
            st.markdown("  - These events have low price sensitivity - quality and exclusivity drive demand")
            st.markdown("  - Focus on value-added experiences like VIP packages and premium amenities")
        elif "Standard" in event_type:
            st.markdown("  - These events have moderate price sensitivity - balance price and quality")
            st.markdown("  - Consider tiered pricing strategies and early bird discounts")
        else:
            st.markdown("  - These events have high price sensitivity - price is a key decision factor")


def main():
    st.title("TufanTicket - AI Event Platform")
    
    # Sidebar navigation
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choose a page:", ["Home", "Event Analytics", "Budget Estimation", "Social Sentiment", "Event Ideas"])
    
    if page == "Home":
        st.header("Welcome to TufanTicket!")
        st.write("Use this platform to manage and analyze your events with AI-powered tools.")
    
    elif page == "Event Analytics":
        st.header("Event Analytics")
        category = st.selectbox("Select Event Category:", ["Music", "Sports", "Arts & Theater", "Food & Drink", "Tech", "Wellness"])
        location = st.text_input("Enter Location:")
        date_range = st.date_input("Select Date Range:", [])
        
        if st.button("Fetch Events"):
            events = fetch_events_api(category, location, date_range)
            st.write(events)
    
    elif page == "Budget Estimation":
        st.header("Budget Estimation")
        event_data = {
            'capacity': st.number_input("Enter Event Capacity:", min_value=100, max_value=50000, step=100),
            'base_price': st.number_input("Enter Base Ticket Price:", min_value=10, max_value=500, step=5),
            'popularity_score': st.slider("Popularity Score:", 0, 100),
            'trending_score': st.slider("Trending Score:", 0.0, 1.0)
        }
        
        if st.button("Generate Budget Estimate"):
            budget = generate_budget_estimate(event_data)
            st.write(budget)
    
    elif page == "Social Sentiment":
        st.header("Social Sentiment Analysis")
        keyword = st.text_input("Enter Keyword for Sentiment Analysis:")
        
        if st.button("Fetch Sentiment"):
            sentiment_data = fetch_social_sentiment(keyword)
            st.write(sentiment_data)
    
    elif page == "Event Ideas":
        st.header("Event Ideas Generator")
        location = st.text_input("Enter Location:")
        category = st.selectbox("Select Event Category:", ["Music", "Sports", "Arts & Theater", "Tech", "Food & Drink"])
        
        if st.button("Generate Ideas"):
            ideas = generate_event_ideas(location, category)
            for idea in ideas:
                st.write(idea)

# Run the app
if __name__ == "__main__":
    main()            
