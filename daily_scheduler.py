import schedule
import time
import subprocess
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

def run_game_content():
    """Run the create_game_content.py script"""
    try:
        logging.info("Starting game content generation...")
        
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Run the create_game_content.py script
        result = subprocess.run(
            ['python', os.path.join(script_dir, 'create_game_content.py')],
            capture_output=True,
            text=True
        )
        
        # Log the output
        if result.stdout:
            logging.info(f"Script output:\n{result.stdout}")
        if result.stderr:
            logging.error(f"Script errors:\n{result.stderr}")
            
        logging.info("Game content generation completed")
        
    except Exception as e:
        logging.error(f"Error running game content generation: {e}")

def main():
    # Schedule the job to run daily at 9:00 AM
    schedule.every().day.at("09:00").do(run_game_content)
    
    logging.info("Scheduler started. Will run daily at 9:00 AM")
    logging.info("Press Ctrl+C to exit")
    
    # Run the job immediately on startup
    run_game_content()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main() 