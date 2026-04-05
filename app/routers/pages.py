from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "home.html")


@router.get("/sign_up", response_class=HTMLResponse)
def read_signup(request: Request):
    return templates.TemplateResponse(request, "signup.html")


@router.get("/login", response_class=HTMLResponse)
def read_login(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.get("/profile", response_class=HTMLResponse)
def read_profile(request: Request):
    return templates.TemplateResponse(request, "profile.html")


@router.get("/modify_name", response_class=HTMLResponse)
def read_modify_name(request: Request):
    return templates.TemplateResponse(request, "modify_name.html")
