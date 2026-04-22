import shutil
import os
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import PostResponse
from app.auth import get_current_user
from app.models import User, Post
from datetime import datetime, timezone

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post("/create-post", response_model=PostResponse)
def create_post(
    title: str = Form(...),
    status: str = Form("Active"),
    content: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    post = Post(
        user_id=current_user.id,
        title=title,
        status=status,
        content=content,
    )

    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/update-post/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    title: str = Form(...),
    status: str = Form("Active"),
    content: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_post = db.query(Post).filter(Post.id == post_id, Post.user_id == current_user.id).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    
    now = datetime.now(timezone.utc)
    post_time = db_post.created_at
    if post_time.tzinfo is None:
        post_time = post_time.replace(tzinfo=timezone.utc)

    time_passed = now - post_time

    if time_passed.total_seconds() > (2 * 3600): 
        raise HTTPException(status_code=403, detail="Too late to edit!")

    db_post.title = title
    db_post.status = status
    db_post.content = content

    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/get-posts", response_model=List[PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    posts = (
        db.query(Post).filter(Post.user_id == current_user.id)
        .order_by(Post.created_at.desc())
        .all()
    )

    db.commit()
    return posts[::-1]


@router.get("/all-posts", response_model=List[PostResponse])
def get_posts(
    db: Session = Depends(get_db),
):
    posts = (
        db.query(Post)
        .order_by(Post.created_at.desc())
        .all()
    )

    db.commit()
    return posts[::-1]


@router.get("/post-by-id/{post_id}", response_model=PostResponse)
def get_posts(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/delete-post/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == current_user.id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    
    now = datetime.now(timezone.utc)
    post_time = post.created_at
    if post_time.tzinfo is None:
        post_time = post_time.replace(tzinfo=timezone.utc)

    time_passed = now - post_time

    if time_passed.total_seconds() > (2 * 3600): 
        raise HTTPException(status_code=403, detail="Too late to delete!")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully."}
