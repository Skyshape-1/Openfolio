"""
API Key Test Script for Mili AI Assistant
==========================================
Usage:
1. Ensure ANTHROPIC_API_KEY is set in your environment or .env file
2. Run: python -m backend.tests.test_api
   (or from backend directory: python tests/test_api.py)
3. Check results - supports both custom endpoint and official Anthropic API
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import AsyncAnthropic

# Load environment variables
# assuming this file is in backend/tests/, we look for .env in backend/
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# ============================================================
# CONFIGURATION
# ============================================================
TEST_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CUSTOM_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.vectorengine.ai")

# ============================================================
# TEST CONFIGURATION
# ============================================================
TEST_MODEL = "claude-3-7-sonnet-20250219"
TEST_PROMPT = "Say hello in one word"


async def test_with_custom_endpoint(api_key: str, base_url: str):
    """Test API key with custom endpoint"""
    print(f"\n{'='*60}")
    print(f"TEST 1: Custom Endpoint")
    print(f"{'='*60}")
    print(f"Base URL: {base_url}")
    print(f"API Key: {api_key[:10]}...{api_key[-5:] if api_key else ''}")

    client = AsyncAnthropic(api_key=api_key, base_url=base_url)

    try:
        response = await client.messages.create(
            model=TEST_MODEL,
            max_tokens=50,
            messages=[{"role": "user", "content": TEST_PROMPT}]
        )
        print(f"\n SUCCESS!")
        print(f" Response: {response.content[0].text}")
        print(f" Model: {response.model}")
        return True
    except Exception as e:
        print(f"\n FAILED: {type(e).__name__}")
        print(f" Error: {str(e)[:200]}")
        return False


async def test_with_official_api(api_key: str):
    """Test API key with official Anthropic API"""
    print(f"\n{'='*60}")
    print(f"TEST 2: Official Anthropic API")
    print(f"{'='*60}")
    print(f"Base URL: https://api.anthropic.com (Official)")
    print(f"API Key: {api_key[:10]}...{api_key[-5:] if api_key else ''}")

    client = AsyncAnthropic(api_key=api_key)  # No base_url = official API

    try:
        response = await client.messages.create(
            model=TEST_MODEL,
            max_tokens=50,
            messages=[{"role": "user", "content": TEST_PROMPT}]
        )
        print(f"\n SUCCESS!")
        print(f" Response: {response.content[0].text}")
        print(f" Model: {response.model}")
        return True
    except Exception as e:
        print(f"\n FAILED: {type(e).__name__}")
        print(f" Error: {str(e)[:200]}")
        return False


async def test_rag_style_query(api_key: str, base_url: str):
    """Test with a RAG-style query (longer context)"""
    print(f"\n{'='*60}")
    print(f"TEST 3: RAG-Style Query (with system prompt)")
    print(f"{'='*60}")
    print(f"Base URL: {base_url}")

    client = AsyncAnthropic(api_key=api_key, base_url=base_url)

    try:
        response = await client.messages.create(
            model=TEST_MODEL,
            max_tokens=100,
            system="You are a helpful AI assistant. Answer questions based on the provided context.",
            messages=[{
                "role": "user",
                "content": "What is the capital of France?"
            }]
        )
        print(f"\n SUCCESS!")
        print(f" Response: {response.content[0].text[:100]}...")
        return True
    except Exception as e:
        print(f"\n FAILED: {type(e).__name__}")
        print(f" Error: {str(e)[:200]}")
        return False


async def main():
    print("\n" + "="*60)
    print(" Mili API Key Validator")
    print("="*60)

    if not TEST_API_KEY or TEST_API_KEY == "sk-YOUR_NEW_API_KEY_HERE":
        print("\n ERROR: Please set ANTHROPIC_API_KEY in your backend/.env file!")
        return

    print(f"\nAPI Key: {TEST_API_KEY[:10]}...{TEST_API_KEY[-5:]}")
    print(f"Model: {TEST_MODEL}")

    # Run all tests
    results = {}

    # Test 1: Custom endpoint
    results["custom"] = await test_with_custom_endpoint(TEST_API_KEY, CUSTOM_BASE_URL)

    # Test 2: Official API
    results["official"] = await test_with_official_api(TEST_API_KEY)

    # Test 3: RAG-style query (only if endpoint works)
    if results["custom"]:
        results["rag"] = await test_rag_style_query(TEST_API_KEY, CUSTOM_BASE_URL)
    else:
        results["rag"] = False

    # Final summary
    print(f"\n{'='*60}")
    print(" SUMMARY")
    print(f"{'='*60}")
    print(f"Custom Endpoint:      {' PASS' if results['custom'] else ' FAIL'}")
    print(f"Official API:          {' PASS' if results['official'] else ' FAIL'}")
    print(f"RAG-Style Query:       {' PASS' if results['rag'] else ' N/A'}")

    print(f"\n{'='*60}")
    if results["custom"]:
        print(" RESULT: API key is VALID for Mili!")
    elif results["official"]:
        print(" RESULT: API key works with OFFICIAL API only")
    else:
        print(" RESULT: API key is INVALID or EXPIRED")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
