from fastapi import Form, FastAPI, Response, status
from faker import Faker
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
faker = Faker()

@app.post("/login", status_code=200)
async def user_login(username: str = Form(), password: str = Form()):
	return {
		"username": username,
		"password": password
	}