from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(title="TastyTrails FastAPI", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to TastyTrails FastAPI Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fastapi"}

# Search endpoints
@app.get("/api/search/restaurants")
async def search_restaurants(query: Optional[str] = None):
    # Placeholder for search functionality
    return {"message": f"Searching for restaurants with query: {query}", "results": []}

# Recommendation endpoints
@app.get("/api/recommendations")
async def get_recommendations(user_id: Optional[int] = None):
    # Placeholder for recommendation functionality
    return {"message": f"Getting recommendations for user: {user_id}", "recommendations": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)