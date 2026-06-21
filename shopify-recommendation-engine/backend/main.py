from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.recommendations import router
from backend.models.recommender import recommender

app = FastAPI(
    title="Shopify Product Recommendation Engine",
    description="Hybrid collaborative + content-based recommender for e-commerce.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def startup():
    recommender.load_and_train()


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}
