# Shopify Product Recommendation Engine

A hybrid product recommendation system combining **collaborative filtering** and **content-based filtering** — inspired by the kind of ML infrastructure used at Shopify to personalise merchant storefronts.

## What it does

- Analyses purchase patterns across 200 simulated customers and 15 products
- Generates personalised product recommendations for any item in the catalogue
- Lets you adjust the algorithm mix in real time via an interactive slider
- Exposes a clean REST API ready to be wired into a Shopify storefront or App

## How it works

```
User clicks a product
        ↓
FastAPI backend receives product_id
        ↓
┌─────────────────────────────────────┐
│  Collaborative Filtering (alpha)    │  ← "customers who bought X also bought..."
│  item-item cosine similarity        │
├─────────────────────────────────────┤
│  Content-Based Filtering (1-alpha)  │  ← "similar category, tags, price range"
│  tag + category one-hot encoding    │
└─────────────────────────────────────┘
        ↓
 Weighted score → top-N results
        ↓
React frontend renders recommendation cards
```

## Tech stack

| Layer    | Technology |
|----------|-----------|
| ML model | scikit-learn (cosine similarity), pandas, numpy |
| Backend  | FastAPI + uvicorn |
| Frontend | React (vanilla, no bundler needed) |
| Data     | Synthetic e-commerce dataset (200 users, 15 products, 1 122 interactions) |

## Quick start

```bash
# 1. Clone
git clone https://github.com/emiryldm19/shopify-recommendation-engine
cd shopify-recommendation-engine

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Generate the dataset
python backend/data/generate_data.py

# 4. Start the API
uvicorn backend.main:app --reload
# → API running at http://localhost:8000
# → Interactive docs at http://localhost:8000/docs

# 5. Open the frontend
open frontend/index.html
# or just drag it into your browser
```

## API reference

| Endpoint | Description |
|----------|-------------|
| `GET /api/products` | All products |
| `GET /api/recommend/{product_id}?n=4&alpha=0.6` | Top-n recommendations |
| `GET /api/stats` | Dataset statistics |
| `GET /docs` | Auto-generated Swagger UI |

### Example

```bash
curl http://localhost:8000/api/recommend/1?n=4&alpha=0.6
```

```json
{
  "source_product": { "id": 1, "title": "Wireless Noise-Cancelling Headphones", ... },
  "recommendations": [
    { "id": 15, "title": "Blue Light Blocking Glasses", "score": 0.4036, ... },
    { "id": 8,  "title": "USB-C Hub 7-in-1",            "score": 0.3975, ... }
  ],
  "config": { "n": 4, "alpha": 0.6 }
}
```

## Project structure

```
shopify-recommendation-engine/
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── models/
│   │   └── recommender.py       # Hybrid ML model
│   ├── routers/
│   │   └── recommendations.py   # API routes
│   └── data/
│       ├── generate_data.py     # Synthetic dataset generator
│       ├── interactions.csv     # Generated purchase data
│       └── products.json        # Product catalogue
├── frontend/
│   └── index.html               # React UI (single file, no bundler)
├── requirements.txt
└── README.md
```

## What I learned / would extend next

- **Real Shopify data**: replace the synthetic dataset with the Shopify Admin API to pull real order history
- **Matrix factorisation**: upgrade from item-item cosine to SVD or ALS for better accuracy at scale
- **A/B testing**: track click-through rate on recommended vs non-recommended products
- **Shopify App integration**: embed the API as a Shopify App using Shopify CLI + Polaris UI

## Author

Built as a portfolio project targeting ML Engineering and Full-Stack roles.
