# Naukri Resume Automation

Automated script to update your resume on Naukri.com using Playwright.

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd CvCron_version2
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install playwright python-dotenv pyyaml
   playwright install
   ```

4. **Configure credentials**
   ```bash
   cp .env.example .env
   # Edit .env file with your Naukri credentials
   ```

5. **Add your resume**
   ```bash
   mkdir resumes
   # Copy your resume PDF to resumes/latest_resume.pdf
   ```

## Usage

### Local Usage
Run the automation:
```bash
python -m src.test_naukri
```

### GitHub Actions (Automated)

#### Setup GitHub Secrets
1. Go to your repository → Settings → Secrets and variables → Actions
2. Add these secrets:
   - `NAUKRI_EMAIL`: Your Naukri email
   - `NAUKRI_PASSWORD`: Your Naukri password
   - `RESUME_URL`: Direct download link to your resume

#### Setup Resume URL
1. Upload your resume to Google Drive
2. Right-click → "Get link" → "Anyone with the link can view"
3. Convert the link:
   - From: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
   - To: `https://drive.google.com/uc?export=download&id=FILE_ID`
4. Use the converted link as `RESUME_URL` secret

#### Run Automation
- **Automatic**: Runs daily at 5:00 AM IST
- **Manual**: Go to Actions tab → "Naukri Resume Automation" → "Run workflow"

## Security

- Never commit your `.env` file
- Store credentials in GitHub Secrets for Actions
- Keep your credentials secure
- The `.gitignore` file protects sensitive data

## Files Structure

- `src/` - Main source code
- `logs/` - Automation logs and screenshots
- `resumes/` - Your resume files
- `config/` - Configuration files
- `.env` - Your credentials (not in Git)