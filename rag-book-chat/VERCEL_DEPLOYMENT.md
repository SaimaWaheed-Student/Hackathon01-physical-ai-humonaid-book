# Vercel Deployment Guide

This guide will help you deploy the RAG Book Chat backend to Vercel.

## Prerequisites

- A Vercel account (sign up at https://vercel.com)
- GitHub repository with the code
- Required API keys:
  - QDRANT_URL
  - QDRANT_API_KEY
  - OPENROUTER_API_KEY

## Deployment Steps

### 0. Setup GitHub Integration (IMPORTANT - Read First!)

**If you get "Failed to fetch" error**, see `VERCEL_GITHUB_SETUP.md` for detailed troubleshooting.

Quick setup:
1. Go to Vercel Dashboard → Settings → Git
2. Make sure GitHub is connected
3. Click "Adjust GitHub App Permissions"
4. Grant access to your repository: `Hackathon01-physical-ai-humonaid-book`
5. Save and return to Vercel

### 1. Import Project to Vercel

1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. You should see your GitHub repository listed
   - If not, click "Adjust GitHub App Permissions" and grant access
4. Click "Import" next to your repository
5. **IMPORTANT**: Set Root Directory to `rag-book-chat`
6. Framework Preset: Other (leave as default)

### 2. Configure Environment Variables

**IMPORTANT**: You'll be asked to add environment variables during the import process OR you can add them later in project settings.

#### During Import (Recommended):
After clicking "Import", before deploying, you'll see "Environment Variables" section. Add:

**Required (Must Add):**
- `QDRANT_URL` = Your Qdrant instance URL (e.g., https://xxx.cloud.qdrant.io)
- `QDRANT_API_KEY` = Your Qdrant API key
- `OPENROUTER_API_KEY` = Your OpenRouter API key

**Optional (Can use defaults):**
- `COLLECTION_NAME` = book_v1
- `EMBEDDING_MODEL` = text-embedding-3-small
- `LLM_MODEL` = anthropic/claude-3.5-sonnet

For each variable:
1. Enter the Name (e.g., QDRANT_URL)
2. Enter the Value (your actual key/URL)
3. Select Environment: Production, Preview, Development (or all)
4. Click "Add"

#### After Deployment:
If you skipped this step, go to:
1. Your project in Vercel Dashboard
2. Settings → Environment Variables
3. Add each variable with Name and Value
4. Click "Save"
5. Redeploy the project

### 3. Deploy

Click "Deploy" and Vercel will automatically:
- Install dependencies from `requirements.txt`
- Build the serverless functions
- Deploy your API

### 4. Test Your Deployment

Once deployed, you'll receive a URL like `https://your-project.vercel.app`

Test the health endpoint:
```bash
curl https://your-project.vercel.app/health
```

### 5. Update Frontend CORS

If you have a frontend, update the CORS settings in `app/main.py` to allow your frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Important Notes

- Vercel serverless functions have a 10-second execution timeout on the free tier
- For longer running requests, consider upgrading to a Pro plan
- The app uses serverless architecture, so there's no persistent in-memory state between requests
- Make sure to set up Qdrant vector database separately (Vercel doesn't host databases)

## API Endpoints

After deployment, your API will be available at:

- `GET /health` - Health check
- `POST /query` - Query the chatbot
- `POST /session` - Create a new session
- `GET /session/{session_id}` - Get session info
- `GET /books` - List ingested books
- `POST /ingest` - Ingest a new book
- `GET /audit/privacy` - Privacy audit
- `POST /admin/purge-sessions` - Purge expired sessions

## Troubleshooting

### "Failed to fetch" or GitHub import errors
- **See `VERCEL_GITHUB_SETUP.md` for complete troubleshooting guide**
- Quick fix: Go to Vercel Settings → Git → Adjust GitHub App Permissions
- Alternative: Use Vercel CLI to deploy (instructions in setup guide)

### Function timeout errors
- Optimize your queries
- Consider upgrading to Vercel Pro for 60-second timeouts

### Environment variable issues
- Double-check all environment variables are set correctly in Vercel dashboard
- Redeploy after adding/changing environment variables

### CORS errors
- Update the `allow_origins` in `app/main.py`
- Redeploy after making changes

## Monitoring

Use Vercel's built-in monitoring:
- Function logs: Available in the Vercel dashboard
- Analytics: Track function invocations and performance
- Error tracking: Automatic error capture

## Next Steps

1. Set up a custom domain in Vercel
2. Configure monitoring and alerts
3. Set up CI/CD for automatic deployments
4. Consider setting up a staging environment
