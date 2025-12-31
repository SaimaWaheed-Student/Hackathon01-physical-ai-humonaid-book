# 🚀 Quick Start Guide

## Installation (One-time setup)

```bash
# 1. Navigate to project
cd my-book

# 2. Install dependencies
npm install

# Done! You're ready to go.
```

---

## Development (Day-to-day)

### Start Development Server
```bash
npm start
```
Then open: http://localhost:3000

### Build for Production
```bash
npm run build
```

### Serve Built Version Locally
```bash
npm run serve
```

---

## Deployment (3 Easy Options)

### Option A: Vercel (Recommended - 5 minutes)
```bash
# Install Vercel CLI (one-time)
npm i -g vercel

# Deploy (automatic on push to GitHub)
vercel --prod
```

### Option B: GitHub Pages (2 minutes)
```bash
npm run deploy
```

### Option C: Docker (30 minutes)
```bash
# Build and run docs in Docker
docker-compose build
docker-compose up docs
```

---

## Learning Modules

### Run Module 1 (ROS 2)
```bash
docker-compose run module-1
```

### Run Module 3 (GPU-accelerated AI)
```bash
docker-compose run --gpus all module-3
```

---

## File Guide

| File | Purpose |
|------|---------|
| `docs/` | All course content (lessons, exercises, quizzes) |
| `src/components/` | React components (CodeSandbox, Quiz, VideoEmbed, etc.) |
| `.github/workflows/` | Automated CI/CD pipelines |
| `docker/` | Docker images for each module |
| `sidebars.ts` | Navigation structure |
| `docusaurus.config.ts` | Site configuration |
| `FINAL_SUMMARY.md` | Complete project overview |
| `DEPLOYMENT_GUIDE.md` | Production deployment instructions |
| `DOCKER_SETUP.md` | Docker usage guide |

---

## Key Features

✅ **Module 1 Complete**: 3 lessons + 8 exercises + 10-question quiz + capstone
✅ **React Components**: CodeSandbox, URDFViewer, Quiz, VideoEmbed, AudioPlayer
✅ **Automated CI/CD**: GitHub Actions for builds and deployment
✅ **Docker Ready**: Containerized environments for all 4 modules
✅ **Production Ready**: Deploy to Vercel, GitHub Pages, or self-hosted

---

## First Time Running?

1. **Development**:
   ```bash
   npm start
   ```

2. **Production Build**:
   ```bash
   npm run build
   npm run serve
   ```

3. **Docker**:
   ```bash
   docker-compose up docs
   ```

4. **Deploy**:
   - **Vercel**: `vercel --prod`
   - **GitHub Pages**: `npm run deploy`

---

## Troubleshooting

### Port 3000 in use?
```bash
PORT=3001 npm start
```

### Build fails?
```bash
npm install --legacy-peer-deps
npm run build
```

### Clear cache?
```bash
npm run clear
npm install
npm start
```

---

## Next Steps

1. ✅ Local testing: `npm start`
2. ✅ Production build: `npm run build`
3. ✅ Deploy to Vercel: `vercel --prod`
4. 🔄 Add Modules 2-4 content
5. 🎉 Launch!

---

## Commands Reference

```bash
# Development
npm start              # Start dev server
npm run build          # Build for production
npm run serve          # Serve production build
npm run clear          # Clear build cache
npm run typecheck      # Check TypeScript types

# Docker
docker-compose build   # Build all Docker images
docker-compose up docs # Run documentation website
docker-compose run module-1  # Run Module 1 environment

# Deployment
vercel --prod         # Deploy to Vercel
npm run deploy        # Deploy to GitHub Pages
```

---

## Support

- 📖 **Documentation**: See `FINAL_SUMMARY.md` and `DEPLOYMENT_GUIDE.md`
- 🐳 **Docker Help**: See `DOCKER_SETUP.md`
- 🚀 **Deployment**: See `DEPLOYMENT_GUIDE.md`
- 💻 **Development**: See individual lesson files in `docs/`

---

## 📊 Project Status

| Component | Status |
|-----------|--------|
| Module 1 (ROS 2) | ✅ Complete |
| React Components | ✅ Complete |
| Docker Setup | ✅ Complete |
| CI/CD Pipelines | ✅ Complete |
| Documentation | ✅ Complete |
| **Overall** | **✅ Production Ready** |

---

**You're all set! Start with `npm start` and happy learning! 🎓**
