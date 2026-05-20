from pathlib import Path
from fastapi import FastAPI, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, get_db, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


def get_current_user(session_user: str = Cookie(default=None)):
    return session_user

@app.get('/', response_class=HTMLResponse)
async def index(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={'user': user}
    )

from fastapi import Form
from fastapi.responses import RedirectResponse
from auth import hash_password, verify_pasword

@app.get('/register', response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='register.html',
        context={'error': None}
    )

@app.post('/register')
async def register(request: Request, db: Session = Depends(get_db),
                   username: str = Form(...), password: str = Form(...)):
    existing = db.query(models.User).filter_by(username=username).first()
    if existing:
        return templates.TemplateResponse(
            request=request,
            name='register.html',
            context={'error': 'Пользователь уже существует'}
        )
    user = models.User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()
    return RedirectResponse('/login', status_code=302)


@app.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='login.html',
        context={'error': None}
    )

@app.post('/login')
async def login(request: Request, db: Session = Depends(get_db),
                username: str = Form(...), password: str = Form(...)):
    user = db.query(models.User).filter_by(username=username).first()
    if not user or not verify_pasword(password, user.password):
        return templates.TemplateResponse(
            request=request,
            name='login.html',
            context={'error': 'Неверный логин или пароль'}
        )
    response = RedirectResponse('/', status_code=302)
    response.set_cookie('session_user', username)
    return response

@app.get('/logout')
async def logout():
    response = RedirectResponse('/', status_code=302)
    response.delete_cookie('session_user')
    return response