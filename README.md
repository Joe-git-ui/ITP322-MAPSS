To create the file:
1.Open Sublime Text (or your preferred editor).
2.Create a New File.
3.Paste the content below into that file.
4.Save it as README.md in your MAPS folder.

# [cite_start]ITP 322: Group 1 - Google Maps Integration [cite: 1, 7]

### [cite_start]Systems Integration and Architecture 2 [cite: 1]

## Project Description

[cite_start]This project demonstrates the integration of a Geocoding API (LocationIQ) into a FastAPI application[cite: 4, 38]. [cite_start]It serves as a production-ready endpoint that converts location names into geographic coordinates while maintaining strict security and usage standards[cite: 4].

## [cite_start]Features [cite: 21]

- [cite_start]**Geocoding Search:** Real-time retrieval of latitude and longitude data[cite: 33].
- [cite_start]**Secure Authentication:** Implementation of API Key security[cite: 15, 31].
- [cite_start]**Rate Limiting:** Protection against service abuse (5 requests/minute).
- [cite_start]**Automated Documentation:** Full Swagger UI integration via `/docs`[cite: 13, 25].

## [cite_start]Prerequisites [cite: 22]

- Python 3.10+
- FastAPI & Uvicorn
- `python-dotenv` for environment variable management
- `slowapi` for rate limiting

## [cite_start]Installation Instructions [cite: 23]

1.  [cite_start]**Clone the Repository:** [cite: 36]
    ```bash
    git clone <your-repo-url>
    cd MAPS
    ```
2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install fastapi uvicorn httpx python-dotenv slowapi
    ```

## [cite_start]Configuration Guide [cite: 24]

[cite_start]Create a `.env` file in the root directory [cite: 36] and configure your credentials:

```env
LOCATIONIQ_API_KEY=pk.7293a24df586127cfbb0ca222ef9e15e
MY_APP_AUTH_KEY=a_secret_password_for_your_fastapi_endpoint


API Endpoints Documentation

GET /search

Description: Fetches geocoding data for a specific location.Query Param: location (e.g., "Bontoc")Header Required: X-API-KEY Response Example:
JSON{
  "lat": "17.0891276",
  "lon": "120.9773940",
  "display_name": "Bontoc, Mountain Province, Philippines"
}


Authentication & Rate Limiting
 Authentication: We utilized API Key Authentication. The server validates the X-API-KEY header against the stored environment variable before processing requests.
 Rate Limiting: To prevent abuse, we implemented a limit of 5 requests per minute per user.

 Testing Instructions
 1. Start the server: uvicorn main:app --reload
 2. Open http://127.0.0.1:8000/docs.
 3. Click the Authorize button and enter your MY_APP_AUTH_KEY.
 4.Execute the /search endpoint to see the live data flow.

 Troubleshooting

 403 Forbidden: Verify your API Key in the Authorize section.
 429 Rate Limit: Wait 60 seconds if you exceed 5 requests in a minute.

 Team Members & Contributions
```

Angapilan, Sheena KAte - Programmer
Lampesa, Katryll
Angel, Clifford
Benito, Alejandro
Puyongan, Dariel
Saligen, Joe
