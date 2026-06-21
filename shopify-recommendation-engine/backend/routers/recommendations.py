from fastapi import APIRouter, HTTPException, Query
from backend.models.recommender import recommender

router = APIRouter(prefix="/api", tags=["recommendations"])


@router.get("/products")
def get_products():
    """Return all products."""
    return recommender.get_all_products()


@router.get("/recommend/{product_id}")
def get_recommendations(
    product_id: int,
    n: int = Query(default=4, ge=1, le=10),
    alpha: float = Query(default=0.6, ge=0.0, le=1.0),
):
    """
    Return top-n recommendations for a given product.
    - alpha=1.0  → pure collaborative filtering
    - alpha=0.0  → pure content-based
    - alpha=0.6  → hybrid (default)
    """
    if not recommender.is_trained:
        recommender.load_and_train()

    results = recommender.recommend(product_id, n=n, alpha=alpha)
    if not results:
        raise HTTPException(status_code=404, detail="Product not found")

    source_product = recommender.product_map.get(product_id)
    return {
        "source_product": source_product,
        "recommendations": results,
        "config": {"n": n, "alpha": alpha},
    }


@router.get("/stats")
def get_stats():
    """Dataset statistics."""
    if not recommender.is_trained:
        recommender.load_and_train()
    return recommender.get_stats()
