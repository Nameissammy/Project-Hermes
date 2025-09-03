from fastapi import FastAPI
from project_hermes.main import kickoff

app = FastAPI()


@app.get("/poem/{prompt}")
def generate_poem(prompt: str):
    poem = kickoff(prompt)
    return {"poem": poem, "topic": prompt}
