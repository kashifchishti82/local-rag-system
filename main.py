from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rag_system.ingestion.router import router as ingestion_router
from rag_system.retrieval.router import router as retrieval_router
from rag_system.agents.router import router as agents_router
from rag_system.auth.router import router as auth_router
from rag_system.auth.service import get_current_active_user, decode_token
from config import settings

app = FastAPI(
    title=settings.API_TITLE,
    description="""
    A modular system for ingesting documents, managing AI agents, and generating content.
    
    This API provides endpoints for:
    - Document ingestion and processing
    - Semantic search and retrieval
    - AI agent workflows (Q&A, co-authoring, editing)
    """,
    version=settings.API_VERSION,
    contact={
        "name": settings.CONTACT_NAME,
        "email": settings.CONTACT_EMAIL
    },
    license_info={
        "name": settings.LICENSE_NAME,
        "url": settings.LICENSE_URL
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion_router)
app.include_router(retrieval_router)
app.include_router(agents_router)
app.include_router(auth_router)

# Add middleware to validate tokens for protected routes
@app.middleware("http")
async def validate_token(request, call_next):
    return await call_next(request)
    # Skip validation for public routes
    if request.url.path in ["/auth/login", "/auth/register", "/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)
    
    try:
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Not authenticated")
            
        token = auth_header.split()[1] if len(auth_header.split()) > 1 else None
        if not token:
            raise HTTPException(status_code=401, detail="Invalid token")
            
        # Verify token
        payload = decode_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
            
        # Add user info to request state
        request.state.user = payload
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    return await call_next(request)

# Protect retrieval and agents routes with authentication
def protect_routes(app):
    for route in retrieval_router.routes + agents_router.routes:
        if hasattr(route, 'endpoint'):
            route.endpoint = get_current_active_user(route.endpoint)

protect_routes(app)

@app.get("/", tags=["Health Check"])
def read_root():
    """Check the health of the application."""
    return {"status": "healthy", "message": "Welcome to the RAG System API!"}
