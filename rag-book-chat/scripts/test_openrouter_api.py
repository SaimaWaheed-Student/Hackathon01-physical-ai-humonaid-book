"""Test script to validate OpenRouter API connectivity."""

import sys
from pathlib import Path
import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import Config


def test_embedding():
    """Test embedding via OpenRouter."""
    try:
        print("🔍 Testing OpenRouter embedding API...")

        url = "https://openrouter.ai/api/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": Config.EMBEDDING_MODEL,
            "input": "What is Retrieval-Augmented Generation?"
        }

        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()

        embedding = response.json()["data"][0]["embedding"]
        print(f"✅ Embedding generated!")
        print(f"   Model: {Config.EMBEDDING_MODEL}")
        print(f"   Dimension: {len(embedding)}")

        return True

    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error: Cannot reach OpenRouter API")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: OpenRouter API took too long to respond")
        return False
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(f"❌ Authentication failed: Invalid OPENROUTER_API_KEY")
        elif e.response.status_code == 429:
            print(f"❌ Rate limited: Too many requests to OpenRouter")
        else:
            print(f"❌ HTTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Embedding failed: {e}")
        return False


def test_llm():
    """Test LLM inference via OpenRouter."""
    try:
        print("\n🔍 Testing OpenRouter LLM API...")

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": Config.CHAT_MODEL,
            "messages": [{"role": "user", "content": "Say 'RAG chatbot ready!' in one sentence."}],
            "temperature": 0.7,
            "max_tokens": 50
        }

        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()

        message = response.json()["choices"][0]["message"]["content"]
        print(f"✅ LLM response generated!")
        print(f"   Model: {Config.CHAT_MODEL}")
        print(f"   Response: {message[:100]}...")

        return True

    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error: Cannot reach OpenRouter API")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: OpenRouter API took too long to respond")
        return False
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(f"❌ Authentication failed: Invalid OPENROUTER_API_KEY")
        elif e.response.status_code == 429:
            print(f"❌ Rate limited: Too many requests to OpenRouter")
        else:
            print(f"❌ HTTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ LLM call failed: {e}")
        return False


if __name__ == "__main__":
    print("Testing OpenRouter API connectivity...\n")
    emb_ok = test_embedding()
    llm_ok = test_llm()

    if emb_ok and llm_ok:
        print("\n✅ All OpenRouter tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check configuration.")
        sys.exit(1)
