import pandas as pd
import numpy as np
import json
import random

random.seed(42)
np.random.seed(42)

PRODUCTS = [
    {"id": 1,  "title": "Wireless Noise-Cancelling Headphones", "category": "Electronics", "price": 89.99,  "tags": ["audio", "wireless", "premium"]},
    {"id": 2,  "title": "Yoga Mat - Extra Thick",               "category": "Sports",      "price": 34.99,  "tags": ["yoga", "fitness", "wellness"]},
    {"id": 3,  "title": "Stainless Steel Water Bottle",         "category": "Sports",      "price": 24.99,  "tags": ["hydration", "eco", "fitness"]},
    {"id": 4,  "title": "Organic Green Tea (50 bags)",          "category": "Food",        "price": 14.99,  "tags": ["tea", "organic", "wellness"]},
    {"id": 5,  "title": "Mechanical Keyboard - TKL",            "category": "Electronics", "price": 129.99, "tags": ["keyboard", "gaming", "productivity"]},
    {"id": 6,  "title": "Resistance Bands Set",                 "category": "Sports",      "price": 19.99,  "tags": ["fitness", "home-gym", "strength"]},
    {"id": 7,  "title": "Bamboo Cutting Board",                 "category": "Kitchen",     "price": 29.99,  "tags": ["eco", "kitchen", "cooking"]},
    {"id": 8,  "title": "USB-C Hub 7-in-1",                    "category": "Electronics", "price": 49.99,  "tags": ["productivity", "usb", "accessories"]},
    {"id": 9,  "title": "Essential Oil Diffuser",               "category": "Home",        "price": 39.99,  "tags": ["wellness", "aromatherapy", "home"]},
    {"id": 10, "title": "Running Shoes - Lightweight",          "category": "Sports",      "price": 119.99, "tags": ["running", "fitness", "footwear"]},
    {"id": 11, "title": "Pour Over Coffee Maker",               "category": "Kitchen",     "price": 44.99,  "tags": ["coffee", "kitchen", "morning"]},
    {"id": 12, "title": "Laptop Stand - Adjustable",            "category": "Electronics", "price": 59.99,  "tags": ["productivity", "ergonomic", "desk"]},
    {"id": 13, "title": "Foam Roller - Deep Tissue",            "category": "Sports",      "price": 27.99,  "tags": ["recovery", "fitness", "massage"]},
    {"id": 14, "title": "Reusable Grocery Bags (5 pack)",       "category": "Home",        "price": 12.99,  "tags": ["eco", "grocery", "sustainable"]},
    {"id": 15, "title": "Blue Light Blocking Glasses",          "category": "Electronics", "price": 24.99,  "tags": ["productivity", "health", "screen"]},
]

# Define customer personas (clusters of buying behaviour)
PERSONAS = {
    "fitness_enthusiast": [2, 3, 6, 10, 13],
    "tech_worker":        [1, 5, 8, 12, 15],
    "wellness_seeker":    [2, 4, 6, 9, 14],
    "home_cook":          [7, 11, 14, 4, 3],
    "casual_shopper":     [3, 14, 4, 9, 7],
}

NUM_USERS = 200
rows = []

for user_id in range(1, NUM_USERS + 1):
    persona_name = random.choice(list(PERSONAS.keys()))
    core_products = PERSONAS[persona_name]

    # Buy most core products
    for pid in core_products:
        if random.random() < 0.75:
            rows.append({"user_id": user_id, "product_id": pid, "rating": random.randint(3, 5)})

    # Buy 1-3 random products
    extras = random.sample([p["id"] for p in PRODUCTS if p["id"] not in core_products], k=random.randint(1, 3))
    for pid in extras:
        rows.append({"user_id": user_id, "product_id": pid, "rating": random.randint(1, 4)})

df = pd.DataFrame(rows).drop_duplicates(subset=["user_id", "product_id"])
df.to_csv("/home/claude/shopify-recommendation-engine/backend/data/interactions.csv", index=False)

with open("/home/claude/shopify-recommendation-engine/backend/data/products.json", "w") as f:
    json.dump(PRODUCTS, f, indent=2)

print(f"Generated {len(df)} interactions for {NUM_USERS} users across {len(PRODUCTS)} products.")
