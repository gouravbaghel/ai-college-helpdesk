# Production Deployment Guide
## AI-Powered College Helpdesk & Student Assistant System

This guide outlines deployment procedures across local production servers, Docker containers, cloud platforms (Render, Railway, Streamlit Community Cloud), and Linux VPS instances.

---

## 1. Prerequisites & Environment Configuration

Ensure your environment configuration (`.env`) is configured with production secrets:

```ini
# Production Environment Variables (.env)
GROQ_API_KEY=gsk_your_groq_api_key_here
JWT_SECRET_KEY=generate_a_64_char_secure_random_hex_string
DATABASE_URL=sqlite:///./college_helpdesk.db
CHROMA_PERSIST_DIR=./chroma_db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.1
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
UPLOAD_DIR=./uploads
```

---

## 2. Option A: Docker Deployment (Recommended)

Both backend and frontend can be containerized and managed with Docker Compose.

### Step 1: Build & Launch
```bash
docker compose up -d --build
```

### Step 2: Verify Service Health
```bash
docker compose ps
```

- **Backend REST API:** `http://localhost:8000` (Interactive docs at `http://localhost:8000/docs`)
- **Frontend Web UI:** `http://localhost:8501`

### Step 3: View Container Logs
```bash
docker compose logs -f
```

### Step 4: Stop Containers
```bash
docker compose down
```

---

## 3. Option B: Single-Command Local / Dedicated Server Launcher

A unified supervisor runner is provided in `run_all.py` to start both the FastAPI backend and Streamlit UI concurrently with clean process signal handling:

```bash
# 1. Activate your virtual environment
source venv/bin/activate     # Linux / macOS
venv\Scripts\activate        # Windows

# 2. Run both services
python run_all.py
```

---

## 4. Option C: Cloud Deployment (Render Blueprint)

The repository includes a ready-to-use `render.yaml` specification.

1. Push your repository to **GitHub** or **GitLab**.
2. Sign in to [Render.com](https://render.com).
3. Click **New +** $\rightarrow$ **Blueprint**.
4. Select your repository. Render will automatically detect `render.yaml` and provision:
   - `college-helpdesk-api` (FastAPI REST service on Python 3.11)
   - `college-helpdesk-ui` (Streamlit frontend automatically wired to the backend URL)
5. Add your `GROQ_API_KEY` under the backend environment variable settings.

---

## 5. Option D: Linux VPS Deployment (Ubuntu + Nginx + Systemd)

For production deployment on an Ubuntu VPS with SSL:

### Step 1: Systemd Service for FastAPI (`/etc/systemd/system/helpdesk-api.service`)
```ini
[Unit]
Description=College Helpdesk FastAPI Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/ai-college-helpdesk
ExecStart=/var/www/ai-college-helpdesk/venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
EnvironmentFile=/var/www/ai-college-helpdesk/.env

[Install]
WantedBy=multi-user.target
```

### Step 2: Systemd Service for Streamlit (`/etc/systemd/system/helpdesk-ui.service`)
```ini
[Unit]
Description=College Helpdesk Streamlit Frontend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/ai-college-helpdesk
ExecStart=/var/www/ai-college-helpdesk/venv/bin/streamlit run frontend/app.py --server.port 8501 --server.address 127.0.0.1 --server.headless true
Restart=always
Environment="API_BASE_URL=http://127.0.0.1:8000/api"

[Install]
WantedBy=multi-user.target
```

### Step 3: Enable and Start Services
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now helpdesk-api helpdesk-ui
```

### Step 4: Nginx Reverse Proxy (`/etc/nginx/sites-available/helpdesk`)
```nginx
server {
    server_name helpdesk.yourcollege.edu.in;

    # Streamlit Frontend
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;
    }

    # FastAPI REST Endpoints
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Step 5: SSL Certificate
```bash
sudo certbot --nginx -d helpdesk.yourcollege.edu.in
```

---

## 6. Verification & Health Monitoring

- API Health Check: `GET /health` $\rightarrow$ `{"status": "healthy"}`
- RAG Automated Diagnostic: `python -m tests.test_rag_evaluation`
