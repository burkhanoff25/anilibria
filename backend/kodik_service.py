import aiohttp
import logging
import os
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

KODIK_API_BASE = "https://kodikapi.com"
KODIK_API_TOKEN = (
    os.environ.get('KODIK_API_KEY')
    or 'f15d68e80eea7f2c8b1d3c37b5bba82c'
)

logger.info(f"🔑 Kodik API Token loaded: {KODIK_API_TOKEN[:10]}...")



class KodikService:
    """Service for interacting with Kodik API"""
    
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
        """Make request to Kodik API"""
        url = f"{KODIK_API_BASE}{endpoint}"
        session = await self.get_session()
        
        # Add token to params
        if params is None:
            params = {}
        params['token'] = KODIK_API_TOKEN
        
        logger.info(f"🔄 Making request to Kodik: {url} with params: {params}")
        
        try:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Kodik API success")
                    return data
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Kodik API error: {response.status} for {url}: {error_text}")
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Kodik API error: {response.status} {error_text}"
                    )
        except aiohttp.ClientError as e:
            logger.error(f"❌ Request error to Kodik API: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to connect to Kodik API: {str(e)}")
    
    async def search_anime(
        self,
        title: Optional[str] = None,
        shikimori_id: Optional[str] = None,
        limit: int = 100,
        with_material_data: bool = True
    ) -> Dict:
        """
        Search anime on Kodik
        
        Args:
            title: Anime title to search
            shikimori_id: Shikimori ID for exact match
            limit: Max results (default 100)
            with_material_data: Include material metadata
        
        Returns:
            Dict with results and metadata
        """
        params = {
            'limit': limit,
            'with_material_data': 'true' if with_material_data else 'false',
            'types': 'anime,anime-serial'
        }
        
        if title:
            params['title'] = title
        if shikimori_id:
            params['shikimori_id'] = shikimori_id
        
        data = await self._make_request("/search", params)
        return data
    
    async def get_anime_by_id(self, shikimori_id: str) -> Dict:
        """
        Get anime by Shikimori ID
        
        Args:
            shikimori_id: Shikimori ID
        
        Returns:
            Dict with anime data
        """
        data = await self.search_anime(shikimori_id=shikimori_id, limit=1)
        
        if data.get('results') and len(data['results']) > 0:
            return data['results'][0]
        else:
            raise HTTPException(status_code=404, detail="Anime not found on Kodik")
    
    async def list_anime(
        self,
        limit: int = 100,
        page: int = 1,
        year: Optional[int] = None,
        translation_id: Optional[int] = None,
        with_material_data: bool = True
    ) -> Dict:
        """
        List anime from Kodik
        
        Args:
            limit: Results per page
            page: Page number
            year: Filter by year
            translation_id: Filter by translation
            with_material_data: Include material metadata
        
        Returns:
            Dict with results and pagination
        """
        params = {
            'limit': limit,
            'page': page,
            'with_material_data': 'true' if with_material_data else 'false',
            'types': 'anime,anime-serial',
            'sort': 'updated_at'
        }
        
        if year:
            params['year'] = year
        if translation_id:
            params['translation_id'] = translation_id
        
        data = await self._make_request("/list", params)
        return data
    
    def process_kodik_result(self, result: Dict) -> Dict:
        """
        Process Kodik API result to normalized format
        
        Args:
            result: Raw Kodik API result
        
        Returns:
            Normalized anime data
        """
        material = result.get('material_data', {}) or {}
        
        # Extract player URL
        player_link = result.get('link', '')
        
        # Extract translations
        translations = []
        if result.get('translation'):
            translations.append({
                'id': result['translation'].get('id'),
                'title': result['translation'].get('title'),
                'type': result['translation'].get('type')
            })
        
        # Get poster image
        poster_url = None
        if material.get('poster_url'):
            poster_url = material['poster_url']
        elif material.get('screenshots') and len(material['screenshots']) > 0:
            poster_url = material['screenshots'][0]
        
        return {
            'id': result.get('id'),
            'type': result.get('type'),
            'title': result.get('title') or material.get('title'),
            'title_orig': result.get('title_orig') or material.get('title_en'),
            'shikimori_id': material.get('shikimori_id'),
            'year': result.get('year') or material.get('year'),
            'episodes_count': material.get('episodes_total') or result.get('episodes_count'),
            'poster_url': poster_url,
            'description': material.get('description'),
            'genres': material.get('anime_genres', []),
            'rating_shikimori': material.get('shikimori_rating'),
            'player_link': player_link,
            'translations': translations,
            'quality': result.get('quality'),
            'source': 'kodik'
        }


# Global instance
kodik_service = KodikService()
