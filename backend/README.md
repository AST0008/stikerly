# Stikerly Backend

FastAPI service responsible for sticker generation, template administration, and trend ingestion.

## Responsibilities

- Accept user image uploads and generate final sticker output.
- Manage template metadata in MongoDB.
- Ingest trending meme assets from Reddit and GIPHY.
- Run scheduled background jobs for cleanup and feed refresh.

## Stack

- FastAPI
- Gunicorn + Uvicorn workers
- OpenCV, MediaPipe, Pillow, rembg, DeepFace
- APScheduler
- MongoDB (PyMongo)
- Cloudinary

## Service layout

```text
backend/
├── app/
│   ├── main.py                # app startup, routing, CORS, scheduler
│   ├── config.py              # directories, allowed extensions, constants
│   ├── database.py            # MongoDB client and collections
│   ├── routes/
│   │   ├── sticker.py         # public sticker generation endpoints
│   │   └── admin.py           # template and ingestion admin endpoints
│   ├── services/
│   │   ├── face.py            # face detection, crop, feathering
│   │   ├── meme_manager.py    # template selection logic
│   │   ├── meme_fetcher.py    # Reddit and GIPHY ingestion
│   │   └── cleanup.py         # uploads cleanup job
│   └── models/template.py     # Pydantic models
├── assets/templates/          # local template files (if used)
├── uploads/                   # temporary processing files
└── Dockerfile
```

## API endpoints

### Public

- `GET /` - health check
- `GET /templates` - list templates
- `POST /create-sticker` - generate sticker from uploaded image

`POST /create-sticker` form fields:

- `file` (required)
- `template_id` (optional)

### Admin (`x-admin-key` required)

- `POST /admin/templates/upload` - upload template image, detect face slot
- `POST /admin/templates` - save template metadata
- `DELETE /admin/templates/{template_id}` - delete template metadata
- `POST /admin/memes/fetch/reddit` - ingest from Reddit
- `POST /admin/memes/fetch/giphy` - ingest from GIPHY

### Public read route under admin prefix

- `GET /admin/templates` - read-only template list for frontend

## Core pipeline

1. Validate image extension.
2. Run emotion detection (`DeepFace`) to guide template selection.
3. Remove background (`rembg`).
4. Detect faces (`MediaPipe`) and select dominant face.
5. Crop with padding and feather edges.
6. Load selected template and apply placement/rotation from `face_slot`.
7. Resize to 512x512 with transparent letterboxing.
8. Export WebP and upload to Cloudinary.
9. Return hosted URL in API response.

## Environment variables

Required for normal operation:

```env
MONGO_URI=...
DB_NAME=stikerly
ADMIN_KEY=change-me
ALLOWED_ORIGINS=http://localhost:5173

CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

GIPHY_API_KEY=...
```

Optional fetch controls:

```env
MEME_REDDIT_SUBREDDITS=MemeEconomy,memes,dankmemes
MEME_REDDIT_LIMIT=15
MEME_REDDIT_TIMEFRAME=day
MEME_GIPHY_LIMIT=10
```

## Run locally

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open API docs:

- `http://localhost:8000/docs`

## Run with Docker

From repository root:

```bash
docker compose up -d --build backend mongodb
```

API available at `http://localhost:8000`.

## Operational notes

- Scheduler starts on app startup and registers:
  - periodic Reddit fetch,
  - periodic GIPHY fetch,
  - cleanup job for temporary uploads.
- Current cleanup retention in code is 24 hours.
- Template selection falls back to random templates with valid `face_slot` when no direct emotion match exists.

## Known hardening tasks

- Move admin auth from shared key to role-based auth.
- Add request rate limits and upload size guardrails.
- Add structured logging and metrics/tracing.
- Externalize long-running work to async workers for higher throughput.
