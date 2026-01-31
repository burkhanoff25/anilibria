import aiohttp
import logging
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
from genre_mapping import get_genre_image_filename, get_genre_name_by_id

logger = logging.getLogger(__name__)

ANILIBRIA_API_BASE = "https://api.anilibria.app/api/v1"
ANILIBRIA_CDN_BASE = "https://anilibria.tv"
ANILIBERTY_API_BASE = "https://aniliberty.top/api/v1"
ANILIBERTY_TOKEN = "animeekb"
ANILIBERTY_CSRF_TOKEN = "XPDjn9qYvXz6MaJ1x4bwxGNiaGejas7pFuJNgIjG"

# Path to custom genre images
GENRE_IMAGES_DIR = Path(__file__).parent.parent / "public" / "genre-images"


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
        headers = {
            "User-Agent": "Mozilla/5.0",
            "accept": "application/json",
        }
        
        logger.info(f"🔄 Making request to AniLibria: {url} with params: {params}")
        
        try:
            async with session.get(
                url,
                params=params,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ AniLibria API success: {len(data) if isinstance(data, list) else 'single'} item(s)")
                    return data
                else:
                    logger.error(f"❌ AniLibria API error: {response.status} for {url}")
                    raise HTTPException(status_code=response.status, detail=f"AniLibria API error: {response.status}")
        except aiohttp.ClientError as e:
            logger.error(f"❌ Request error to AniLibria API: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to connect to AniLibria API: {str(e)}")
    
    async def _make_aniliberty_request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Make request to AniLiberty API with authentication"""
        url = f"{ANILIBERTY_API_BASE}{endpoint}"
        session = await self.get_session()
        
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {ANILIBERTY_TOKEN}",
            "X-CSRF-TOKEN": ANILIBERTY_CSRF_TOKEN,
            "User-Agent": "Mozilla/5.0",
        }
        
        logger.info(f"🔄 Making request to AniLiberty: {url} with params: {params}")
        
        try:
            async with session.get(url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ AniLiberty API success: {len(data) if isinstance(data, list) else 'single'} item(s)")
                    return data
                else:
                    logger.error(f"❌ AniLiberty API error: {response.status} for {url}")
                    raise HTTPException(status_code=response.status, detail=f"AniLiberty API error: {response.status}")
        except aiohttp.ClientError as e:
            logger.error(f"❌ Request error to AniLiberty API: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to connect to AniLiberty API: {str(e)}")
    
    def _process_poster_url(self, poster: Optional[Dict]) -> Optional[str]:
        """Process poster URL to add CDN base"""
        if not poster:
            return None
        
        try:
            # Prefer optimized webp version
            if poster.get("optimized"):
                optimized = poster["optimized"]
                if isinstance(optimized, dict):
                    if optimized.get("src"):
                        return f"{ANILIBRIA_CDN_BASE}{optimized['src']}"
                    if optimized.get("preview"):
                        return f"{ANILIBRIA_CDN_BASE}{optimized['preview']}"
            
            # Fallback to main poster object
            if isinstance(poster, dict):
                if poster.get("src"):
                    return f"{ANILIBRIA_CDN_BASE}{poster['src']}"
                if poster.get("preview"):
                    return f"{ANILIBRIA_CDN_BASE}{poster['preview']}"
        except Exception as e:
            logger.warning(f"⚠️ Error processing poster: {e}")
        
        return None
    
    def _process_release(self, release: Dict) -> Dict:
        """Process release data to add full URLs"""
        if "poster" in release:
            release["poster_url"] = self._process_poster_url(release["poster"])
        
        if "latest_episode" in release and release["latest_episode"]:
            episode = release["latest_episode"]
            if "preview" in episode:
                preview = episode["preview"]
                if preview.get("optimized") and preview["optimized"].get("preview"):
                    episode["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['optimized']['preview']}"
                elif preview.get("preview"):
                    episode["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['preview']}"
                elif preview.get("src"):
                    episode["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['src']}"
        
        return release
    
    async def get_latest_releases(self, limit: int = 12, offset: int = 0) -> List[Dict]:
        """Get latest releases, aggregating multiple batches if needed for large limits"""
        BATCH_SIZE = 50  # AniLibria API max per request
        releases = []
        to_fetch = limit
        current_offset = offset
        while to_fetch > 0:
            batch_limit = min(BATCH_SIZE, to_fetch)
            params = {"limit": batch_limit, "offset": current_offset}
            data = await self._make_request("/anime/releases/latest", params)
            if not data:
                break
            releases.extend([self._process_release(release) for release in data])
            if len(data) < batch_limit:
                break  # No more data available
            to_fetch -= batch_limit
            current_offset += batch_limit
        return releases[:limit]
    
    async def get_random_release(self) -> Dict:
        """Get random release with full data"""
        session = await self.get_session()
        
        # First get random release ID
        params = {
            "limit": 1,
            "include": "id",
            "exclude": "poster,description"
        }
        
        async with session.get(
            f"{ANILIBERTY_API_BASE}/anime/releases/random",
            params=params,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as response:
            if response.status != 200:
                raise HTTPException(status_code=502, detail="Random release unavailable")
            data = await response.json()
        
        # Extract release ID
        release_id = None
        if isinstance(data, list) and len(data) > 0:
            release_id = data[0].get("id")
        elif isinstance(data, dict):
            release_id = data.get("id")
        
        if not release_id:
            raise HTTPException(status_code=404, detail="No random release found")
        
        # Get full release data
        return await self.get_release_by_id(release_id)
    
    async def get_release_by_id(self, release_id: int) -> Dict:
        """Get release by ID"""
        data = await self._make_request(f"/anime/releases/{release_id}")
        return self._process_release(data)
    
    async def get_release_by_alias(self, alias: str) -> Dict:
        """Get release by alias"""
        data = await self._make_request(f"/anime/releases/alias/{alias}")
        return self._process_release(data)

    async def get_similar_releases(self, release_id: int, limit: int = 12) -> List[Dict]:
        """Get similar releases by shared genres"""
        base_release = await self.get_release_by_id(release_id)
        base_genres = base_release.get("genres", []) if isinstance(base_release, dict) else []
        base_genre_ids = [g.get("id") for g in base_genres if isinstance(g, dict) and g.get("id")]

        if not base_genre_ids:
            return []

        candidates: List[Dict] = []
        for batch in range(4):
            params = {"limit": 50, "offset": batch * 50}
            data = await self._make_request("/anime/releases/latest", params)
            if not isinstance(data, list) or not data:
                break
            candidates.extend(data)

        scored: List[Dict] = []
        for item in candidates:
            if not isinstance(item, dict):
                continue
            if item.get("id") == release_id:
                continue
            item_genres = item.get("genres", [])
            item_genre_ids = [g.get("id") for g in item_genres if isinstance(g, dict) and g.get("id")]
            if not item_genre_ids:
                continue
            score = len(set(base_genre_ids) & set(item_genre_ids))
            if score == 0:
                continue
            item["_similarity_score"] = score
            scored.append(item)

        scored.sort(key=lambda r: (r.get("_similarity_score", 0), r.get("year") or 0), reverse=True)
        result = [self._process_release(r) for r in scored[:limit]]
        return result
    
    async def get_episodes(self, release_id: int) -> List[Dict]:
        """Get episodes for a release"""
        data = await self._make_request(f"/anime/releases/{release_id}")
        episodes = data.get("episodes", []) if isinstance(data, dict) else []

        # Process episode previews
        for episode in episodes:
            if "preview" in episode:
                preview = episode["preview"]
                if preview.get("optimized") and preview["optimized"].get("preview"):
                    episode["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['optimized']['preview']}"
                elif preview.get("preview"):
                    episode["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['preview']}"
                elif preview.get("src"):
                    episode["preview_url"] = f"{ANILIBRIA_CDN_BASE}{preview['src']}"

        return episodes
    
    async def search_releases(
        self, 
        query: Optional[str] = None,
        genres: Optional[List[int]] = None,
        year: Optional[int] = None,
        season: Optional[str] = None,
        limit: int = 12,
        offset: int = 0
    ) -> List[Dict]:
        """Search releases with filters - fetch multiple batches to ensure comprehensive results"""
        filtered: List[Dict] = []
        
        # When filtering by genre, fetch more batches to find enough results
        # since genre-specific releases may be scattered across multiple batches
        max_batches = 10 if genres else 2  # Increased from 5 to 10
        batch_size = 50
        
        logger.info(f"🔍 search_releases: query={query}, genres={genres}, year={year}, season={season}, limit={limit}, offset={offset}")
        
        for batch_num in range(max_batches):
            batch_offset = batch_num * batch_size
            params = {"limit": batch_size, "offset": batch_offset}
            
            try:
                data = await self._make_request("/anime/releases/latest", params)
            except Exception as e:
                logger.error(f"Error fetching batch {batch_num}: {str(e)}")
                if batch_num == 0:
                    raise
                break
            
            if not data or not isinstance(data, list):
                logger.info(f"⚠️ Batch {batch_num}: Empty or invalid data")
                break
            
            logger.info(f"📦 Batch {batch_num}: Fetched {len(data)} releases")
            
            for release in data:
                if query:
                    name = release.get("name", {}) or {}
                    haystack = " ".join(
                        str(value).lower()
                        for value in [
                            name.get("main"),
                            name.get("english"),
                            name.get("alternative"),
                            release.get("alias"),
                        ]
                        if value
                    )
                    if query.lower() not in haystack:
                        continue

                if year and release.get("year") != year:
                    continue

                if season:
                    season_value = release.get("season", {}) or {}
                    season_raw = season_value.get("value") or season_value.get("description")
                    if not season_raw or str(season_raw).lower() != str(season).lower():
                        continue

                if genres:
                    release_genres = release.get("genres", [])
                    genre_ids = [g.get("id") for g in release_genres if isinstance(g, dict)]
                    if not any(gid in genre_ids for gid in genres):
                        continue

                filtered.append(self._process_release(release))
            
            logger.info(f"✅ After batch {batch_num}: {len(filtered)} total filtered results")
            
            # Stop early if we have enough filtered results for pagination
            if len(filtered) >= offset + limit + 50:
                logger.info(f"🎯 Stopping early with {len(filtered)} filtered results")
                break

        logger.info(f"📊 Final: Slicing from offset {offset} to {offset + limit}, returning {len(filtered[offset:offset + limit])} releases")
        sliced = filtered[offset:offset + limit]
        return sliced
    
    async def get_schedule(self) -> List[Dict]:
        """Get release schedule organized by day of week"""
        # Fetch multiple batches to get comprehensive schedule data
        all_releases = []
        seen_ids = set()
        batch_size = 50
        
        for batch_num in range(5):  # Fetch 250 releases
            try:
                data = await self._make_request("/anime/releases/latest", {"limit": batch_size, "offset": batch_num * batch_size})
                if not data or not isinstance(data, list):
                    break
                
                # Add only unique releases
                for release in data:
                    release_id = release.get('id')
                    if release_id and release_id not in seen_ids:
                        seen_ids.add(release_id)
                        all_releases.append(release)
            except Exception as e:
                logger.error(f"Error fetching schedule batch {batch_num}: {str(e)}")
                if batch_num == 0:
                    raise
                break
        
        # Process releases
        result = []
        for release in all_releases:
            try:
                processed = self._process_release(release)
                result.append(processed)
            except Exception as e:
                logger.error(f"Error processing release for schedule: {str(e)}")
                continue
        
        return result
    
    async def get_genres(self) -> List[Dict]:
        """Get all genres with custom images"""
        session = await self.get_session()
        params = {
            "include": "id,type.genres",
            "exclude": "poster,description",
        }

        async with session.get(
            f"{ANILIBERTY_API_BASE}/anime/genres",
            params=params,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as response:
            if response.status != 200:
                raise HTTPException(status_code=502, detail="Genres unavailable")
            id_list = await response.json()

        async with session.get(
            f"{ANILIBERTY_API_BASE}/anime/genres",
            timeout=aiohttp.ClientTimeout(total=30),
        ) as response:
            if response.status != 200:
                raise HTTPException(status_code=502, detail="Genres unavailable")
            full_list = await response.json()

        details_by_id = {}
        for item in full_list:
            if isinstance(item, dict) and item.get("id") is not None:
                details_by_id[int(item["id"])] = item

        genres: List[Dict] = []
        for item in id_list:
            if not isinstance(item, dict):
                continue
            genre_id = item.get("id")
            if genre_id is None:
                continue

            details = details_by_id.get(int(genre_id), {})
            genre_name = (
                details.get("name")
                or item.get("name")
                or get_genre_name_by_id(genre_id)
            )
            if not genre_name:
                continue

            total_releases = details.get("total_releases") or item.get("total_releases") or 0
            image = details.get("image") or item.get("image") or {}
            optimized = image.get("optimized") or {}
            remote_path = (
                optimized.get("preview")
                or image.get("preview")
                or optimized.get("thumbnail")
                or image.get("thumbnail")
            )
            remote_url = f"{ANILIBERTY_API_BASE.replace('/api/v1', '')}{remote_path}" if remote_path else None

            genre: Dict[str, Any] = {
                "id": int(genre_id),
                "name": genre_name,
                "total_releases": total_releases,
                "custom_image": False,
            }

            if remote_url:
                genre["remote_image_url"] = remote_url

            image_filename = get_genre_image_filename(genre_name)
            for ext in [".webp", ".jpg", ".jpeg", ".png"]:
                image_path = GENRE_IMAGES_DIR / f"{image_filename}{ext}"
                if image_path.exists():
                    genre["image_url"] = f"/genre-images/{image_filename}{ext}"
                    genre["custom_image"] = True
                    logger.info(
                        f"✅ Using custom image for genre '{genre_name}': {image_filename}{ext}"
                    )
                    break

            if not genre.get("image_url") and remote_url:
                genre["image_url"] = remote_url

            genres.append(genre)

        return genres
    
    async def get_franchises(self, limit: int = 12, offset: int = 0) -> List[Dict]:
        """Get franchises, aggregating multiple batches if needed for large limits"""
        BATCH_SIZE = 50  # AniLibria API max per request
        franchises = []
        to_fetch = limit
        current_offset = offset
        while to_fetch > 0:
            batch_limit = min(BATCH_SIZE, to_fetch)
            params = {"limit": batch_limit, "offset": current_offset}
            data = await self._make_request("/anime/franchises", params)
            if not data:
                break
            # Process franchise images
            for franchise in data:
                if "image" in franchise:
                    image = franchise["image"]
                    if image.get("optimized") and image["optimized"].get("preview"):
                        franchise["image_url"] = f"{ANILIBRIA_CDN_BASE}{image['optimized']['preview']}"
                    elif image.get("preview"):
                        franchise["image_url"] = f"{ANILIBRIA_CDN_BASE}{image['preview']}"
                    elif image.get("src"):
                        franchise["image_url"] = f"{ANILIBRIA_CDN_BASE}{image['src']}"
            franchises.extend(data)
            if len(data) < batch_limit:
                break  # No more data available
            to_fetch -= batch_limit
            current_offset += batch_limit
        return franchises[:limit]
    
    async def get_torrents(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Get latest torrents"""
        params = {"limit": limit, "offset": offset}
        data = await self._make_request("/anime/torrents", params)
        torrents = data.get("data", data) if isinstance(data, dict) else data

        for torrent in torrents:
            release = torrent.get("release")
            if isinstance(release, dict):
                torrent["release"] = self._process_release(release)

        return torrents
    
    async def get_videos(self, limit: int = 12, offset: int = 0) -> List[Dict]:
        """Get latest videos from AniLiberty API"""
        params = {
            "limit": limit,
            "include": "id,type.genres",
            "exclude": "poster,description"
        }
        data = await self._make_aniliberty_request("/media/videos", params)
        
        # Process video data
        for video in data:
            # Add video player URL if available
            if "player" in video and video["player"]:
                video["player_url"] = video["player"]
            
            # Process preview images
            if "image" in video:
                image = video["image"]
                if image.get("optimized") and image["optimized"].get("preview"):
                    video["preview_url"] = f"{ANILIBRIA_CDN_BASE}{image['optimized']['preview']}"
                elif image.get("preview"):
                    video["preview_url"] = f"{ANILIBRIA_CDN_BASE}{image['preview']}"
            
            # Process genres if available
            if "type" in video and video["type"] and "genres" in video["type"]:
                video["genres"] = video["type"]["genres"]
        
        return data


# Global service instance
anilibria_service = AniLibriaService()
