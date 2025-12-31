# RAG Chatbot Integration Guide

**Chatbot Widget نے `my-book` Docusaurus website میں embed کیا گیا ہے!**

---

## 📋 What Was Added

### New Files Created

```
my-book/
├── src/
│   ├── components/
│   │   └── ChatbotWidget/           ← NEW
│   │       ├── ChatbotWidget.jsx     (React component)
│   │       ├── ChatbotWidget.module.css (Styling)
│   │       └── index.js             (Export)
│   └── theme/
│       └── Root.jsx                 ← NEW (Wrapper to add chatbot everywhere)
```

### What Changed

- Updated `docusaurus.config.ts` to use custom Root component
- Chatbot widget automatically appears on all pages (bottom-right corner)

---

## 🚀 Setup Steps

### Step 1: Ensure Backend is Running

```bash
# Terminal 1: Navigate to rag-book-chat
cd "C:\Users\saima waheed\Desktop\1-hackathone-book\rag-book-chat"

# Start backend on port 8001
uvicorn app.main:app --port 8001 --reload
```

### Step 2: Ingest the Book

Before using the chatbot, you need to ingest a book with ID `my-book`:

```bash
# Terminal 2: Create or prepare your book file
# Option A: Use existing book
python scripts/ingest_book.py path/to/your/book.pdf --book-id my-book

# Option B: Use a text file
python scripts/ingest_book.py path/to/book.txt --book-id my-book
```

**Expected output:**
```
✅ Book ingested successfully
✅ Chunks created and embedded
✅ Stored in Qdrant
```

### Step 3: Install Dependencies (if needed)

```bash
# Terminal 2: Navigate to my-book
cd "C:\Users\saima waheed\Desktop\1-hackathone-book\my-book"

# Install dependencies (first time only)
npm install
```

### Step 4: Start Docusaurus Development Server

```bash
# Terminal 2: Start the website
npm start

# Site opens automatically at: http://localhost:3000
```

### Step 5: Test the Chatbot

1. **Navigate** to http://localhost:3000
2. **Look for** the 💬 button in bottom-right corner
3. **Click** to expand the chatbot widget
4. **Verify** status shows "✅ Connected"
5. **Ask** a question like: "What is Chapter 1 about?"

---

## 💬 Using the Chatbot

### Basic Usage

1. **Expand Widget**: Click 💬 button in bottom-right
2. **Type Question**: Enter your question
3. **Get Answer**: Chatbot returns answer with sources
4. **Minimize**: Click minus button to collapse

### Selection-Based Context

1. **Select Text**: Highlight any text on the page
2. **Ask Question**: The selected text will be used as primary context
3. **See Response**: Answer will reference the selected passage

### Features

✅ **Connected Status**: Green dot shows backend connection
✅ **Source Citations**: Shows page numbers and relevance scores
✅ **Fallback Response**: ⚠️ badge when using general knowledge
✅ **Typing Animation**: Visual feedback while waiting for response
✅ **Minimize/Maximize**: Space-saving compact mode

---

## 🔧 Configuration

### Backend URL

If backend runs on different URL, edit:

**File**: `src/components/ChatbotWidget/ChatbotWidget.jsx`

```javascript
const API_BASE_URL = 'http://localhost:8001';  // Change this
const BOOK_ID = 'my-book';                     // Change this if needed
```

### Book ID

If your book has different ID:

```javascript
const BOOK_ID = 'your-book-id';  // Your ingested book ID
```

---

## 📊 Architecture

```
my-book (Docusaurus Website)
│
├── docs/                    ← Documentation pages
├── src/components/
│   └── ChatbotWidget/       ← Widget component
│       ├── ChatbotWidget.jsx (React)
│       └── ChatbotWidget.module.css (Styles)
├── src/theme/
│   └── Root.jsx             ← Wraps all pages with chatbot
│
└── rag-book-chat (Backend API)
    ├── app/main.py          ← FastAPI server
    ├── app/rag.py           ← RAG pipeline
    └── app/ingestion.py     ← Book ingestion
```

**Flow:**
```
User navigates to page
    ↓
Root.jsx renders page + ChatbotWidget
    ↓
ChatbotWidget connects to backend (http://localhost:8001)
    ↓
User asks question
    ↓
Question → Backend → Qdrant (search) → OpenRouter (LLM)
    ↓
Response with sources → Chatbot displays
```

---

## 🐛 Troubleshooting

### Problem: Chatbot shows "⚠️ Cannot connect to backend"

**Solution:**
```bash
# 1. Check if backend is running
curl http://localhost:8001/health

# 2. If not running, start it
cd rag-book-chat
uvicorn app.main:app --port 8001

# 3. Verify book is ingested
curl http://localhost:8001/books
```

### Problem: No response from chatbot

**Solution:**
1. Check backend console for errors
2. Verify book was ingested: `curl http://localhost:8001/books`
3. Check browser console (F12) for error messages
4. Ensure API keys are configured in `rag-book-chat/.env`

### Problem: Port 3000 already in use

**Solution:**
```bash
# Use different port
npm start -- --port 4000

# Then visit: http://localhost:4000
```

### Problem: "offline" status appears

**Solution:**
1. Verify backend is running on `http://localhost:8001`
2. Check for CORS errors in browser console
3. Ensure `.env` file is properly configured with API keys

---

## 📁 Frontend Structure

### ChatbotWidget Component

```
ChatbotWidget.jsx
├── State Management
│   ├── messages (chat history)
│   ├── question (current input)
│   ├── isConnected (backend status)
│   ├── sessionId (chat session)
│   └── selectedText (context)
│
├── Main Functions
│   ├── initializeChatbot() - Connect to backend
│   ├── createSession() - Create chat session
│   ├── handleSendQuestion() - Send query
│   └── renderMessage() - Display messages
│
└── UI Components
    ├── Header (status + controls)
    ├── Messages Container
    ├── Input Area
    └── Welcome Message
```

### CSS Styling

- **Position**: Fixed bottom-right (`position: fixed; bottom: 20px; right: 20px;`)
- **Theme**: Purple/blue gradient matching Docusaurus
- **Responsive**: Full-screen on mobile (max-width: 600px)
- **Dark Mode**: Automatically adapts to Docusaurus dark theme

---

## ✅ Testing Checklist

- [ ] Backend running on `http://localhost:8001`
- [ ] Book ingested with ID `my-book`
- [ ] Dependencies installed: `npm install`
- [ ] Docusaurus dev server started: `npm start`
- [ ] Website opens at `http://localhost:3000`
- [ ] Chatbot widget visible (bottom-right corner)
- [ ] Status shows "✅ Connected"
- [ ] Can ask questions and get answers
- [ ] Sources show page numbers
- [ ] Can select text and use as context
- [ ] Widget minimizes/maximizes properly

---

## 🚀 Production Deployment

### Build for Production

```bash
# Build optimized site
npm run build

# Output: build/ folder with static files
```

### Deploy Options

**Option 1: Vercel**
```bash
# Push to GitHub first
git add .
git commit -m "Add RAG chatbot integration"
git push

# Deploy from vercel.com (auto-deploys)
```

**Option 2: Netlify**
```bash
# Build
npm run build

# Deploy build/ folder to netlify.com
```

**Option 3: Self-hosted**
```bash
# Serve build folder
npm run build
npx http-server build

# Or use nginx/Apache
```

---

## 📚 Documentation Links

- **Docusaurus**: https://docusaurus.io/
- **React**: https://react.dev/
- **Chatbot Backend**: `../rag-book-chat/README.md`

---

## 🎯 Next Steps

1. ✅ Start backend: `uvicorn app.main:app --port 8001`
2. ✅ Ingest book: `python scripts/ingest_book.py book.pdf --book-id my-book`
3. ✅ Start website: `npm start`
4. ✅ Test chatbot on http://localhost:3000
5. 🚀 Deploy when ready!

---

## 📞 Quick Reference

```bash
# Start backend (Terminal 1)
cd rag-book-chat
uvicorn app.main:app --port 8001

# Ingest book (Terminal 2)
python scripts/ingest_book.py book.pdf --book-id my-book

# Start website (Terminal 2, after ingestion)
cd ../my-book
npm install  # First time only
npm start    # Opens http://localhost:3000

# Build for production
npm run build

# Clear cache and rebuild
npm run clear && npm run build
```

---

**Congratulations! Your RAG Chatbot is now integrated into your documentation website! 🎉**

Now just need to:
1. ✅ Run backend
2. ✅ Ingest your book
3. ✅ Start the website
4. ✅ Test it out!
