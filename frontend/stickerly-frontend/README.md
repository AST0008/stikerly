# Stikerly Frontend

React application for creating AI meme stickers and managing templates.

## Responsibilities

- User-facing sticker generation flow.
- Visual meme template selection.
- Upload preview and interactive loading states.
- Result preview with download/share actions.
- Admin interface for template upload, metadata save, and deletion.

## Stack

- React 19 + TypeScript
- Vite 7
- Tailwind CSS 4
- GSAP (`@gsap/react`)
- Lucide icons

## App structure

```text
src/
├── App.tsx          # main user flow and sticker creation UI
├── AdminPage.tsx    # admin upload/manage templates UI
├── index.css
├── App.css
└── AdminPage.css
```

## Routing model

The frontend uses a simple hash-based switch:

- `#` -> user sticker creator
- `#/admin` -> admin page

No external router dependency is used at this stage.

## Backend integration

Current API base in code: `http://localhost:8000`.

Primary calls:

- `GET /admin/templates` to populate template gallery.
- `POST /create-sticker` with `FormData(file, template_id?)`.
- Admin calls to `/admin/templates/upload`, `/admin/templates`, `/admin/templates/{id}`.

Expected sticker response fields:

- `status`
- `meme_selected`
- `final_meme_url`

## Local development

```bash
cd frontend/stickerly-frontend
npm install
npm run dev
```

Dev server runs at `http://localhost:5173`.

## Build and preview

```bash
npm run build
npm run preview
```

## Docker

Multi-stage build:

1. Build assets with Node 20 Alpine.
2. Serve static output with NGINX.

Run from repo root with Compose:

```bash
docker compose up -d --build frontend
```

Frontend container is exposed at `http://localhost:5173`.

## UX notes

- Drag-and-drop plus click-to-upload entry.
- Step-by-step loading messages during generation.
- Template gallery with search and sorting.
- WhatsApp deep-link sharing on result output.
- Admin key persisted in local storage for operator convenience.

## Next improvements

- Move API base URL to environment-driven config.
- Add stronger error boundaries and retry affordances.
- Introduce route-level code splitting once app grows.
- Add unit/integration coverage for critical UI flows.
