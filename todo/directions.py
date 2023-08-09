from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

class Direction(str, Enum):
	N = 'North'
	E = 'East'
	W = 'West'
	S = 'South'

@app.get(path="/directions/{choice}", status_code=200, summary="Fetch the choice from the user and return the direction for his choice")
async def fetch_user_choice(choice: Direction):
	if choice == Direction.N:
		return {"selected_choice": Direction.N}
	elif choice == Direction.E:
		return {"selected_choice": Direction.E}
	elif choice == Direction.W:
		return {"selected_choice": Direction.W}
	return {"selected_choice": Direction.S}

@app.get(path="/directions", status_code=200, summary="Fetch a list of all the available directions by default. If there is a query parameter, then return all directions except the one pointed by the query parameter.", deprecated=False)
async def fetch_available_directions(choice: Optional[Direction] = None):
	if choice:
		new_list = [{"choice": direction.value} for direction in Direction if direction != choice] 
		return new_list
	else:
		return [{"choice": direction.value} for direction in Direction]