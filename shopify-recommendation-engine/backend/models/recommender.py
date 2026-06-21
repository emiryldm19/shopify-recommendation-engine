import pandas as pd
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


class HybridRecommender:
    """
    Hybrid recommender: collaborative filtering (user-item matrix)
    + content-based filtering (product tags/category).
    """

    def __init__(self):
        self.interactions = None
        self.products = None
        self.user_item_matrix = None
        self.item_similarity = None
        self.content_similarity = None
        self.product_map = {}   # id -> product dict
        self.is_trained = False

    def load_and_train(self):
        # Load data
        self.interactions = pd.read_csv(DATA_DIR / "interactions.csv")
        with open(DATA_DIR / "products.json") as f:
            self.products = json.load(f)
        self.product_map = {p["id"]: p for p in self.products}

        # --- Collaborative filtering: item-item cosine similarity ---
        self.user_item_matrix = self.interactions.pivot_table(
            index="user_id", columns="product_id", values="rating"
        ).fillna(0)

        self.item_similarity = pd.DataFrame(
            cosine_similarity(self.user_item_matrix.T),
            index=self.user_item_matrix.columns,
            columns=self.user_item_matrix.columns,
        )

        # --- Content-based: tag + category one-hot encoding ---
        all_tags = set(tag for p in self.products for tag in p["tags"])
        all_cats = set(p["category"] for p in self.products)
        features = sorted(all_tags) + sorted(all_cats)

        content_matrix = []
        for p in self.products:
            row = [1 if f in p["tags"] or f == p["category"] else 0 for f in features]
            content_matrix.append(row)

        content_array = np.array(content_matrix, dtype=float)
        sim = cosine_similarity(content_array)
        ids = [p["id"] for p in self.products]
        self.content_similarity = pd.DataFrame(sim, index=ids, columns=ids)

        self.is_trained = True
        print("Model trained.")

    def recommend(self, product_id: int, n: int = 5, alpha: float = 0.6) -> list[dict]:
        """
        Return top-n recommendations for a given product.
        alpha: weight for collaborative score (1-alpha for content score).
        """
        if not self.is_trained:
            self.load_and_train()

        if product_id not in self.product_map:
            return []

        # Collaborative scores
        cf_scores = (
            self.item_similarity[product_id]
            if product_id in self.item_similarity.columns
            else pd.Series(0, index=[p["id"] for p in self.products])
        )

        # Content scores
        cb_scores = (
            self.content_similarity[product_id]
            if product_id in self.content_similarity.columns
            else pd.Series(0, index=[p["id"] for p in self.products])
        )

        # Normalise each to [0,1]
        def norm(s):
            mn, mx = s.min(), s.max()
            return (s - mn) / (mx - mn + 1e-9)

        combined = alpha * norm(cf_scores) + (1 - alpha) * norm(cb_scores)
        combined = combined.drop(index=product_id, errors="ignore")
        top_ids = combined.nlargest(n).index.tolist()

        results = []
        for pid in top_ids:
            p = self.product_map[pid]
            score = round(float(combined[pid]), 4)
            results.append({**p, "score": score})
        return results

    def get_all_products(self) -> list[dict]:
        if not self.products:
            with open(DATA_DIR / "products.json") as f:
                self.products = json.load(f)
            self.product_map = {p["id"]: p for p in self.products}
        return self.products

    def get_stats(self) -> dict:
        if not self.is_trained:
            return {}
        return {
            "total_users": int(self.interactions["user_id"].nunique()),
            "total_products": len(self.products),
            "total_interactions": len(self.interactions),
            "avg_rating": round(float(self.interactions["rating"].mean()), 2),
        }


# Singleton instance
recommender = HybridRecommender()
