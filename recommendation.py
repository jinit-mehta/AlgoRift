import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time
from multiprocessing import Pool, cpu_count

# Configuration
MAX_FRIENDS = 20
TOP_K_SIMILAR_USERS = 10
LOCATION_WEIGHT = 0.3
CHUNK_SIZE = 10000  # Process data in chunks to avoid memory overload

def recommend_events_simplified(user_id, train_df, events_df, users_df, user_friends_df, num_recommendations=5):
    """
    Simplified recommendation function with optimizations.
    """
    user_id = str(user_id)
    print(f"Generating recommendations for user {user_id}")

    # 1. Get events the user has already interacted with
    user_events = set(train_df[train_df['user'] == user_id]['event'].astype(str))
    if not user_events:
        print(f"User {user_id} has no event interactions")

    # 2. Get user's location
    user_location = None
    if user_id in users_df['user_id'].astype(str).values:
        user_location = users_df[users_df['user_id'].astype(str) == user_id]['location'].iloc[0]
        if pd.isna(user_location) or user_location == '':
            user_location = None

    # 3. Get user's friends
    user_friends = []
    if user_id in user_friends_df['user'].astype(str).values:
        friends_row = user_friends_df[user_friends_df['user'].astype(str) == user_id]['friends'].iloc[0]
        if isinstance(friends_row, str) and friends_row.strip():
            user_friends = friends_row.split()[:MAX_FRIENDS]

    # Create a scoring dictionary for candidate events
    event_scores = {}

    # 4. Score events based on friends' attendance
    if user_friends:
        friend_events = train_df[
            (train_df['user'].astype(str).isin(user_friends)) &
            (train_df['interested'] == 1)
        ]['event'].astype(str)

        for event, count in friend_events.value_counts().items():
            if event not in user_events:  # Don't recommend events user already interacted with
                # Higher score for events more friends attended
                event_scores[event] = event_scores.get(event, 0) + (count / len(user_friends)) * 0.6

    # 5. Score events based on location match
    if user_location and not pd.isna(user_location):
        user_location_lower = user_location.lower()

        # Process events in chunks
        for i in range(0, len(events_df), CHUNK_SIZE):
            events_chunk = events_df.iloc[i:i+CHUNK_SIZE]

            for _, event in events_chunk.iterrows():
                event_id = str(event['event_id'])

                # Skip events user already interacted with
                if event_id in user_events:
                    continue

                # Check for location match
                event_city = str(event['city']).lower() if not pd.isna(event['city']) else ""
                event_country = str(event['country']).lower() if not pd.isna(event['country']) else ""

                location_score = 0
                if event_city and event_city in user_location_lower:
                    location_score = 0.8
                elif event_country and event_country in user_location_lower:
                    location_score = 0.4

                if location_score > 0:
                    event_scores[event_id] = event_scores.get(event_id, 0) + location_score * LOCATION_WEIGHT

    # 6. Add a simple collaborative filtering component
    if len(user_events) > 0:
        # Get users who attended the same events
        similar_users = train_df[
            (train_df['event'].astype(str).isin(user_events)) &
            (train_df['interested'] == 1) &
            (train_df['user'].astype(str) != user_id)
        ]['user'].astype(str)

        # Count event overlap to find most similar users
        similar_user_counts = similar_users.value_counts().head(TOP_K_SIMILAR_USERS)

        # For each similar user, find events they liked
        for similar_user, count in similar_user_counts.items():
            similarity = count / len(user_events)  # Simple similarity score

            # Get events the similar user liked
            similar_user_events = train_df[
                (train_df['user'].astype(str) == similar_user) &
                (train_df['interested'] == 1)
            ]['event'].astype(str)

            # Score events from similar users
            for event in similar_user_events:
                if event not in user_events:
                    event_scores[event] = event_scores.get(event, 0) + similarity * 0.5

    # Convert scores to DataFrame and sort
    if not event_scores:
        print("No recommendations found")
        return pd.DataFrame(columns=['event_id', 'score'])

    recommendations = pd.DataFrame({
        'event_id': list(event_scores.keys()),
        'score': list(event_scores.values())
    })

    # Sort and take top recommendations
    recommendations = recommendations.sort_values('score', ascending=False).head(num_recommendations)

    return recommendations

def generate_recommendations_batch(user_ids, train_df, events_df, users_df, user_friends_df, num_recommendations=5):
    """Generate recommendations for a batch of users in parallel"""
    all_recommendations = []

    # Use multiprocessing to parallelize recommendations
    with Pool(cpu_count()) as pool:
        results = pool.starmap(
            recommend_events_simplified,
            [(user_id, train_df, events_df, users_df, user_friends_df, num_recommendations) for user_id in user_ids]
        )

    # Combine results
    for recs in results:
        if not recs.empty:
            recs['user_id'] = user_id
            all_recommendations.append(recs)

    if all_recommendations:
        final_recommendations = pd.concat(all_recommendations, ignore_index=True)
        final_recommendations = final_recommendations[['user_id', 'event_id', 'score']]
        return final_recommendations
    else:
        return pd.DataFrame(columns=['user_id', 'event_id', 'score'])

# Main function to run the recommendation system
def run_simple_recommendation_system():
    print("Running simplified recommendation system")

    print("Loading data...")
    # Load data with optimized approach
    events_cols = ['event_id', 'city', 'country']
    users_cols = ['user_id', 'location']
    user_friends_cols = ['user', 'friends']
    train_cols = ['user', 'event', 'interested']

    # Load the data with only needed columns
    events = pd.read_csv("/content/drive/MyDrive/d2k/events.csv", usecols=events_cols)
    users = pd.read_csv("/content/drive/MyDrive/d2k/users.csv", usecols=users_cols)
    user_friends = pd.read_csv("/content/drive/MyDrive/d2k/user_friends.csv", usecols=user_friends_cols)
    train = pd.read_csv("/content/drive/MyDrive/d2k/train.csv", usecols=train_cols)

    # Convert IDs to string for consistency
    events['event_id'] = events['event_id'].astype(str)
    users['user_id'] = users['user_id'].astype(str)
    train['user'] = train['user'].astype(str)
    train['event'] = train['event'].astype(str)
    user_friends['user'] = user_friends['user'].astype(str)

    # Generate recommendations for a small sample of users
    sample_users = train['user'].unique()[:50]  # Take just 50 users for quick testing

    print(f"Generating recommendations for {len(sample_users)} users")
    recommendations = generate_recommendations_batch(
        sample_users, train, events, users, user_friends
    )

    print(f"Generated {len(recommendations)} recommendations for {recommendations['user_id'].nunique()} users")
    print(recommendations.head())

    # Optionally save to CSV
    recommendations.to_csv("simple_recommendations.csv", index=False)

    return recommendations

if __name__ == "__main__":
    run_simple_recommendation_system()