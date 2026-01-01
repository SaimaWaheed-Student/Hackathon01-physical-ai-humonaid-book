# Backend Deployment Guide

This guide walks you through deploying the RAG chatbot backend to Render.

## Prerequisites

- GitHub account
- Render account (free): https://render.com
- Qdrant Cloud account (free): https://cloud.qdrant.io
- OpenRouter API key: https://openrouter.ai

## Step 1: Push Code to GitHub

The code is already pushed to your GitHub repository.

## Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

## Step 3: Deploy to Render

### Option A: Using render.yaml (Recommended)

1. Go to https://dashboard.render.com
2. Click **New** → **Blueprint**
3. Connect your GitHub repository: `Hackathon01-physical-ai-humonaid-book`
4. Render will detect `rag-book-chat/render.yaml`
5. Click **Apply**

### Option B: Manual Setup

1. Go to https://dashboard.render.com
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `rag-book-chat`
   - **Root Directory**: `rag-book-chat`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

## Step 4: Add Environment Variables

In Render dashboard, go to your service → **Environment** and add:

```
QDRANT_URL=https://your-qdrant-url.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key
OPENROUTER_API_KEY=your-openrouter-api-key
COLLECTION_NAME=book_v1
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=anthropic/claude-3.5-sonnet
```

### Get Your API Keys

**Qdrant:**
1. Go to https://cloud.qdrant.io
2. Create a free cluster
3. Copy the URL and API key

**OpenRouter:**
1. Go to https://openrouter.ai/keys
2. Create an API key
3. Add credits ($5 minimum)

## Step 5: Deploy

1. Click **Create Web Service**
2. Wait for deployment (3-5 minutes)
3. You'll get a URL like: `https://rag-book-chat.onrender.com`

## Step 6: Ingest Your Book

After deployment, ingest your book data:

```bash
# Update the script to use your production URL
export BACKEND_URL=https://rag-book-chat.onrender.com

# Run ingestion locally (it will upload to Qdrant Cloud)
python scripts/ingest_book.py docs/sample-book.txt --book-id my-book
```

## Step 7: Test the API

```bash
# Health check
curl https://rag-book-chat.onrender.com/health

# Test query
curl -X POST https://rag-book-chat.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Physical AI?",
    "book_id": "my-book"
  }'
```

## Step 8: Update Frontend

Update the frontend to use your production backend URL in:
`my-book/src/components/ChatbotWidget/ChatbotWidget.jsx`

```javascript
const API_BASE_URL = 'https://rag-book-chat.onrender.com';
```

## Monitoring

- **Logs**: Render Dashboard → Your Service → Logs
- **Metrics**: Render Dashboard → Your Service → Metrics
- **Health**: https://rag-book-chat.onrender.com/health

## Free Tier Limits

Render free tier includes:
- 750 hours/month (enough for 1 service running 24/7)
- Spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds

## Troubleshooting

### Service won't start
- Check logs in Render dashboard
- Verify all environment variables are set
- Check that requirements.txt has all dependencies

### CORS errors
- The backend already has CORS enabled for all origins
- Check browser console for exact error

### Qdrant connection fails
- Verify QDRANT_URL includes port (`:6333`)
- Verify QDRANT_API_KEY is correct
- Check Qdrant Cloud dashboard for cluster status

### OpenRouter API errors
- Verify API key is correct
- Check you have credits in your account
- Monitor usage at https://openrouter.ai/activity

## Cost Optimization

**Free Services:**
- Render: Free tier
- Qdrant Cloud: 1GB free cluster
- GitHub Pages: Free for public repos

**Paid Services:**
- OpenRouter: Pay per use (~$0.50-2.00 per 1000 queries)

## Next Steps

1. Deploy backend to Render
2. Configure environment variables
3. Ingest your book
4. Update frontend with backend URL
5. Redeploy GitHub Pages with updated config
6. Test end-to-end!
