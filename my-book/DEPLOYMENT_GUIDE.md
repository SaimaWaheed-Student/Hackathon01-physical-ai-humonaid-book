# Deployment Guide

Complete instructions for deploying the Physical AI & Humanoid Robotics book to production.

## Deployment Options

### Option 1: Vercel (Recommended - Free + Premium)

Vercel is the easiest and recommended way to deploy Docusaurus.

**Setup:**

1. Create a Vercel account: https://vercel.com

2. Connect your GitHub repository:
   - Go to Vercel Dashboard
   - Click "New Project"
   - Select your GitHub repository
   - Click "Import"

3. Configure project settings:
   - **Framework**: Docusaurus
   - **Root Directory**: `./my-book`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. Set environment variables (optional):
   - Add any API keys needed for your site

5. Click "Deploy"

Vercel will automatically:
- Build on every push to main/master
- Deploy to production
- Create preview URLs for pull requests
- Provide a custom domain (or use vercel.app)

**Custom Domain:**
```bash
# Add to vercel.json
{
  "alias": ["yourdomain.com", "www.yourdomain.com"]
}
```

### Option 2: GitHub Pages (Free, Basic)

Deploy using GitHub's free hosting.

**Setup:**

1. Add to `docusaurus.config.ts`:
```typescript
const config: Config = {
  url: 'https://yourusername.github.io',
  baseUrl: '/1-hackathone-book/',
  organizationName: 'yourusername',
  projectName: '1-hackathone-book',
  // ...
};
```

2. Add deployment script to `package.json`:
```json
{
  "scripts": {
    "deploy": "docusaurus deploy"
  }
}
```

3. Deploy:
```bash
npm run deploy
```

4. Enable GitHub Pages in repository settings:
   - Settings → Pages
   - Source: `gh-pages` branch
   - Domain: Your custom domain (optional)

### Option 3: Docker + Kubernetes

For enterprise/large-scale deployments.

**Build Docker image:**
```bash
docker build -f docker/Dockerfile.docs -t physical-ai-book:latest .
docker tag physical-ai-book:latest yourusername/physical-ai-book:latest
docker push yourusername/physical-ai-book:latest
```

**Deploy to Kubernetes:**
```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: physical-ai-book
spec:
  replicas: 3
  selector:
    matchLabels:
      app: physical-ai-book
  template:
    metadata:
      labels:
        app: physical-ai-book
    spec:
      containers:
      - name: docs
        image: yourusername/physical-ai-book:latest
        ports:
        - containerPort: 3000
```

```bash
kubectl apply -f kubernetes/deployment.yaml
```

### Option 4: Self-Hosted (VPS/Cloud)

Deploy to your own server (AWS, Azure, DigitalOcean, etc.).

**Step-by-step:**

1. SSH into your server:
```bash
ssh user@your-server.com
```

2. Clone repository:
```bash
git clone https://github.com/yourusername/1-hackathone-book.git
cd 1-hackathone-book/my-book
```

3. Install Node.js:
```bash
curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

4. Build:
```bash
npm install
npm run build
```

5. Setup web server (Nginx):
```bash
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/default
```

Add:
```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        root /home/user/1-hackathone-book/my-book/build;
        index index.html index.htm;
        try_files $uri $uri/ =404;
    }
}
```

6. Restart Nginx:
```bash
sudo systemctl restart nginx
```

7. Setup SSL with Let's Encrypt:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## CI/CD Integration

GitHub Actions automatically deploys on push:

```yaml
# .github/workflows/build-and-deploy.yml
name: Deploy
on:
  push:
    branches: [main, master]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 20
      - run: cd my-book && npm ci && npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./my-book/build
```

## Domain & SSL

### Purchase Domain
- GoDaddy, Namecheap, Google Domains, etc.
- Point nameservers to your hosting provider

### SSL Certificate
- **Vercel**: Automatic
- **GitHub Pages**: Automatic
- **Self-hosted**: Use Let's Encrypt (free)

## Monitoring & Analytics

### Add Analytics (Optional)

1. **Google Analytics**:
   - Sign up: https://analytics.google.com
   - Add to `docusaurus.config.ts`:
   ```typescript
   gtag: {
     trackingID: 'G-XXXXXXXXXX',
     anonymizeIP: true,
   }
   ```

2. **Vercel Analytics**:
   - Enable in Vercel dashboard
   - Auto-integrated with Vercel hosting

## Maintenance

### Regular Updates

1. **Update dependencies**:
```bash
npm update
```

2. **Update Docusaurus**:
```bash
npm install @docusaurus/core@latest @docusaurus/preset-classic@latest
```

3. **Test locally**:
```bash
npm run build
npm run serve
```

4. **Deploy**:
```bash
git add .
git commit -m "Update dependencies"
git push
```

### Backup

- GitHub is your backup (all content in version control)
- Regular commits ensure you can revert if needed

## Troubleshooting

### Build fails
```bash
npm install --legacy-peer-deps
npm run build
```

### Port already in use
```bash
# Change port in docusaurus.config.ts or use environment variable
PORT=3001 npm start
```

### Large build size
- Compress images: `imagemin`
- Enable bundle splitting in webpack config
- Remove unused dependencies

## Performance Optimization

```bash
# Analyze bundle size
npm install --save-dev webpack-bundle-analyzer
npm run build -- --analyze
```

## Disaster Recovery

In case of emergency:

1. Clone from GitHub backup
2. Rebuild: `npm install && npm run build`
3. Deploy to staging first
4. Test thoroughly
5. Deploy to production

## Support

- **Vercel Support**: https://vercel.com/support
- **Docusaurus Docs**: https://docusaurus.io/docs
- **GitHub Pages Help**: https://docs.github.com/en/pages
