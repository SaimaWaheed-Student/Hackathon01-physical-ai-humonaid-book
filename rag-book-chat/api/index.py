"""Vercel serverless function entry point for RAG Chatbot API."""

from app.main import app

# Export the FastAPI app for Vercel
handler = app
