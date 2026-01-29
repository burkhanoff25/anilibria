import aiohttp
import logging
from typing import Optional, List, Dict, Any
from fastapi import HTTPException

logger = logging.getLogger(__name__)

ANILIBRIA_API_BASE = "https://api.anilibria.app/api/v1"
ANILIBRIA_CDN_BASE = "https://anilibria.top"


class AniLibriaService:
    """Service for interacting with AniLibria API"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Make request to AniLibria API"""
        url = f"{ANILIBRIA_API_BASE}{endpoint}"
        session = await self.get_session()
        
        try:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"AniLibria API error: {response.status} for {url}")
                    raise HTTPException(status_code=response.status, detail=f"AniLibria API error: {response.status}")
        except aiohttp.ClientError as e:
            logger.error(f"Request error to AniLibria API: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to connect to AniLibria API: {str(e)}")
    
    def _process_poster_url(self, poster: Optional[Dict]) -> Optional[str]:
        """Process poster URL to add CDN base"""
        if not poster:
            return None
        
        # Prefer optimized webp version
        if poster.get("optimized") and poster["optimized"].get("src"):
            return f"{ANILIBRIA_CDN_BASE}{poster['optimized']['src']}"
        elif poster.get("src"):
            return f"{ANILIBRIA_CDN_BASE}{poster['src']}"
        
        return None
    
    def _process_release(self, release: Dict) -> Dict:
        """Process release data to add full URLs"""
        if "poster" in release:
            release["poster_url"] = self._process_poster_url(release["poster"])
        
        if "latest_episode" in release and release["latest_episode"]:
            episode = release["latest_episode"]
            if "preview" in episode:
                preview = episode["preview"]
                if preview.get("optimized") and preview["optimized"].get("src"):
                    episode["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['optimized']['src']}"
                elif preview.get("src"):
                    episode["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['src']}"
        
        return release
    
    async def get_latest_releases(self, limit: int = 12, offset: int = 0) -> List[Dict]:
        """Get latest releases"""
        params = {"limit": limit, "offset": offset}
        data = await self._make_request("/anime/releases/latest", params)
        return [self._process_release(release) for release in data]
    
    async def get_release_by_id(self, release_id: int) -> Dict:
        """Get release by ID"""
        data = await self._make_request(f"/anime/releases/{release_id}")
        return self._process_release(data)
    
    async def get_release_by_alias(self, alias: str) -> Dict:
        """Get release by alias"""
        data = await self._make_request(f"/anime/releases/alias/{alias}")
        return self._process_release(data)
    
    async def get_episodes(self, release_id: int) -> List[Dict]:
        """Get episodes for a release"""
        data = await self._make_request(f"/anime/releases/{release_id}/episodes")
        
        # Process episode previews
        for episode in data:
            if "preview" in episode:
                preview = episode["preview"]
                if preview.get("optimized") and preview["optimized"].get("src"):
                    episode["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['optimized']['src']}"
                elif preview.get("src"):
                    episode["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['src']}"
        
        return data
    
    async def search_releases(
        self, 
        query: Optional[str] = None,
        genres: Optional[List[int]] = None,
        year: Optional[int] = None,
        season: Optional[str] = None,
        limit: int = 12,
        offset: int = 0
    ) -> List[Dict]:
        """Search releases with filters"""
        params = {"limit": limit, "offset": offset}
        
        if query:
            params["search"] = query
        if genres:
            params["genres"] = ",".join(map(str, genres))
        if year:
            params["year"] = year
        if season:
            params["season"] = season
        
        data = await self._make_request("/anime/releases", params)
        return [self._process_release(release) for release in data]
    
    async def get_schedule(self) -> Dict:
        """Get release schedule"""
        data = await self._make_request("/anime/releases/schedule")
        
        # Process schedule data
        for day_key in data:
            if isinstance(data[day_key], list):
                data[day_key] = [self._process_release(release) for release in data[day_key]]
        
        return data
    
    async def get_genres(self) -> List[Dict]:
        """Get all genres"""
        data = await self._make_request("/anime/catalog/references/genres")
        
        # Process genre images
        for genre in data:
            if "image" in genre:
                image = genre["image"]
                if image.get("optimized") and image["optimized"].get("preview"):
                    genre["image_url"] = f"{ANILIBRIA_CDN_BASE}{image['optimized']['preview']}"
                elif image.get("preview"):
                    genre["image_url"] = f"{ANILIBRIA_CDN_BASE}{image['preview']}"
        
        return data
    
    async def get_franchises(self, limit: int = 12, offset: int = 0) -> List[Dict]:
        """Get franchises"""
        params = {"limit": limit, "offset": offset}
        data = await self._make_request("/anime/franchises", params)
        
        # Process franchise images
        for franchise in data:
            if "image" in franchise:
                image = franchise["image"]
                if image.get("optimized") and image["optimized"].get("src"):
                    franchise["image_url"] = f"{ANILIBRIA_CDN_BASE}{image['optimized']['src']}"
                elif image.get("src"):
                    franchise["image_url"] = f"{ANILIBRIA_CDN_BASE}{image['src']}"
        
        return data
    
    async def get_torrents(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Get latest torrents"""
        params = {"limit": limit, "offset": offset}
        data = await self._make_request("/anime/torrents", params)
        return data
    
    async def get_videos(self, limit: int = 12, offset: int = 0) -> List[Dict]:
        """Get latest videos"""
        params = {"limit": limit, "offset": offset}
        data = await self._make_request("/media/videos/latest", params)
        
        # Process video previews
        for video in data:
            if "preview" in video:
                preview = video["preview"]
                if preview.get("optimized") and preview["optimized"].get("src"):
                    video["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['optimized']['src']}"
                elif preview.get("src"):
                    video["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['src']}"
        
        return data


# Global service instance
anilibria_service = AniLibriaService()
