from fastapi import FastAPI
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.models import Base
from app.database import engine
from app.api import posts, auth, ui



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authenticatd Posts")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(ui.router)

@app.get("/")
def root():
    return {'message': f"Welcome to home page. goto UI page 'ui/login'"}