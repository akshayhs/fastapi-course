import logging

from fastapi import Form, FastAPI, Response, status
from faker import Faker
from pydantic import BaseModel, Field
from random import randint
from typing import Optional

app = FastAPI()
faker = Faker()

logger = logging.getLogger(__name__)


class Book(BaseModel):
	"""A Python class that models data related to a book"""
	id: int
	title: str = Field(title="Title of the book", min_length=3, max_length=55, description="Enter the title of the book")
	author: str = Field(title="Author of the book",min_length=5, max_length=55)
	description: Optional[str] = Field(title="Description of the book",min_length=10, max_length=300)
	rating: int = Field(le=10, gt=0)

	class Config:
	 	json_schema_extra = {
		 "example": {
			"id": randint(1, 100),
			"title": faker.bs(),
			"author": f"{faker.first_name()} {faker.last_name()}",
			"description": faker.catch_phrase(),
			"rating": randint(1, 10)
		 }
	 }

BOOKS = list()

@app.patch("/books/{id}", status_code=200, summary="Partially update a book.", description="This endpoint is used to perform a partial update on the book given its object ID.")
async def patial_update_book(id: int, book: Book):
	for i in BOOKS:
		logger.debug(i)
		if i.id == id:
			BOOKS[i] = {
				"id": i.id,
				"title": book.title,
				"description": book.description,
				"author": book.author,
				"rating": book.rating
			}
	return BOOKS

@app.get(path="/books")
async def fetch_book_list():
	if len(BOOKS) > 0:
		for book in BOOKS:
			logger.debug(book)
		return BOOKS
	else:
		return {"message": "No books found in the list."}

@app.post(path="/books")
async def create_book(book: Book):
	BOOKS.append(book)
	return book