"""RAG (Retrieval-Augmented Generation) pipeline for chatbot."""

import logging
from typing import List, Tuple
import requests

from qdrant_client import QdrantClient
from app.config import Config

logger = logging.getLogger(__name__)


def retrieve_similar_chunks(
    question: str,
    book_id: str = "default",
    top_k: int = 5,
    threshold: float = 0.6
) -> List[dict]:
    """Retrieve chunks similar to the question via semantic search.

    Args:
        question: User question
        book_id: ID of book to search
        top_k: Number of top chunks to retrieve
        threshold: Minimum similarity score

    Returns:
        List of relevant chunks with metadata
    """
    try:
        logger.info(f"Retrieving chunks for question: {question[:50]}...")

        # Step 1: Embed the question
        logger.debug("Embedding question...")
        url = "https://openrouter.ai/api/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": Config.EMBEDDING_MODEL,
            "input": question
        }

        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        question_embedding = response.json()["data"][0]["embedding"]
        logger.debug(f"Question embedding generated: {len(question_embedding)} dims")

        # Step 2: Search Qdrant
        logger.debug(f"Searching Qdrant for book_id={book_id}...")
        client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
            timeout=10
        )

        from qdrant_client.models import Filter, FieldCondition, MatchValue

        search_results = client.query_points(
            collection_name=Config.COLLECTION_NAME,
            query=question_embedding,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="book_id",
                        match=MatchValue(value=book_id)
                    )
                ]
            ),
            limit=top_k,
            score_threshold=threshold
        ).points

        logger.info(f"Found {len(search_results)} relevant chunks")

        # Step 3: Format results
        results = []
        for result in search_results:
            if result.score >= threshold:
                results.append({
                    "chunk_text": result.payload["chunk_text"],
                    "page_num": result.payload["page_num"],
                    "chunk_id": result.payload["chunk_id"],
                    "section_title": result.payload.get("section_title"),
                    "similarity_score": result.score
                })

        return results

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to embed question: {e}")
        return []
    except Exception as e:
        logger.error(f"Failed to search Qdrant: {e}", exc_info=True)
        return []


def synthesize_answer(
    question: str,
    context_chunks: List[dict],
    selected_text: str = None,
    include_fallback: bool = True
) -> Tuple[str, bool]:
    """Synthesize answer using LLM and context chunks.

    Supports selection-based queries where selected text is treated
    as primary context, with optional supplementary full-book search.

    Args:
        question: User question
        context_chunks: List of relevant chunks from retrieval
        selected_text: Optional user-selected text as primary context
        include_fallback: Whether to use general knowledge fallback

    Returns:
        Tuple of (answer_text, is_fallback_flag)
    """
    try:
        logger.info(f"Synthesizing answer from {len(context_chunks)} chunks (selected_text={bool(selected_text)})")

        if selected_text or context_chunks:
            # Use selected text as primary context if available
            if selected_text:
                primary_context = f"[USER SELECTED TEXT]\n{selected_text}"
                if context_chunks:
                    supplementary = "\n\n".join([
                        f"[Page {c['page_num']}] {c['chunk_text']}"
                        for c in context_chunks[:3]  # Limit to 3 supplementary chunks
                    ])
                    context_text = f"{primary_context}\n\n[SUPPLEMENTARY BOOK SECTIONS]\n{supplementary}"
                else:
                    context_text = primary_context
            else:
                # No selected text, use retrieved chunks
                context_text = "\n\n".join([
                    f"[Page {c['page_num']}] {c['chunk_text']}"
                    for c in context_chunks
                ])

            prompt = f"""You are a helpful assistant answering questions about a book.
Use the provided context to answer the question.
If the context doesn't contain enough information, say: "I didn't find sufficient information in the book about this."
Always cite your sources by mentioning page numbers or that you're referencing the selected text.

Context:
{context_text}

Question: {question}

Answer:"""
            is_fallback = False

        else:
            # No context, use general knowledge if allowed
            if not include_fallback:
                return "I couldn't find information about this in the book.", False

            prompt = f"""Answer this question based on general knowledge.
Always indicate that this answer is NOT from the book.

Question: {question}

Answer: Based on general knowledge (not from the book):"""
            is_fallback = True

        # Call OpenRouter LLM
        logger.debug(f"Calling OpenRouter LLM: {Config.CHAT_MODEL}")
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": Config.CHAT_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }

        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()

        answer = response.json()["choices"][0]["message"]["content"]
        logger.info(f"Answer synthesized (fallback={is_fallback}, len={len(answer)}, selected_text={bool(selected_text)})")

        return answer, is_fallback

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to call OpenRouter LLM: {e}")
        error_answer = f"Error generating answer: {str(e)}"
        return error_answer, False
    except Exception as e:
        logger.error(f"Failed to synthesize answer: {e}", exc_info=True)
        error_answer = f"Error generating answer: {str(e)}"
        return error_answer, False
