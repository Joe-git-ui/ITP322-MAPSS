To create the file:
1.Open Sublime Text (or your preferred editor).
2.Create a New File.
3.Paste the content below into that file.
4.Save it as README.md in your MAPS folder.

# ITP 322: Group 1 - LocationIQ Geocoding & Mapping API

## Systems Integration and Architecture 2

## Project Description

This project demonstrates the integration of LocationIQ Geocoding and Static Maps APIs into a FastAPI application. It provides production-ready endpoints for converting location names to coordinates and generating map images, with security, Pydantic validation, and smart rate limiting.

## Features

- **Geocoding Search:** Real-time lat/lon for locations using LocationIQ.
- **Static Map Imaging:** PNG map image bytes for the first result.
- **Pydantic Models:** Type-safe request/response validation.
- **Smart Rate Limiting:** 5/min *only for unauthorized users* (authenticated bypass).
- **API Key Authentication:** Secure X-API-KEY header.
- **Swagger Docs:** Interactive API docs at `/docs`.

## Step-by-Step Setup for Beginners

### 1. Prerequisites

- Python 3.10+ (download from python.org)
- Git (git-scm.com)

### 2. Clone, Venv, Install

```bash
git clone <your-repo-url> ITP322-MAPS-master
cd ITP322-MAPS-master
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate
pip install -r requirements.txt
```

**Note:** All deps (fastapi, uvicorn, pydantic, httpx, slowapi, dotenv) in requirements.txt.

## 3. Get API Key & Configure .env (Required!)

### Get LocationIQ API Key (Free!)

1. Visit https://locationiq.com/
2. Click **Sign Up** (use email/password).
3. Verify your email.
4. Go to **Dashboard** > **API Keys**.
5. Create a new key (free plan: 5k requests/day for geocoding + static maps).
6. Copy the key (format: `pk.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`).

### Setup .env

1. Copy `.env.example` to `.env` (in project root).
2. Open `.env` in editor.
3. Paste your `LOCATIONIQ_API_KEY=pk.your_key_here`
4. Set `MY_APP_AUTH_KEY=your_strong_password_here` (for your API auth header).

**Security:** Never commit `.env` (already in .gitignore).

## 4. Run & Test

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs

### Try /search

- **Query:** `?location=Bontoc`
- **Auth (optional, bypasses rate limit):** Click **Authorize** > `X-API-KEY` = your MY_APP_AUTH_KEY
- **Response:** JSON with `places` list (structured) + `map_image` (PNG bytes as base64; save to file.png in client).

**Example Response:**
```json
{
  "places": [
    {
      "lat_lon": {"lat": 17.0891, "lon": 120.9774},
      "display_name": "Bontoc, ..."
    }
  ],
  "map_image": "iVBORw0KGgoAAAANSUhEUgAA... (bytes)"
}
```

### Rate Limiting Test
- Without auth key: Max 5 req/min -> 429 if exceeded.
- With valid auth: Unlimited.

## Troubleshooting

- **No .env keys:** Endpoint 500 "NoneType" - check .env loaded.
- **Invalid LocationIQ key:** 400 Geocoding error.
- **429 Too Many Requests:** Wait 1min (unauth only).
- **Validation Error:** Check `location` param required.
- Server not starting? `pip install -r requirements.txt` again.

## Team Members & Contributions
```

Angapilan, Sheena KAte - Programmer
Lampesa, Katryll
Angel, Clifford
Benito, Alejandro
Puyongan, Dariel
Saligen, Joe
