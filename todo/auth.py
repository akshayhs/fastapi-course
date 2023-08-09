from datetime import datetime, timedelta
from os import environ

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from db import engine, SessionLocal
from models import User, Base

load_dotenv()

JWT_SECRET = environ.get("JWT_SECRET_KEY")
ALGORITHM = 'HS256'

class CreateUser(BaseModel):
	username: str
	email: Optional[str]
	first_name: str
	last_name: str
	last_name: str
	password: str
 
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Creates the database and performs all other necessary actions for our tables if for some reason, auth.py is ran before main.py
Base.metadata.create_all(bind=engine)

OAUTH2_BEARER = OAuth2PasswordBearer(tokenUrl="token")
	
app = FastAPI()

def get_database_connection():
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()

def get_password_hash(password):
	# Accepts the incoming password desired by the user, hashes it using bcrypt algorithm and returns the hash.
	return bcrypt_context.hash(password)

def verify_passwords(user_password, hashed_password):
	"""This function is used to verify if the user entered password matches with the hashed password in our database."""
	return bcrypt_context.verify(user_password, hashed_password)

def authenticate_user(username: str, password: str, db):
	user = db.query(User).get(username == username)
	# Check if the user exists in the database
	if not user:
		return False
	if not verify_passwords(password, user.password):
		return False
	return user

def create_access_token(id: int, username: str, db, expires: Optional[timedelta] = None):
	fetch_user = db.query(User).get(id)
	user = {"id": fetch_user.id, "username": fetch_user.username}
	data = {"user": user}
	# Check if the expires has a set values
	if expires is not None:
		expiry = datetime.utcnow() + expires
		# Convert the expiry time to string
		expirty_string = str(int(expiry.timestamp()))
		# Update the encode dictionary to indicate when to expire
		data.update({"expires": expirty_string})
	else:
		# If there is no value associated to the expires argument, then by default the token expires in 15 minutes from generation time
		expiry = datetime.now() + timedelta(minutes=15)
		# Convert the expiry time to string
		expirty_string = str(int(expiry.timestamp()))
		# Update the encode dictionary to indicate when to expire
		data.update({"expires": expirty_string})
	# Return the encoded string with the user, secret signing key and the algorithm to use
	return {
		"token": jwt.encode(data, JWT_SECRET, algorithm=ALGORITHM),
		"expires": expirty_string
	}

async def get_current_user(token: str = Depends(OAUTH2_BEARER)):
	try:
		payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
		username: str = payload.get("user")
		id: int = payload.get("id")
		if id is None or username is None:
			raise HTTPException(status_code=404, detail="No user was found for the given user")
		return {
			"id": id,
			"username": username
		}
	except JWTError as exc:
		raise HTTPException(status_code=400, detail=str(exc))
	

@app.post("/users/account/signup", status_code=201)
async def create_user(user: CreateUser, db: Session = Depends(get_database_connection)):
	new_user = User(username=user.username, email=user.email, first_name=user.first_name, last_name=user.last_name)
	new_user.password = get_password_hash(user.password)
	db.add(new_user)
	db.commit()
	return JSONResponse(status_code=201, content={
		"message": f"A user for {new_user.email} has been created successfully.",
		"status": "success",
		"status_code": 201
	})

@app.post("/users/auth/token", status_code=200)
async def perform_auth(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_database_connection)):
	user = authenticate_user(form.username, form.password, db)
	if not user:
		raise HTTPException(status_code=404, detail="No user was found for the given email address.")
	token_duration = timedelta(minutes=5)
	token = create_access_token(user.id, user.username, db, expires=token_duration)
	return token