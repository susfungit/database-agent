#!/usr/bin/env python3
"""
Simple test script to verify the database agent setup works.
"""

import sys
import os

def test_imports():
    """Test if all imports work correctly."""
    print("Testing imports...")
    
    try:
        # Test llmwrapper import
        from llmwrapper import get_llm
        print("✅ llmwrapper import successful")
    except ImportError as e:
        print(f"❌ llmwrapper import failed: {e}")
        print("   Please run: pip install -e ../llmwrapper")
        return False
    
    try:
        # Test our modules
        from src.database_agent.agent import DatabaseAgent
        print("✅ DatabaseAgent import successful")
    except ImportError as e:
        print(f"❌ DatabaseAgent import failed: {e}")
        return False
    
    try:
        from src.utils.config_loader import ConfigLoader
        print("✅ ConfigLoader import successful")
    except ImportError as e:
        print(f"❌ ConfigLoader import failed: {e}")
        return False
    
    try:
        from src.utils.logger import setup_logger
        print("✅ Logger import successful")
    except ImportError as e:
        print(f"❌ Logger import failed: {e}")
        return False
    
    return True

def test_config_loading():
    """Test configuration loading."""
    print("\nTesting configuration loading...")
    
    try:
        from src.utils.config_loader import ConfigLoader
        config = ConfigLoader.load_config("config/llm_config.yaml")
        print("✅ Configuration loaded successfully")
        print(f"   LLM Provider: {config.get('llm', {}).get('provider', 'not set')}")
        return True
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

def test_agent_initialization():
    """Test agent initialization (without LLM)."""
    print("\nTesting agent initialization...")
    
    try:
        from src.database_agent.agent import DatabaseAgent
        from unittest.mock import Mock, patch
        
        # Mock the LLM to avoid actual API calls
        with patch('src.database_agent.llm_integration.get_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.chat.return_value = "SELECT * FROM users;"
            mock_get_llm.return_value = mock_llm
            
            config = {
                "llm": {
                    "provider": "openai",
                    "model": "gpt-4",
                    "api_key": "test-key"
                }
            }
            
            agent = DatabaseAgent(config)
            print("✅ Agent initialization successful")
            return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Database Agent Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config_loading,
        test_agent_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Set your API key in .env file")
        print("2. Run: python src/mcp_server.py")
        print("3. Test with: curl http://localhost:8000/health")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("Make sure you're in the database-agent directory and packages are installed:")
        print("  pip install -e ../llmwrapper")
        print("  pip install -e ../schema-graph-builder")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 