# Deployment Guide

This guide covers deploying Capital Support to various platforms.

## Table of Contents
- [Render (Recommended for Free)](#render-free)
- [Docker](#docker)
- [Local Development](#local-development)
- [Troubleshooting](#troubleshooting)

## Render (Free)

### Prerequisites
- GitHub account (repository is public)
- Render account (free)

### Step-by-Step Deployment

#### 1. Prepare Code
```bash
git add .
git commit -m "Deployment ready"
git push origin main
```

#### 2. Create Render Account
- Visit https://render.com
- Sign up with GitHub
- Authorize Render to access your repos

#### 3. Create PostgreSQL Database
1. Dashboard → **New +** → **PostgreSQL**
2. Configure:
   - Name: `capital-support-db`
   - Database: `capital_support`
   - User: `postgres`
   - Region: Choose closest region
   - Plan: **Free** ⭐
3. Click **Create Database**
4. Wait 2-3 minutes for creation
5. Copy the **Internal Database URL**

#### 4. Create Web Service
1. Dashboard → **New +** → **Web Service**
2. Connect your GitHub repository
3. Configure:
   ```
   Name:           capital-support
   Runtime:        Python 3
   Build Command:  pip install -r requirements.txt
   Start Command:  uvicorn app.app:app --host 0.0.0.0 --port $PORT
   Plan:           Free
   ```
4. Click **Create Web Service**

#### 5. Add Environment Variables
1. In Web Service settings, find **Environment** section
2. Add variable:
   - Key: `DATABASE_URL`
   - Value: Paste the PostgreSQL Internal URL from step 3
3. Click **Save Changes**

#### 6. Monitor Deployment
- Watch the deploy log in real-time
- App should be live in 2-5 minutes
- You'll see a URL like: `https://capital-support.onrender.com`

### ⚠️ Free Tier Limitations
- Apps spin down after 15 minutes of inactivity
- Takes ~30 seconds to wake up
- 0.5 CPU, 512MB RAM
- Database persists between restarts

### Upgrading to Paid (Optional)
- Standard tier: $7-12/month
- Always-on servers
- More resources
- Better performance

## Docker

### Build Image
```bash
docker build -t capital-support .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="sqlite+aiosqlite:///./test.db" \
  capital-support
```

### With Docker Compose
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/capital_support
  
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: capital_support
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run with: `docker-compose up`

## Local Development

### Setup
```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/CapitalSupport.git
cd CapitalSupport

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

### Access
- App: http://localhost:8000
- API Docs: http://localhost:8000/docs
- OpenAPI Schema: http://localhost:8000/openapi.json

### Database
- Default: SQLite at `./test.db`
- Auto-created on first run
- Tables created automatically via lifespan

## Alternative Platforms

### Railway.app
1. Connect GitHub repo
2. Add PostgreSQL plugin
3. Deploy similar to Render
4. Free tier: $5 credit/month

### Heroku (Paid)
1. `heroku create capital-support`
2. `heroku addons:create heroku-postgresql`
3. `git push heroku main`

### DigitalOcean App Platform
- App: $5-12/month
- Database: Managed PostgreSQL
- One-click deployment from GitHub

## Environment Variables

### Development
```env
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

### Production (PostgreSQL)
```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
```

## Troubleshooting

### Deployment Fails
1. Check Deploy Log for errors
2. Common issues:
   - Missing dependencies → update `requirements.txt`
   - Wrong start command → verify command syntax
   - Database connection error → check DATABASE_URL

### App Not Loading
- Give it 30 seconds (first load after spin-down)
- Check status in Render dashboard
- Look for "Server running" in logs

### Database Connection Error
- Verify `DATABASE_URL` is set correctly
- Ensure database is running
- Check PostgreSQL credentials match

### CORS Errors
- Check frontend URL in CORS config
- Update `app/app.py` if needed:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Static Files Not Loading
- Ensure `app/static/index.html` exists
- Check file permissions
- Verify root route is configured

## Performance Optimization

### Database
- Use connection pooling
- Index frequently queried columns
- Archive old payment records

### Frontend
- Minify CSS/JavaScript
- Cache API responses
- Lazy load components

### Server
- Enable gzip compression
- Use CDN for static files
- Monitor CPU/memory usage

## Monitoring

### Render Dashboard
- Real-time logs
- Resource usage (CPU, memory)
- Deployment history
- Custom metrics

### Manual Monitoring
- Test API: `curl https://your-app.onrender.com/docs`
- Check database: Connect with DB client
- Monitor logs: Check Render dashboard

## Backup & Recovery

### Database Backup
```bash
# PostgreSQL
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

### Application Backup
- Code: Stored in GitHub
- Database: Managed by Render
- Regular backups recommended for production

## Next Steps

1. ✅ Deploy to Render
2. ✅ Test all features
3. ✅ Set up custom domain (optional)
4. ✅ Monitor performance
5. ✅ Plan scaling if needed

---

For more help, check README.md or API docs at `/docs`
