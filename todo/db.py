from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a database URL and associate it to a variable
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

# Create a database engine using the connection URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {
	"check_same_thread": False
})

# Create a database session that basically binds to the engine above
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base for creating different Models
Base = declarative_base()