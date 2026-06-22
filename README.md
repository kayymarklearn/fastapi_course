# fastapi-course

A social media API — users, posts, upvotes. Built as part of a FastAPI course.

## what this is

You can register an account, log in, create posts, list/search through them, and upvote posts. Posts are owned by whoever created them — you can only edit or delete your own. Authentication is handled with JWT tokens, passwords are hashed with argon2, and it all sits on top of PostgreSQL with SQLAlchemy handling the queries.

There's also a full frontend built with Vue 3, TypeScript, and Tailwind CSS. It lives in the `frontend/` directory.

## what's in the repo

```
app/
  main.py          # FastAPI app, CORS setup, router includes
  config.py        # Reads environment variables
  database.py      # SQLAlchemy engine and session
  models.py        # ORM models (User, Post, Vote)
  schemas.py       # Pydantic models for request/response
  oauth2.py        # JWT creation and verification
  utils.py         # Password hashing
  routers/
    auth.py        # POST /login
    post.py        # CRUD for /posts
    user.py        # POST /users, GET /users/{id}, GET /users/me
    vote.py        # POST /vote

frontend/          # Vue 3 + TypeScript + Tailwind CSS frontend
  src/
    api/           # Axios client, auth/posts/votes API calls
    components/    # Navbar, PostCard, VoteButton
    router/        # Vue Router config with lazy-loaded routes
    stores/        # Pinia auth store (token + user state)
    types/         # TypeScript interfaces matching the backend schemas
    views/         # Login, Register, Posts list, Post detail, Create/Edit

alembic/           # Database migrations (6 revisions)
compose.yml        # Dev compose config (hot-reload, hardcoded env)
compose.example.yml   # Prod compose config (reads .env, runs migrations on start)
Dockerfile
```

## running it

### with docker (easiest)

The dev compose file has everything hardcoded so you can literally just run it:

```bash
docker compose up
```

That starts the API on port 8000 and a PostgreSQL 18 container. The API auto-reloads when you change files because the code directory is mounted as a volume.

For something closer to production, there's a second compose file that reads from `.env`, adds a healthcheck on postgres, and runs `alembic upgrade head` on startup:

```bash
cp .env .env         # make sure it exists (it's already there if you cloned the repo)
docker compose -f compose.example.yml up
```

### frontend

With the backend running (Docker or otherwise), start the frontend dev server:

```bash
cd frontend
npm install    # first time only
npm run dev
```

That starts Vite on `localhost:5173` and proxies `/api` requests to the backend at `localhost:8000`. Open the browser and you'll see the login page — create an account, then start posting.

### without docker

You'll need a PostgreSQL instance running somewhere. Then:

```bash
uv run uvicorn app.main:app --reload
```

Make sure your `.env` points at the right database. Run migrations first:

```bash
alembic upgrade head
```

The .env file in the repo has throwaway credentials that work for local dev. Change the SECRET_KEY if you're putting this anywhere real — the one in there was generated for a tutorial and is definitely floating around on the internet.

## endpoints

All the POST/PUT/DELETE endpoints except `/users` and `/login` require a Bearer token. Hit `/login` with email and password, get a token back, then send it in the `Authorization` header.

| method | path | auth | what it does |
|--------|------|------|-------------|
| POST | `/users` | no | create an account |
| GET | `/users/{id}` | no | get a user by id |
| GET | `/users/me` | yes | get the currently authenticated user |
| POST | `/login` | no | get a JWT token |
| GET | `/posts` | yes | list posts (supports `?limit=`, `?skip=`, `?search=`) |
| POST | `/posts` | yes | create a post |
| GET | `/posts/{id}` | yes | get one post |
| PUT | `/posts/{id}` | yes | update your own post |
| DELETE | `/posts/{id}` | yes | delete your own post |
| POST | `/vote` | yes | upvote a post (`{"post_id": 1, "dir": 1}`) or remove vote (`dir: 0`) |

The post listing endpoints return a `votes` count alongside each post — that's a LEFT JOIN on the votes table, not a cached counter, so it's always accurate.

## environment variables

| variable | default | needed? |
|----------|---------|---------|
| DATABASE_HOSTNAME | localhost | optional |
| DATABASE_PORT | 5432 | optional |
| DATABASE_PASSWORD | — | yes |
| DATABASE_NAME | — | yes |
| DATABASE_USERNAME | postgres | optional |
| SECRET_KEY | — | yes (change before deploying) |
| ALGORITHM | HS256 | optional |
| ACCESS_TOKEN_EXPIRE_MINUTES | 30 | optional |

## a few notes

- The compose.yml has env vars inline for convenience. The .env.example is the template to copy.
- The API returns 403 if you try to modify someone else's post, not 404. This is intentional — leaking whether a post exists is worse than saying "you can't touch this." The frontend hides edit/delete buttons for posts you don't own, so you'll only ever see the 403 if you hit the API directly.
- Migrations are sequential and have already been applied in the repo. If you're starting fresh, `alembic upgrade head` will run all six.
