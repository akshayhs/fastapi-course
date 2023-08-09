from fastapi import FastAPI

app = FastAPI()

BOOKS = [
	{'title': 'Book 1', 'author': 'Author 1'},
	{'title': 'Book 2', 'author': 'Author 2'},
	{'title': 'Book 3', 'author': 'Author 3'},
	{'title': 'Book 4', 'author': 'Author 4'},
	{'title': 'Book 5', 'author': 'Author 5'}
]

@app.get("/books/{book_id}", status_code=200, summary="Return the book with the given index ID.", deprecated=False)
async def fetch_book_by_id(book_id: int):
	item_idx = book_id - 1;
	return BOOKS[item_idx]

@app.get("/books", status_code=200, summary="Return a list of  all the books", response_description="Ok.", deprecated=False)
async def fetch_books_list():
	return BOOKS

