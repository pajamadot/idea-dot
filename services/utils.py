import os
from dotenv import load_dotenv

def load_env_vars():
    """Load environment variables from .env.local in the project root"""
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get services directory
    project_root = os.path.dirname(script_dir)  # Go up one level to project root
    env_path = os.path.join(project_root, '.env.local')
    
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"Loaded environment variables from {env_path}")
    else:
        print(f"Warning: .env.local not found at {env_path}")
        print("Continuing without loading environment variables...") 