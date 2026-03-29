# Stikerly - Full-Stack Application

## Deployment via Docker Compose

We have fully containerized both the overarching Stikerly application (Frontend React + Backend FastAPI) for seamless production deployment using `Docker Compose`.

### Instructions:
1. Ensure you have your `backend/.env` securely populated with all MongoDB, Giphy, and Cloudinary keys as intended. 
2. Simply move into the root folder (this folder) and launch the containers:

```bash
docker compose up -d --build
```

### Architecture
- **Backend (API):** Available via `http://localhost:8000` (Powered by 4-worker Gunicorn + FastAPI)
- **Frontend (Web):** Available via `http://localhost:5173` (Powered by optimized React Vite + NGINX)

All generated image assets and meme templates from the backend are preserved natively inside permanent Docker Volumes (`backend_uploads`, `backend_assets`).
