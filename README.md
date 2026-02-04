# Portfolio Backend

FastAPI backend for the portfolio admin panel and future chatbot integration.

## Setup

### 1. Create Python Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase service role key (not anon key!)
- `ADMIN_EMAIL`: Email address allowed to access admin
- `FRONTEND_URL`: Frontend URL for CORS (default: http://localhost:3000)

### 4. Setup Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to SQL Editor and run the contents of `schema.sql`
3. Copy your project URL and service role key to `.env`
4. Enable Email auth in Authentication > Providers
5. Create an admin user in Authentication > Users

### 5. Run the Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Public (Read)
- `GET /api/experiences` - All experiences with roles
- `GET /api/projects` - All projects
- `GET /api/projects/featured` - Featured projects only
- `GET /api/coolstuff` - All cool stuff items
- `GET /api/content` - All content
- `GET /api/skills` - All skills

### Admin (Write - requires Bearer token)
- `POST/PUT/DELETE /api/experiences/*`
- `POST/PUT/DELETE /api/projects/*`
- `POST/PUT/DELETE /api/coolstuff/*`
- `PUT /api/content/{id}`
- `POST/PUT/DELETE /api/skills/*`

## Authentication

All write endpoints require a Bearer token from Supabase Auth:

```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Authorization: Bearer YOUR_SUPABASE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Project", ...}'
```

The token is obtained from Supabase Auth on the frontend.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── config.py        # Settings
│   ├── database.py      # Supabase client
│   ├── auth.py          # Auth middleware
│   ├── models.py        # Pydantic models
│   └── routers/
│       ├── experiences.py
│       ├── projects.py
│       ├── coolstuff.py
│       └── content.py
├── schema.sql           # Database schema
├── requirements.txt
└── .env.example
```
