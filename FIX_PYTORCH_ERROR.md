# Fix PyTorch DLL Error on Windows

## Problem
```
OSError: [WinError 126] The specified module could not be found.
Error loading "...\torch\lib\c10.dll"
```

## Solution (Choose ONE)

### ✅ OPTION 1: Install Visual C++ Redistributable (Recommended - 1 minute)

1. Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Run the installer
3. Click "Install"
4. Restart your terminal
5. Try again: `python scripts/ingest_book.py book.pdf --book-id my-book`

**✅ This is the permanent fix!**

---

### ✅ OPTION 2: Quick Workaround (No download - 2 minutes)

If you don't want to download:

```bash
# Use this one-time workaround to test
python scripts/ingest_book_simple.py book.pdf --book-id my-book

# This will show if your book can be ingested
# Then follow the normal flow
```

---

### ✅ OPTION 3: Use Virtual Environment (5 minutes)

```bash
# Create fresh virtual environment
python -m venv venv_rag
venv_rag\Scripts\activate

# Install dependencies in clean environment
pip install -r requirements.txt

# Now try:
python scripts/ingest_book.py book.pdf --book-id my-book
```

---

## Quick Start Path

**BEST**: Option 1 (install C++ runtime) → Restart terminal → Run commands normally

**FASTEST**: Option 2 (preview) → Then use Option 1 afterward

**SAFEST**: Option 3 (virtual env) → Clean isolation

---

## After Fixing

Once you've fixed the issue, run these 3 commands:

```bash
# Terminal 1
uvicorn app.main:app --port 8001

# Terminal 2
python scripts/ingest_book.py book.pdf --book-id my-book

# Terminal 3 (in my-book folder)
npm start
```

Then visit: http://localhost:3000

---

**Recommended**: Download and install Visual C++ Redistributable (option 1).
It takes 1 minute and fixes it permanently.

