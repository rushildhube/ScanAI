from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import db
from routes import auth, upload, analysis
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
import os
from config.settings import settings

app = FastAPI(
    title="Dental Disease Classification API",
    description="API for a Dental Disease Classification Web Application using a ViT model.",
    version="1.0.0"
)

# Add Session Middleware to handle OAuth sessions.
# The secret_key is required to sign the session cookie.
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Middleware for CORS
origins = ["*"] # Change this in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers for modularity
app.include_router(auth.router, tags=["Authentication"], prefix="/auth")
app.include_router(upload.router, tags=["Image Upload"], prefix="/api")
app.include_router(analysis.router, tags=["Analysis"], prefix="/api")

# Connect/disconnect to database on startup/shutdown
@app.on_event("startup")
async def startup_db_client():
    await db.connect_to_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.close_db_connection()

# Serve static frontend files and HTML pages
if os.path.exists("../frontend/static"):
    app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open("../frontend/index.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend files not found. Please check the file paths.</h1>", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading page: {str(e)}</h1>", status_code=500)


@app.get("/login", response_class=HTMLResponse)
async def read_login():
    try:
        with open("../frontend/login.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Login page not found. Please check the file paths.</h1>", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading login page: {str(e)}</h1>", status_code=500)

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard():
    try:
        with open("../frontend/dashboard.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard page not found. Please check the file paths.</h1>", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading dashboard: {str(e)}</h1>", status_code=500)

# Root directory creation. These are relative to the project root,
# not the backend directory where the server is run.
os.makedirs("../uploads", exist_ok=True)
