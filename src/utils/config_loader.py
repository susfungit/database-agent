import yaml
import os
from typing import Dict, Any

class ConfigLoader:
    """Configuration loader for the database agent."""
    
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            
            # Override with environment variables
            config = ConfigLoader._override_with_env(config)
            
            return config
        except Exception as e:
            raise Exception(f"Failed to load config from {config_path}: {e}")
    
    @staticmethod
    def _override_with_env(config: Dict[str, Any]) -> Dict[str, Any]:
        """Override config values with environment variables."""
        # LLM configuration
        if "OPENAI_API_KEY" in os.environ:
            config.setdefault("llm", {})
            config["llm"]["api_key"] = os.environ["OPENAI_API_KEY"]
        
        if "LLM_PROVIDER" in os.environ:
            config.setdefault("llm", {})
            config["llm"]["provider"] = os.environ["LLM_PROVIDER"]
        
        if "LLM_MODEL" in os.environ:
            config.setdefault("llm", {})
            config["llm"]["model"] = os.environ["LLM_MODEL"]
        
        # Server configuration
        if "SERVER_HOST" in os.environ:
            config.setdefault("server", {})
            config["server"]["host"] = os.environ["SERVER_HOST"]
        
        if "SERVER_PORT" in os.environ:
            config.setdefault("server", {})
            config["server"]["port"] = int(os.environ["SERVER_PORT"])
        
        # Logging configuration
        if "LOG_LEVEL" in os.environ:
            config.setdefault("logging", {})
            config["logging"]["level"] = os.environ["LOG_LEVEL"]
        
        return config 