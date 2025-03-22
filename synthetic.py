import pandas as pd
import numpy as np
from faker import Faker
import os
from random import randint, choice, sample
from multiprocessing import Pool

fake = Faker()

# Constants
NUM_USERS, NUM_EVENTS, NUM_ORGANIZERS = 7000, 1000, 1000
CITIES = {
    "New York": "United States", "London": "United Kingdom", "Tokyo": "Japan", "Sydney": "Australia",
    "Paris": "France", "Berlin": "Germany", "Toronto": "Canada", "Mumbai": "India", "São Paulo": "Brazil",
    "Cape Town": "South Africa", "Los Angeles": "United States", "Shanghai": "China", "Singapore": "Singapore",
    "Dubai": "United Arab Emirates", "Moscow": "Russia", "Mexico City": "Mexico", "Bangkok": "Thailand",
    "Istanbul": "Turkey", "Seoul": "South Korea", "Madrid": "Spain"
}
CATEGORIES = ["Music", "Sports", "Workshops", "Theater", "Comedy", "Art", "Tech", "Food", "Film", "Literature"]
TYPES = ["Concert", "Match", "Seminar", "Play", "Show", "Exhibition", "Conference", "Tasting", "Screening", "Reading"]

def generate_users():
    user_ids = [f"U{i:04d}" for i in range(1, NUM_USERS + 1)]
    # Distribute users evenly across cities
    cities_per_user = np.array(list(CITIES.keys()) * (NUM_USERS // len(CITIES) + 1))[:NUM_USERS]
    np.random.shuffle(cities_per_user)
    return pd.DataFrame({
        "user_id": user_ids,
        "name": [fake.name() for _ in range(NUM_USERS)],
        "age": np.random.randint(18, 66, NUM_USERS),
        "location": [f"{city}, {CITIES[city]}" for city in cities_per_user],
        "preferences": [sample(CATEGORIES, randint(1, 3)) for _ in range(NUM_USERS)],
        "attended_events": [[] for _ in range(NUM_USERS)],
        "social_connections": [sample([uid for uid in user_ids if uid != uid_i], randint(5, 20)) for uid_i in user_ids],
        "exploration_score": np.round(np.random.uniform(0, 1, NUM_USERS), 2)
    })

def generate_events():
    categories = np.random.choice(CATEGORIES, NUM_EVENTS)
    # Distribute events evenly across cities
    cities_per_event = np.array(list(CITIES.keys()) * (NUM_EVENTS // len(CITIES) + 1))[:NUM_EVENTS]
    np.random.shuffle(cities_per_event)
    dates = [fake.date_between(start_date="-1y", end_date="today") if i < NUM_EVENTS // 2 
             else fake.date_between(start_date="today", end_date="+1y") for i in range(NUM_EVENTS)]
    return pd.DataFrame({
        "event_id": [f"E{i:04d}" for i in range(1, NUM_EVENTS + 1)],
        "name": [f"{fake.word().capitalize()} {cat} Event" for cat in categories],
        "type": np.random.choice(TYPES, NUM_EVENTS),
        "category": categories,
        "location": [f"{city}, {CITIES[city]}" for city in cities_per_event],
        "date": pd.to_datetime(dates),
        "time": [fake.time() for _ in range(NUM_EVENTS)],
        "ticket_price": np.round(np.random.uniform(10, 200, NUM_EVENTS), 2),
        "artist": [fake.name() if cat == "Music" else None for cat in categories],
        "popularity_score": np.round(np.random.uniform(0, 1, NUM_EVENTS), 2)
    })

def generate_bookings_for_event(args):
    event_id, ticket_price, event_category, event_date, event_city, users_df = args
    num_attendees = randint(200, 600)
    # Prefer users from the same city, with some from other cities
    same_city_users = users_df[users_df["location"].str.startswith(event_city)]
    other_city_users = users_df[~users_df["location"].str.startswith(event_city)]
    sampled_users = pd.concat([
        same_city_users.sample(min(len(same_city_users), int(num_attendees * 0.7)), replace=True),
        other_city_users.sample(num_attendees - min(len(same_city_users), int(num_attendees * 0.7)), replace=True)
    ]).sample(num_attendees, replace=True)
    
    ticket_quantities = np.random.randint(1, 5, num_attendees)
    match = sampled_users["preferences"].apply(lambda x: event_category in x)
    interested = np.where(match, 
                          np.random.choice([1, 1, 1, 1, 0], num_attendees),  # 80% chance of 1 if match
                          np.random.choice([0, 0, 0, 0, 1], num_attendees))  # 20% chance of 1 if no match
    
    return pd.DataFrame({
        "booking_id": [f"B{i:06d}" for i in range(num_attendees)],  # Temporary
        "user_id": sampled_users["user_id"].values,
        "event_id": event_id,
        "booking_date": [fake.date_between(start_date="-1y", end_date=event_date) for _ in range(num_attendees)],
        "ticket_quantity": ticket_quantities,
        "total_price": ticket_quantities * ticket_price,
        "interested": interested,
        "rating": [randint(1, 5) if i == 1 and choice([True, False]) else None for i in interested]
    })

def generate_bookings(users_df, events_df):
    past_events = events_df[events_df["date"] <= pd.Timestamp("today")]
    event_args = [(e["event_id"], e["ticket_price"], e["category"], e["date"], 
                   e["location"].split(",")[0].strip(), users_df) for _, e in past_events.iterrows()]
    
    with Pool() as pool:
        bookings_dfs = pool.map(generate_bookings_for_event, event_args)
    
    bookings_df = pd.concat(bookings_dfs, ignore_index=True)
    bookings_df["booking_id"] = [f"B{i:06d}" for i in range(1, len(bookings_df) + 1)]
    
    # Update attended_events
    attended_events = bookings_df.groupby("user_id")["event_id"].apply(list).to_dict()
    users_df["attended_events"] = users_df["user_id"].map(lambda x: attended_events.get(x, []))
    
    return bookings_df

def generate_organizers(events_df):
    return pd.DataFrame({
        "organizer_id": [f"O{i:04d}" for i in range(1, NUM_ORGANIZERS + 1)],
        "name": [fake.company() for _ in range(NUM_ORGANIZERS)],
        "event_id": events_df["event_id"].values,
        "ticket_sales": np.random.randint(1000, 50000, NUM_ORGANIZERS),
        "pricing_strategy": np.random.choice(["Low", "Medium", "High"], NUM_ORGANIZERS),
        "feedback_score": np.round(np.random.uniform(1, 5, NUM_ORGANIZERS), 2)
    })

def save_data():
    print("Generating users..."); users_df = generate_users()
    print("Generating events..."); events_df = generate_events()
    print("Generating bookings..."); bookings_df = generate_bookings(users_df, events_df)
    print("Generating organizers..."); organizers_df = generate_organizers(events_df)
    
    os.makedirs("data", exist_ok=True)
    print("Saving to CSV...")
    users_df.to_csv("data/users.csv", index=False)
    events_df.to_csv("data/events.csv", index=False)
    bookings_df.to_csv("data/bookings.csv", index=False)
    organizers_df.to_csv("data/organizers.csv", index=False)
    print("Data generated and saved.")

if __name__ == "__main__":
    save_data()