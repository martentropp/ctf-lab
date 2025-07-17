from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
import psycopg2
from fastapi.responses import HTMLResponse
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
                            password="ctf_pass")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={}
    )

@app.post("/login")
async def login(username: str = Form(), password: str = Form()):
    conn = connect_to_db()
    cur = conn.cursor()
    sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        cur.execute(sql)
        result = cur.fetchone()
        if result:
            return {"message": f"Successfully logged in as {username}"}
        else:
            return {"error": "Invalid credentials."}
    except Exception as e:
        return {"error": "Failed to login"}
    finally:
        conn.close()