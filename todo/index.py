from fastapi import FastAPI

app = FastAPI()

@app.get("/", summary="Render the contents of the index endpoint.", response_description="Ok.", deprecated=False)
def render_index_contents():
  """This endpoint renders a simple message to indicate to the frontend client that no useful data is be served here."""
  return {"message": "You are currently at the index endpoint. This endpoint serves no data."}