# Deployment Guide

## Render.com Setup

### 1. Deploy to Render
1. Push code to GitHub
2. Go to [Render.com](https://render.com)
3. Connect GitHub repository
4. Choose "Web Service"
5. Use these settings:
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

### 2. Environment Variables
Add these in Render dashboard:
- `NAUKRI_EMAIL`: Your Naukri email
- `NAUKRI_PASSWORD`: Your Naukri password  
- `HEADLESS`: `true`

### 3. Get Your URL
After deployment, you'll get a URL like:
`https://your-app-name.onrender.com`

## Cron-job.org Setup

### 1. Create Account
1. Go to [cron-job.org](https://console.cron-job.org)
2. Sign up for free account

### 2. Create Cron Job
1. Click "Create cronjob"
2. **URL**: `https://your-app-name.onrender.com/update-resume`
3. **Schedule**: `0 9 * * *` (9 AM daily)
4. **Method**: POST
5. **Title**: "Naukri Resume Update"
6. Save

## Testing

### Test Endpoints
- Health check: `GET https://your-app-name.onrender.com/health`
- Manual trigger: `POST https://your-app-name.onrender.com/update-resume`

### Local Testing
```bash
python app.py
# Visit http://localhost:5000
```

## Resume File

Since Render doesn't have persistent storage, you have two options:

### Option 1: Embed in Code
Place `latest_resume.pdf` in `resumes/` folder and deploy with code.

### Option 2: URL Download (Recommended)
Add environment variable:
- `RESUME_URL`: Direct download link to your resume

The app will download the resume before each update.