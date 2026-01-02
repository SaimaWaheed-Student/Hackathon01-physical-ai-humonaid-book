# Vercel GitHub Integration Setup

If you're getting "Failed to fetch" error when importing your project to Vercel, follow these steps:

## Solution 1: Grant Vercel Access to GitHub Repository

### Step 1: Check GitHub Integration
1. Go to Vercel Dashboard: https://vercel.com/dashboard
2. Click on your profile icon (top right)
3. Select "Settings"
4. Go to "Git" tab
5. Under "Connected Git Accounts", check if GitHub is connected
6. If not connected, click "Connect GitHub Account"

### Step 2: Configure Repository Access
1. In Vercel Settings → Git → GitHub
2. Click "Adjust GitHub App Permissions" or "Configure GitHub App"
3. This will open GitHub in a new tab
4. Scroll down to "Repository access"
5. Choose one of:
   - **Option A**: "All repositories" (easiest)
   - **Option B**: "Only select repositories" → Select `Hackathon01-physical-ai-humonaid-book`
6. Click "Save"

### Step 3: Try Import Again
1. Go back to Vercel Dashboard
2. Click "Add New" → "Project"
3. You should now see your repository listed
4. Click "Import" next to your repository

## Solution 2: Direct Repository URL Method

If the above doesn't work, try importing directly:

1. Go to Vercel Dashboard
2. Click "Add New" → "Project"
3. If you don't see your repository:
   - Click "Import Third-Party Git Repository"
   - Enter: `https://github.com/SaimaWaheed-Student/Hackathon01-physical-ai-humonaid-book`
   - Click "Continue"

## Solution 3: Reinstall GitHub Integration

If still having issues:

### In Vercel:
1. Go to Settings → Git
2. Under GitHub, click "Disconnect"
3. Click "Connect GitHub Account" again
4. Follow the authorization steps

### In GitHub:
1. Go to GitHub Settings: https://github.com/settings/installations
2. Find "Vercel" in the list
3. Click "Configure"
4. Make sure your repository has access
5. Click "Save"

## Solution 4: Check Repository Permissions

Make sure the repository is accessible:

1. Go to your GitHub repository:
   https://github.com/SaimaWaheed-Student/Hackathon01-physical-ai-humonaid-book
2. Click "Settings" (repository settings, not profile)
3. Check that you have admin access
4. If it's a private repo, make sure Vercel has access

## Solution 5: Use Vercel CLI (Alternative Method)

If dashboard import still fails, use Vercel CLI:

### Install Vercel CLI:
```bash
npm install -g vercel
```

### Login to Vercel:
```bash
vercel login
```

### Deploy from Command Line:
```bash
cd "C:\Users\saima waheed\Desktop\1-hackathone-book\rag-book-chat"
vercel
```

Follow the prompts:
- Set up and deploy? Yes
- Which scope? Select your account
- Link to existing project? No
- Project name? rag-book-chat
- Directory? ./
- Override settings? No

### Set Environment Variables via CLI:
```bash
vercel env add QDRANT_URL
vercel env add QDRANT_API_KEY
vercel env add OPENROUTER_API_KEY
```

### Deploy to Production:
```bash
vercel --prod
```

## Common Issues

### "Repository not found"
- Make sure you're logged into the correct GitHub account
- Check repository name spelling
- Verify repository isn't private without proper access

### "Authentication failed"
- Disconnect and reconnect GitHub in Vercel settings
- Check GitHub personal access tokens
- Clear browser cache and try again

### "Access denied"
- Repository must not be archived
- You must have admin or write access
- Check organization permissions if repo is in an org

## Verification

After successful connection, you should:
1. See your repository in Vercel's import list
2. Be able to click "Import"
3. See the configuration screen with:
   - Framework Preset: Other
   - Root Directory: `rag-book-chat`
   - Build Command: (auto-detected)
   - Output Directory: (auto-detected)

## Next Steps

Once import is successful:
1. Set Root Directory to: `rag-book-chat`
2. Add environment variables (see VERCEL_DEPLOYMENT.md)
3. Click "Deploy"

## Need More Help?

- Vercel Documentation: https://vercel.com/docs/git/vercel-for-github
- GitHub App Settings: https://github.com/settings/installations
- Vercel Support: https://vercel.com/support
