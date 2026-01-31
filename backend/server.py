from fastapi import FastAPI, APIRouter, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

# Create router
api_router = APIRouter(prefix="/api")

# New endpoint: Get releases for a franchise
@api_router.get("/anilibria/franchises/{franchise_id}/releases")
async def get_franchise_releases(franchise_id: str):
    """Get all releases for a given franchise (by id or name match)"""
    try:
        # Fetch all releases and all franchises
        franchises = await anilibria_service.get_franchises(200)
        releases = await anilibria_service.get_latest_releases(500)
        # Find the franchise by id
        franchise = next((f for f in franchises if str(f.get("id")) == str(franchise_id)), None)
        if not franchise:
            return []
        # Try to match releases by franchise id or by name
        franchise_name = franchise.get("name")
        franchise_id_val = franchise.get("id")
        matched = []
        for r in releases:
            # Try to match by explicit field if present
            if str(r.get("franchise_id")) == str(franchise_id_val):
                matched.append(r)
            elif str(r.get("franchise")) == str(franchise_id_val):
                matched.append(r)
            # Fallback: try to match by franchise name if available
            elif franchise_name and (
                (r.get("franchise_name") and r.get("franchise_name").strip().lower() == franchise_name.strip().lower()) or
                (r.get("franchise") and isinstance(r.get("franchise"), str) and r.get("franchise").strip().lower() == franchise_name.strip().lower())
            ):
                matched.append(r)
        return matched
    except Exception as e:
        logger.error(f"Error fetching franchise releases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from anilibria_service import anilibria_service
from kodik_service import kodik_service


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging FIRST
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB connection (optional)
client = None
db = None
try:
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=2000)
    db = client[os.environ.get('DB_NAME', 'test_database')]
    logger.info("✅ MongoDB connected")
except Exception as e:
    logger.warning(f"⚠️ MongoDB not available: {e}")

# Create FastAPI app
app = FastAPI()

# Add CORS middleware FIRST
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for genre images
GENRE_IMAGES_PATH = ROOT_DIR.parent / "public" / "genre-images"
if GENRE_IMAGES_PATH.exists():
    app.mount("/genre-images", StaticFiles(directory=str(GENRE_IMAGES_PATH)), name="genre-images")
    logger.info(f"✅ Mounted genre images directory: {GENRE_IMAGES_PATH}")

# Create router
api_router = APIRouter(prefix="/api")

# Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Routes
@api_router.get("/")
async def root():
    return {"message": "API is running", "status": "ok"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    try:
        await db.status_checks.insert_one(doc)
        return status_obj
    except Exception as e:
        logger.error(f"Error creating status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    if not db:
        return []
    
    try:
        status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
        for check in status_checks:
            if isinstance(check.get('timestamp'), str):
                check['timestamp'] = datetime.fromisoformat(check['timestamp'])
        return status_checks
    except Exception as e:
        logger.error(f"Error fetching status: {e}")
        return []

# AniLibria API Routes
@api_router.get("/anilibria/releases/latest")
async def get_latest_releases(
    limit: int = Query(12, ge=1, le=500),  # Increased max limit
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

@api_router.get("/anilibria/releases/{release_id}/similar")
async def get_similar_releases(
    release_id: int,
    limit: int = Query(12, ge=1, le=24)
):
    """Get similar releases by genre"""
    try:
        return await anilibria_service.get_similar_releases(release_id, limit=limit)
    except Exception as e:
        logger.error(f"Error fetching similar releases for {release_id}: {str(e)}")
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
        releases = await anilibria_service.search_releases(
            query=query,
            genres=genre_list,
            year=year,
            season=season,
            limit=limit,
            offset=offset
        )
        if releases:
            return releases

        if query:
            kodik_data = await kodik_service.search_anime(title=query, limit=limit)
            kodik_results = kodik_data.get("results", []) if isinstance(kodik_data, dict) else []
            mapped = []
            for item in kodik_results:
                processed = kodik_service.process_kodik_result(item)
                mapped.append({
                    "id": processed.get("shikimori_id") or processed.get("id"),
                    "name": {"main": processed.get("title") or "Без названия"},
                    "alias": None,
                    "poster_url": processed.get("poster_url"),
                    "year": processed.get("year"),
                    "description": processed.get("description"),
                    "genres": [
                        {"name": genre} for genre in (processed.get("genres") or [])
                    ],
                    "type": "Kodik",
                    "source": "kodik",
                    "player_link": processed.get("player_link"),
                    "original_title": processed.get("title_orig") or "",
                })
            return mapped

        return releases
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

@api_router.get("/anilibria/random")
async def get_random_release():
    """Get a random anime release"""
    try:
        return await anilibria_service.get_random_release()
    except Exception as e:
        logger.error(f"Error fetching random release: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/anilibria/franchises")
async def get_franchises(
    limit: int = Query(12, ge=1, le=500),  # Increased max limit
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

# Kodik API endpoints
@api_router.get("/kodik/search")
async def kodik_search(
    title: Optional[str] = Query(None),
    shikimori_id: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=100)
):
    """Search anime on Kodik"""
    try:
        data = await kodik_service.search_anime(
            title=title,
            shikimori_id=shikimori_id,
            limit=limit
        )
        
        # Process results
        if data.get('results'):
            processed_results = [
                kodik_service.process_kodik_result(result)
                for result in data['results']
            ]
            return {
                'results': processed_results,
                'total': data.get('total', 0),
                'prev_page': data.get('prev_page'),
                'next_page': data.get('next_page')
            }
        return data
    except Exception as e:
        logger.error(f"Error searching Kodik: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/kodik/anime/{shikimori_id}")
async def kodik_get_anime(shikimori_id: str):
    """Get anime by Shikimori ID from Kodik"""
    try:
        result = await kodik_service.get_anime_by_id(shikimori_id)
        return kodik_service.process_kodik_result(result)
    except Exception as e:
        logger.error(f"Error fetching anime from Kodik: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/kodik/list")
async def kodik_list(
    limit: int = Query(100, ge=1, le=100),
    page: int = Query(1, ge=1),
    year: Optional[int] = Query(None),
    translation_id: Optional[int] = Query(None)
):
    """List anime from Kodik"""
    try:
        data = await kodik_service.list_anime(
            limit=limit,
            page=page,
            year=year,
            translation_id=translation_id
        )
        
        # Process results
        if data.get('results'):
            processed_results = [
                kodik_service.process_kodik_result(result)
                for result in data['results']
            ]
            return {
                'results': processed_results,
                'total': data.get('total', 0),
                'prev_page': data.get('prev_page'),
                'next_page': data.get('next_page')
            }
        return data
    except Exception as e:
        logger.error(f"Error listing anime from Kodik: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Include router
app.include_router(api_router)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    try:
        if client:
            client.close()
        await anilibria_service.close()
        await kodik_service.close()
    except Exception as e:
        logger.warning(f"Shutdown warning: {e}")


