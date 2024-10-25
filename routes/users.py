from fastapi import Depends, APIRouter, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import date

from controllers.user_ctrl import UserCrud
from controllers.crud import Crud
from src import models, schemas
from src.security import (
    current_user_validation, get_current_user, hash_password
)
from src.database import SessionLocal, engine
import templates.pages as pages
import templates.users as tpl_users

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/users"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Table Page
@routes.get("/", response_class=HTMLResponse)
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    user_ctrl = UserCrud(db)
    rph_list = Crud(models.Rph, db).get()
    penyelia_list = Crud(models.Penyelia, db).get()
    juleha_list = Crud(models.Juleha, db).get()
    lapak_list = Crud(models.Lapak, db).get()
    actors = {
        "rph": rph_list,
        "penyelia": penyelia_list,
        "juleha": juleha_list,
        "lapak": lapak_list
    }
    users = user_ctrl.get_users(skip=skip, limit=limit)
    return str(pages.table_page(
        "users",
        tpl_users.users_table(actors, users)
    ))


# New Page
@routes.get("/new", response_class=HTMLResponse)
def new_user():
    return str(pages.detail_page(
        "user",
        tpl_users.user_form()
    ))


# Post Endpoint
@routes.post("/")
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    role: int = Form(...),
    acting_as: int = Form(...),
    db: Session = Depends(get_db)
):
    user = models.User(
        username=username,
        email=email,
        password=password,
        phone=phone,
        tgl_update=date.today(),
    )
    user_ctrl = UserCrud(db)
    db_user = user_ctrl.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = user_ctrl.create_user(user=user)
    role_ctrl = Crud(models.Role, db)
    role = models.Role(
        user_id=db_user.id,
        role=role,
        acting_as=acting_as,
    )
    role_ctrl.create(role)
    return RedirectResponse("/users", status_code=302)


# Edit Page
@routes.get("/edit/{username}", response_class=HTMLResponse)
def edit_user(req: Request, username: str, db: Session = Depends(get_db)):
    user = UserCrud(db).get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    form = tpl_users.user_form(user=user)
    if req.headers.get('HX-Request'):
        return str(form)
    else:
        return str(pages.detail_page("user", form))


# Actors dropdown
@routes.get("/acting_as", response_class=HTMLResponse)
def get_actors(role: int, db: Session = Depends(get_db)):
    match role:
        case 0:
            return str(tpl_users.super_admin())
        case 1:
            actors = Crud(models.Rph, db).get()
        case 2:
            actors = Crud(models.Penyelia, db).get()
        case 3:
            actors = Crud(models.Juleha, db).get()
        case 4:
            actors = Crud(models.Lapak, db).get()
    return str(tpl_users.actors_dropdown(actors))


# Detail Page
@routes.get("/{username}", response_class=HTMLResponse)
def read_user(username: str, db: Session = Depends(get_db)):
    lock = True
    user = UserCrud(db).get_user_by_username(username)
    role = Crud(models.Role, db).get_by('user_id', user.id)
    rph_list = Crud(models.Rph, db).get()
    penyelia_list = Crud(models.Penyelia, db).get()
    juleha_list = Crud(models.Juleha, db).get()
    lapak_list = Crud(models.Lapak, db).get()
    actors = {
        "rph": rph_list,
        "penyelia": penyelia_list,
        "juleha": juleha_list,
        "lapak": lapak_list
    }
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.detail_page(
        "users",
        tpl_users.user_form(user=user, role=role, actors=actors, lock=lock)
    ))


# Update Endpoint
@routes.put("/{username}", response_class=HTMLResponse)
async def update_user(
    username: str,
    email: str = Form(...),
    phone: str = Form(...),
    role: int = Form(...),
    acting_as: int = Form(...),
    db: Session = Depends(get_db)
):
    lock = True
    user_ctrl = UserCrud(db)
    role_ctrl = Crud(models.Role, db)
    user_db = user_ctrl.get_user_by_username(username)
    role_db = role_ctrl.get_by("user_id", user_db.id)

    user_db.email = email
    user_db.phone = phone
    user_db.tgl_update = date.today()
    role_db.role = role
    role_db.acting_as = acting_as

    user_db = user_ctrl.update(user_db)
    role_ctrl.update(role_db)
    rph_list = Crud(models.Rph, db).get()
    penyelia_list = Crud(models.Penyelia, db).get()
    juleha_list = Crud(models.Juleha, db).get()
    lapak_list = Crud(models.Lapak, db).get()
    actors = {
        "rph": rph_list,
        "penyelia": penyelia_list,
        "juleha": juleha_list,
        "lapak": lapak_list
    }
    return str(tpl_users.user_form(user_db, actors=actors, lock=lock))


@routes.get("/{username}/pass", response_class=HTMLResponse)
def update_password_view(username: str):
    return str(tpl_users.change_password_form(username))


@routes.put("/{username}/pass", response_class=HTMLResponse)
async def update_password(
    username: str,
    password: str = Form(...),
    password_new: str = Form(...),
    db: Session = Depends(get_db)
):
    lock = True
    user_ctrl = UserCrud(db)
    user_db = user_ctrl.get_user_by_username(username)

    if not current_user_validation(user_db, password):
        return tpl_users.unauthorized()
    user_db.password = hash_password(password_new)
    user_db.tgl_update = date.today()

    user_db = user_ctrl.update(user_db)
    rph_list = Crud(models.Rph, db).get()
    penyelia_list = Crud(models.Penyelia, db).get()
    juleha_list = Crud(models.Juleha, db).get()
    lapak_list = Crud(models.Lapak, db).get()
    actors = {
        "rph": rph_list,
        "penyelia": penyelia_list,
        "juleha": juleha_list,
        "lapak": lapak_list
    }
    return str(tpl_users.user_form(user_db, actors=actors, lock=lock))


# Delete Endpoint
@routes.post("/{rm_username}", response_class=HTMLResponse)
def remove_user(
    rm_username: str,
    password: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    rph_list = Crud(models.Rph, db).get()
    penyelia_list = Crud(models.Penyelia, db).get()
    juleha_list = Crud(models.Juleha, db).get()
    lapak_list = Crud(models.Lapak, db).get()
    actors = {
        "rph": rph_list,
        "penyelia": penyelia_list,
        "juleha": juleha_list,
        "lapak": lapak_list
    }
    if not current_user_validation(current_user, password):
        return str(tpl_users.unauthorized("/users/"))
    user_ctrl = UserCrud(db)
    user_db = user_ctrl.get_user_by_username(rm_username)
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    users = user_ctrl.remove(user_db)
    return str(tpl_users.users_table(actors, users))

