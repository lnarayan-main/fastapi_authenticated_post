from fastapi import FastAPI
from fastapi import FastAPI, Depends


from app.models import Base
from app.database import engine
from app.api import posts, auth



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authenticatd Posts")

app.include_router(auth.router)
app.include_router(posts.router)

@app.get("/")
def root():
    return {'message': "Welcome to home page."}