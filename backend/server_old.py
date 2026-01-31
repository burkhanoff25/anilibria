from fastapi import FastAPI, APIRouter, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from anilibria_service import anilibria_service


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection (optional for API routes)
try:
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=2000)
    db = client[os.environ.get('DB_NAME', 'test_database')]
except Exception as e:
    logger.warning(f"⚠️ MongoDB connection warning: {e}")
    db = None

# Create the main app without a prefix
app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add CORS middleware FIRST (before routes)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # Allow all origins for development
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for genre images
GENRE_IMAGES_PATH = ROOT_DIR.parent / "public" / "genre-images"
if GENRE_IMAGES_PATH.exists():
    app.mount("/genre-images", StaticFiles(directory=str(GENRE_IMAGES_PATH)), name="genre-images")
    logger.info(f"✅ Mounted genre images directory: {GENRE_IMAGES_PATH}")
else:
    logger.warning(f"⚠️  Genre images directory not found: {GENRE_IMAGES_PATH}")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# AniLibria API Routes

@api_router.get("/anilibria/releases/latest")
async def get_latest_releases(
    limit: int = Query(12, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    """Get latest anime releases"""
    try:
        return await anilibria_service.get_latest_releases(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"Error fetching latest releases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/anilibria/releases/{release_id}")
async def get_release(release_id: int):
    """Get release by ID"""
    try:
        return await anilibria_service.get_release_by_id(release_id)
    except Exception as e:
        logger.error(f"Error fetching release {release_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/anilibria/releases/alias/{alias}")
async def get_release_by_alias(alias: str):
    """Get release by alias"""
    try:
        return await anilibria_service.get_release_by_alias(alias)
    except Exception as e:
        logger.error(f"Error fetching release by alias {alias}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/anilibria/releases/{release_id}/episodes")
async def get_episodes(release_id: int):
    """Get episodes for a release"""
    try:
        return await anilibria_service.get_episodes(release_id)
    except Exception as e:
        logger.error(f"Error fetching episodes for release {release_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/anilibria/search")
async def search_releases(
    query: Optional[str] = Query(None),
    genres: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    season: Optional[str] = Query(None),
    limit: int = Query(12, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    """Search anime releases"""
    try:
        genre_list = [int(g) for g in genres.split(",")] if genres else None
        return await anilibria_service.search_releases(
            query=query,
            genres=genre_list,
            year=year,
            season=season,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        logger.error(f"Error searching releases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/anilibria/schedule")
async def get_schedule():
    """Get release schedule"""
    try:
        return await anilibria_service.get_schedule()
    except Exception as e:
        logger.error(f"Error fetching schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/anilibria/genres")
async def get_genres():
    """Get all genres"""
    try:
        return await anilibria_service.get_genres()
    except Exception as e:
        logger.error(f"Error fetching genres: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/anilibria/franchises")
async def get_franchises(
    limit: int = Query(12, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    """Get franchises"""
    try:
        return await anilibria_service.get_franchises(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"Error fetching franchises: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/anilibria/torrents")
async def get_torrents(
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    """Get latest torrents"""
    try:
        return await anilibria_service.get_torrents(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"Error fetching torrents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/anilibria/videos")
async def get_videos(
    limit: int = Query(12, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    """Get latest videos"""
    try:
        return await anilibria_service.get_videos(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"Error fetching videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    await anilibria_service.close()