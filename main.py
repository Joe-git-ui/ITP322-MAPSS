import os
import httpx
from fastapi import FastAPI, HTTPException, Security, Depends, Request
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

# Load variables from your .env file
load_dotenv()
LOCATIONIQ_KEY = os.getenv("LOCATIONIQ_API_KEY")
MY_APP_KEY = os.getenv("MY_APP_AUTH_KEY")

# Set up Rate Limiting (Required: prevents abuse)
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="ITP 322: Group 1 - LocationIQ Integration")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set up API Key Authentication (Required: 1 of 2 choices)
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def get_api_key(header_key: str = Depends(api_key_header)):
    if header_key == MY_APP_KEY:
        return header_key
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )

@app.get("/search")
@limiter.limit("5/minute") # Rate limiting implementation
async def search_location(
    location: str, 
    request: Request, 
    token: str = Depends(get_api_key)
):
    """
    Integrates with LocationIQ to find coordinates for a specific place.
    """
    url = "https://us1.locationiq.com/v1/search.php"
    params = {
        "key": LOCATIONIQ_KEY,
        "q": location,
        "format": "json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, 
            detail="Error from LocationIQ API"
        )
        
    return response.json()

@app.get("/")
async def root():
    return {"message": "Group 1 Systems Integration API is Running"}