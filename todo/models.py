from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional
# The Base class is used to subclass the Model class
from db import Base

class User(Base):
	__tablename__ = 'user' # Defining the name for the user table in the database

	# Columns for the table goes here
	id: int = Column(Integer, primary_key=True, index=True)
	username: str = Column(String, unique=True)
	email: Optional[str] = Column(String, unique=True, index=True)
	first_name: str = Column(String)
	last_name: str = Column(String)
	password: str = Column(String)
	is_active: bool = Column(Boolean, default=True)
	todos = relationship("Todo", back_populates="user")  # One-to-many relationship

class Todo(Base):
	"""A Model for Todo"""
	__tablename__ = 'todo' # Defining the name for the todo table in the database

	# Columns for the table goes here
	id: int = Column(Integer, primary_key=True, index=True)
	title: str = Column(String)
	description: str = Column(String)
	priority: int = Column(Integer)
	complete: bool = Column(Boolean, default=False)
	user_id = Column(Integer, ForeignKey("user.id"))
	user = relationship("User", back_populates="todos")  # Many-to-one relationship
