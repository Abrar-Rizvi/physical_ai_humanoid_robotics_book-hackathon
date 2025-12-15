"""
Quickstart validation script for RAG Agent Backend
"""
import asyncio
import os
from src.config import settings
from src.clients.openai_client import openai_client
from src.clients.qdrant_client import qdrant_client, verify_collection_exists
from src.health import get_health_status


async def validate_setup():
    """
    Validate that all components are properly configured
    """
    print("🔍 Validating RAG Agent Backend setup...")

    # Check if required environment variables are set
    print("\n✅ Checking environment variables...")
    if not settings.openai_api_key:
        print("❌ OPENAI_API_KEY is not set")
        return False
    else:
        print("✅ OPENAI_API_KEY is set")

    if not settings.qdrant_url:
        print("❌ QDRANT_URL is not set")
        return False
    else:
        print("✅ QDRANT_URL is set")

    # Test OpenAI connection
    print("\n🌐 Testing OpenAI connection...")
    try:
        response = openai_client.models.list()
        if response.data:
            print("✅ OpenAI connection successful")
        else:
            print("❌ OpenAI connection failed - no models returned")
            return False
    except Exception as e:
        print(f"❌ OpenAI connection failed: {str(e)}")
        return False

    # Test Qdrant connection
    print("\n🌐 Testing Qdrant connection...")
    try:
        # Verify the collection exists
        collection_exists = verify_collection_exists(qdrant_client, settings.qdrant_collection_name)
        if collection_exists:
            print(f"✅ Qdrant connection successful, collection '{settings.qdrant_collection_name}' exists")
        else:
            print(f"⚠️ Qdrant connection successful, but collection '{settings.qdrant_collection_name}' does not exist")
            # This might be OK depending on use case
    except Exception as e:
        print(f"❌ Qdrant connection failed: {str(e)}")
        return False

    # Test health check
    print("\n🏥 Testing health check...")
    try:
        health_status = await get_health_status()
        print(f"✅ Health check successful - Status: {health_status.status}")
        print(f"   Services: {health_status.services}")
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False

    print("\n🎉 All validations passed! RAG Agent Backend is ready.")
    return True


if __name__ == "__main__":
    success = asyncio.run(validate_setup())
    if success:
        print("\n🚀 You can now start the RAG Agent Backend with:")
        print("   cd backend")
        print("   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
        print("\n📋 Example API calls:")
        print("   Health check: curl http://localhost:8000/health")
        print('   Query: curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d \'{"query": "Your question here"}\'')
    else:
        print("\n❌ Setup validation failed. Please check the error messages above.")