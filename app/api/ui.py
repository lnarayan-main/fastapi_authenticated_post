from fastapi import APIRouter, Request, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/ui", tags=["ui"])

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.getenv("APP_BASE_DIR", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
templates_dir = os.path.join(BASE_DIR, "templates")

os.makedirs(templates_dir, exist_ok=True)

templates = Jinja2Templates(directory=templates_dir)

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

async def get_ui_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    return token

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, token: str = Depends(get_ui_token)):
    if not token:
        return RedirectResponse(url="/ui/login", status_code=303)
    
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/create-post", response_class=HTMLResponse)
async def create_post_page(request: Request, token: str = Depends(get_ui_token)):
    if not token:
        return RedirectResponse(url="/ui/login", status_code=303)
    return templates.TemplateResponse("create_post.html", {"request": request})

@router.get("/edit-post/{post_id}", response_class=HTMLResponse)
async def edit_post_page(request: Request, post_id: int, token: str = Depends(get_ui_token)):
    if not token:
        return RedirectResponse(url="/ui/login", status_code=303)
    return templates.TemplateResponse("edit_post.html", {"request": request, "post_id": post_id})


@router.get("/post-detail/{post_id}", response_class=HTMLResponse)
async def post_detail_page(request: Request, post_id: int, token: str = Depends(get_ui_token)):
    if not token:
        return RedirectResponse(url="/ui/login", status_code=303)
    return templates.TemplateResponse("post_detail.html", {"request": request, "post_id": post_id})


# @router.get("/test", response_class=HTMLResponse)
# async def test_page():
#     return HTMLResponse(content="<h1>Test Page Works!</h1>")





