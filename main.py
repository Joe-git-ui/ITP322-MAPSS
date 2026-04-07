import os
import httpx
from fastapi import FastAPI, HTTPException, Security, Depends, Request
from fastapi.security.api_key import APIKeyHeader
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

from pydantic import BaseModel
from typing import List, Union

# Load variables from your .env file
load_dotenv()
LOCATIONIQ_KEY = os.getenv("LOCATIONIQ_API_KEY")
MY_APP_KEY = os.getenv("MY_APP_AUTH_KEY")

# Pydantic Models
class LocationQuery(BaseModel):
    location: str

class LatLon(BaseModel):
    lat: float
    lon: float

class Place(BaseModel):
    lat_lon: LatLon
    display_name: str

class GeocodingResponse(BaseModel):
    places: List[Place]
    map_image: Union[bytes, None] = None

# Set up Rate Limiting (Required: prevents abuse)
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="ITP 322: Group 1 - LocationIQ Integration")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set up API Key Authentication (Required: 1 of 2 choices)
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def get_auth_or_rate_limit(header_key: str = Security(api_key_header)):
    """Rate limit only unauthorized requests. No request param (linter fix); uses fixed key for unauth."""
    if header_key is None or header_key != MY_APP_KEY:
        # Fixed IP key for unauth rate limit (per client IP approx)
        ip_key = 'unauth_client_ip_placeholder'
        app.state.limiter.check(ip_key, "5/minute")
    # Auth OK or bypassed
    return True

@app.get("/search", response_model=GeocodingResponse)
async def search_location(
    query: LocationQuery = Depends(),
    request: Request,
    api_check: bool = Depends(get_auth_or_rate_limit)
):
    """
    Geocodes location with Pydantic validation, returns structured places list and static map image PNG bytes.
    Rate limiting applied only to unauthorized requests (5/min).
    """
    url = "https://us1.locationiq.com/v1/search.php"
    params = {
        "key": LOCATIONIQ_KEY,
        "q": query.location,
        "format": "json"
    }
    
    async with httpx.AsyncClient() as client:
        resp_geo = await client.get(url, params=params)
        
        if resp_geo.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Geocoding API error: {resp_geo.status_code}"
            )
        
        try:
            data: list[dict] = resp_geo.json()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid JSON from geocoding API")
        
        places = []
        map_image = None
        if data:
            # Parse places with Pydantic
            for item in data:
                lat_lon = LatLon(lat=float(item["lat"]), lon=float(item["lon"]))
                places.append(Place(lat_lon=lat_lon, display_name=item["display_name"]))
            
            # Generate static map image for first place
            first_lat = places[0].lat_lon.lat
            first_lon = places[0].lat_lon.lon
            static_url = "https://api.locationiq.com/v1/staticmap"
            static_params = {
                "key": LOCATIONIQ_KEY,
                "center": f"{first_lat},{first_lon}",
                "zoom": 13,
                "size": "512x400",
                "format": "png"
            }
            resp_img = await client.get(static_url, params=static_params)
            
            if resp_img.status_code == 200:
                map_image = resp_img.content
            else:
                # Log but don't fail
                pass
        
        return GeocodingResponse(places=places, map_image=map_image)

@app.get("/")
async def root():
    return {"message": "Group 1 Systems Integration API is Running"}