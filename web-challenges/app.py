from fastapi import FastAPI, Request, Form, HTTPException
from pydantic import BaseModel
import psycopg2
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

class Challenge(BaseModel):
    id: int
    name: str
    description: str | None = None
    totalValue: int
    category: str | None = None

class User(BaseModel):
    id: int
    username: str
    password: str

class Attempt(BaseModel):
    challenge_id: int
    user_id: int
    score: int
    status: str

def connect_to_db():
    return psycopg2.connect(dbname="ctf_db", 
                            user="ctf_user", 
                            password="ctf_pass",
                            host="db",
                            port="5432")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={}
    )

@app.post("/login")
async def login(request: Request, username: str = Form(), password: str = Form()):
    conn = connect_to_db()
    cur = conn.cursor()
    sql = f"""SELECT * 
            FROM Users 
            WHERE username = '{username}' AND password = '{password}'"""

    try:
        cur.execute(sql)
        result = cur.fetchone()

        if result:
            return RedirectResponse(url=f"/dashboard?user={result[1]}", 
                                    status_code=302)
        else:
            return templates.TemplateResponse(
                request=request, 
                name="login.html", 
                context={"error": "Invalid username or password"}
            )
    except Exception as e:
        print(f"SQL Error: {e}")
        return templates.TemplateResponse(
            request=request,
            name="login.html", 
            context={"error": "Login failed. Please try again."}
        )
    finally:
        conn.close()

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: str):
    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={"username": user}
    )