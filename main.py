from typing import Union
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing_extensions import Annotated

app = FastAPI()

products_db = [
    {"id": 1, "name": "Laptop", "price": 1000.0},
    {"id": 2, "name": "Smartphone", "price": 500.0}
]

@app.get("/")
async def root():# endpoint
  return {"message": "Welcome to the e-commerce API!"}

@app.get("/products")
async def get_products():
  return {"products": products_db}


class Product(BaseModel):
  name: str = Field(
    title="The name of the product", 
    min_length=3, 
    max_length=20)
  price: float
  description: Union[str, None] = None

@app.post("/products")
async def add_product(product: Product):
  name = product.name
  price = product.price
  description = product.description
  id = len(products_db) + 1
  
  products_db.append({"id": id, "name": name, "price": price, "description": description})
  
  return {"message": "Product added successfully", "product": product}


def find_product_by_id(product_id):
    for product in products_db:
        if product["id"] == product_id:
            return product
    return None

@app.put("/products/{product_id}")
async def get_product(product_id: int):
  product = find_product_by_id(product_id)
  
  if product is not None:
    return {"message": "Product retrieved succesfully", "product": product}
  else:
    return {"message": "Product not found"}
  
# /search?search_query=laptop&min_price=50
@app.get('/search')
async def search_product(search_query: Annotated[Union[str, None], Query(min_length=3)] = None, min_price: Annotated[Union[float, None], Query(ge=0)] = None):
  if search_query:
    search_results = [product for product in products_db if search_query.lower() in product["name"].lower()]
    
  else:
    search_results = products_db
  
  if min_price:
    search_results = [product for product in search_results if product["price"] >= min_price]
    
  return {"search_results": search_results}