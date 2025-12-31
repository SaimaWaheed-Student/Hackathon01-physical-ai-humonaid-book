"""Test script to validate Qdrant Cloud connectivity."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client import QdrantClient
from app.config import Config


def test_qdrant():
    """Test Qdrant Cloud connection."""
    try:
        print("🔍 Testing Qdrant Cloud connection...")
        print(f"   URL: {Config.QDRANT_URL}")

        client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
            timeout=5.0
        )

        # Test connection
        info = client.get_collection_names()
        print(f"✅ Qdrant connected!")
        print(f"   Collections: {len(info.collections)} existing collections")
        if info.collections:
            for coll in info.collections[:5]:  # Show first 5
                print(f"      - {coll.name}")

        # Try to create a test collection
        print(f"\n🔍 Testing collection creation...")
        test_collection_name = f"{Config.COLLECTION_NAME}_test"
        try:
            client.recreate_collection(
                collection_name=test_collection_name,
                vectors_config={
                    "size": 1536,
                    "distance": "Cosine"
                }
            )
            print(f"✅ Created test collection: {test_collection_name}")

            # Clean up
            client.delete_collection(test_collection_name)
            print(f"✅ Deleted test collection")

        except Exception as e:
            print(f"⚠️  Test collection skipped: {e}")

        return True

    except Exception as e:
        print(f"❌ Qdrant connection failed: {e}")
        print(f"   Please check:")
        print(f"   1. QDRANT_URL in .env is correct")
        print(f"   2. QDRANT_API_KEY in .env is valid")
        print(f"   3. Internet connection is available")
        return False


if __name__ == "__main__":
    success = test_qdrant()
    sys.exit(0 if success else 1)
