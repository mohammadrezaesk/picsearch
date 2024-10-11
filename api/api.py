from fastapi import FastAPI

from services import products_fetch_service
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    # "http://localhost",
    # "http://localhost:5173",
    # "http://localhost:8080",
    "*"  # do not do this in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
def read_root(query: str = "", mode: str = "all"):
    products = products_fetch_service.get_products(query, mode)
    return {"products": products}
