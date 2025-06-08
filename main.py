from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import crear_consecutivo, obtener_hojas
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

USERS = {"admin": "1234", "usuario1": "clave1"}
sesiones = {}

@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if USERS.get(username) == password:
        sesiones["usuario"] = username
        return RedirectResponse("/dashboard", status_code=303)
    return templates.TemplateResponse("index.html", {"request": request, "error": "Credenciales incorrectas"})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if "usuario" not in sesiones:
        return RedirectResponse("/", status_code=303)
    hojas = obtener_hojas()
    return templates.TemplateResponse("dashboard.html", {"request": request, "hojas": hojas, "usuario": sesiones["usuario"]})

@app.post("/insert_project")
def insertar(asunto: str = Form(...), elaborado_por: str = Form(...)):
    consecutivo = crear_consecutivo(asunto, elaborado_por)
    return {"message": f"Agregado: {consecutivo}"}

@app.get("/logout")
def logout():
    sesiones.pop("usuario", None)
    return RedirectResponse("/")