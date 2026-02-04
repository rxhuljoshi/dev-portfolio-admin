from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import experiences, projects, coolstuff, content

app = FastAPI(
    title="Portfolio Admin API",
    description="API for managing portfolio content",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(experiences.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(coolstuff.router, prefix="/api")
app.include_router(content.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Portfolio Admin API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
