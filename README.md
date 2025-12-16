# Todo App - Phase II: Full-Stack Web Application

A full-stack todo application with multi-user authentication, built using spec-driven development with Claude Code and Spec-Kit Plus.

![Profile Views](https://komarev.com/ghpvc/?username=samade747&style=flat-square)

## Features

- Multi-user authentication with Better Auth
- Create, read, update, and delete tasks
- Filter tasks by status, priority, and tags
- Search tasks by title or description
- Sort tasks by various criteria
- Persistent storage with PostgreSQL/SQLite
- Responsive dark theme UI

## Tech Stack

### Frontend
- Next.js 14 (App Router)
- React 18
- Tailwind CSS
- Better Auth
- JavaScript

### Backend
- FastAPI
- SQLModel
- PostgreSQL (Neon) / SQLite
- JWT Authentication
- Python

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- PostgreSQL (optional, SQLite used by default for development)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Update the `.env` file with your configuration (especially `BETTER_AUTH_SECRET`)

6. Run the backend server:
   ```bash
   uvicorn uvicorn_app:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file based on `.env.example`:
   ```bash
   cp .env.example .env.local
   ```

4. Update the `.env.local` file with your configuration (especially `BETTER_AUTH_SECRET` - must match backend)

5. Run the development server:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

## API Endpoints

All endpoints require JWT authentication via `Authorization: Bearer <token>` header.

- `GET /api/{user_id}/tasks` - List tasks with optional filters
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

### Query Parameters for List Tasks

- `status`: Filter by "open" or "done"
- `priority`: Filter by "low", "medium", or "high"
- `tag`: Filter by tag
- `q`: Search in title/description
- `sort_by`: Sort by "created_at", "due_date", "priority", or "title"
- `order`: Sort order "asc" or "desc"

## Testing

### Backend Tests

```bash
cd backend
pytest
```

## Database

### SQLite (Development)

By default, the app uses SQLite for local development. The database file is created automatically at `backend/todo.db`.

### PostgreSQL (Production)

To use PostgreSQL (e.g., Neon), update the `DATABASE_URL` in the backend `.env` file:

```
DATABASE_URL=postgresql://user:password@host/database
```

## Project Structure

```
phase2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── tasks.py        # Task endpoints
│   │   ├── auth.py             # JWT authentication
│   │   ├── db.py               # Database connection
│   │   ├── main.py             # FastAPI app
│   │   ├── models.py           # SQLModel models
│   │   └── schemas.py          # Pydantic schemas
│   ├── tests/
│   │   └── test_tasks.py       # API tests
│   ├── requirements.txt
│   └── uvicorn_app.py
├── frontend/
│   ├── app/
│   │   ├── api/auth/[...all]/  # Better Auth routes
│   │   ├── signin/             # Sign in page
│   │   ├── signup/             # Sign up page
│   │   ├── todos/              # Tasks page
│   │   ├── layout.js           # Root layout
│   │   ├── page.js             # Home page
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   ├── Navbar.js           # Navigation bar
│   │   ├── TodoFilters.js      # Filter controls
│   │   ├── TodoForm.js         # Task form
│   │   ├── TodoItem.js         # Task item
│   │   └── TodoList.js         # Task list
│   ├── lib/
│   │   ├── api.js              # API client
│   │   ├── auth.js             # Better Auth server
│   │   └── auth-client.js      # Better Auth client
│   └── package.json
└── specs/                      # Specification files
```

## Environment Variables

### Backend

- `DATABASE_URL`: Database connection string
- `BETTER_AUTH_SECRET`: Shared secret for JWT verification (must match frontend)

### Frontend

- `BETTER_AUTH_SECRET`: Shared secret for JWT signing (must match backend)
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## Security

- All API endpoints require JWT authentication
- Users can only access their own tasks
- Passwords are hashed by Better Auth
- JWT tokens include user_id for authorization
- CORS is configured to allow frontend origin

## Development

This project follows spec-driven development principles:

1. Specifications are defined in `/specs`
2. Implementation follows the specs exactly
3. Changes to requirements must update specs first
4. Code is generated/modified by Claude Code based on specs

## License

This is a demonstration project for Hackathon II - Evolution of Todo.

![Profile Views](https://komarev.com/ghpvc/?username=samade747&style=flat-square)
