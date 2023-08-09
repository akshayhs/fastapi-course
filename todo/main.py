from pprint import pprint

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional

# Import the database engine
from db import engine, SessionLocal
# Import the instance from the models file
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class Todo(BaseModel):
	title: str
	description: Optional[str]
	priority: int = Field(ge=1, le=5, description="Priority must be between 1 and 5")
	complete: bool

def get_db_connection():
	try:
		db = SessionLocal()
		pprint(db.bind)
		yield db
	finally:
		db.close()
	
@app.delete("/todos/{id}", status_code=200)
async def delete_todo(id: int, db: Session = Depends(get_db_connection)):
  # Fetch the instance with the given ID
	instance = db.query(models.Todo).get(id)
	
	# Validate instance to make sure it exists
	if instance is None:
		raise HTTPException(status_code=400, detail=f"The instance with the given id of {id} does not exist in the database. Hence the DELETE operation failed on the instance.")
	# Delete the instance
	db.delete(instance)
	db.commit()

	# Return the response
	return {
		"status": 200,
		"success": True
	}


@app.patch("/todos/{id}", status_code=204)
async def partially_update_todo(id: int, todo: Todo, db: Session = Depends(get_db_connection)):
	# Fetch the todo by the given ID
	instance = db.query(models.Todo).get(id)
	if instance is None:
		raise HTTPException(status_code=400, detail=f"An instance with the given id of {id} was not found. Hence, the instance could not be partially updated successfully.")
	# If the instance was found
	instance.title = todo.title
	instance.description = todo.description
	instance.priority = todo.priority
	instance.complete = todo.complete
	db.add(instance)
	db.commit()
	return { 
		"status": 204,
		"type": "success"
	}

	
@app.get("/todos/{id}")
async def fetch_todo_by_id(id: int, db: Session = Depends(get_db_connection)):
	todo = db.query(models.Todo).get(id)
	if todo != None:
		return todo
	raise HTTPException(status_code=404, detail=f"Instance with the given id of {id} was not found in the database.")

@app.get("/todos")
async def fetch_books_list(db: Session = Depends(get_db_connection)):
	return db.query(models.Todo).all()

@app.post("/todos", status_code=201)
async def create_todo(todo: Todo, db: Session = Depends(get_db_connection)):
	instance = models.Todo()
	instance.title = todo.title
	instance.description = todo.description
	instance.priority = todo.priority
	instance.complete = todo.complete
	# Add the todo instance to the model
	db.add(instance=instance)
	db.commit()
	# Return a dictionary
	return { 
		"status": 201,
		"type": "success"
	}