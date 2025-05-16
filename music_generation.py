import os
import asyncio
import fal_client
import requests
from typing import Dict, Any, Optional, Union
import time
from pathlib import Path
from services.utils import load_env_vars

# Load environment variables
load_env_vars()

async def generate_music_async(
    prompt: str, 
    duration: int = 10, 
    output_folder: str = "input",
    output_filename: str = "game_music.wav"
) -> Optional[str]:
    """
    Generate music using CassetteAI's music generator API and download it to the specified folder.
    Asynchronous version using run_async.
    """
    if duration < 10:
        print("Duration must be at least 10 seconds. Setting duration to 10.")
        duration = 10
    print(f"Generating music asynchronously with prompt: {prompt}")
    print(f"Requested duration: {duration} seconds")
    os.makedirs(output_folder, exist_ok=True)
    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        print("Error: FAL_KEY environment variable not set")
        return None
    try:
        result = await fal_client.run_async(
            "CassetteAI/music-generator",
            arguments={
                "prompt": prompt,
                "duration": duration
            }
        )
        if not result or "audio_file" not in result or "url" not in result["audio_file"]:
            print("Error: Failed to generate music or invalid response")
            return None
        audio_url = result["audio_file"]["url"]
        print(f"Music generated successfully. URL: {audio_url}")
        response = requests.get(audio_url)
        if response.status_code != 200:
            print(f"Error downloading audio file: HTTP {response.status_code}")
            return None
        
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Music saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error generating music asynchronously: {e}")
        return None

def generate_music_from_prompt_file(
    prompt_file: str, 
    duration: int = 10, 
    output_folder: str = "input",
    output_filename: str = "game_music.wav"
) -> Optional[str]:
    """
    Read a music prompt from a file and generate music using it (async).
    """
    try:
        with open(prompt_file, 'r') as f:
            prompt = f.read().strip()
        if not prompt:
            print(f"Error: Empty prompt in file {prompt_file}")
            return None
        # Run the async function in an event loop
        return asyncio.run(generate_music_async(
            prompt, 
            duration, 
            output_folder,
            output_filename
        ))
    except FileNotFoundError:
        print(f"Error: Prompt file not found: {prompt_file}")
        return None
    except Exception as e:
        print(f"Error reading prompt file: {e}")
        return None

async def async_main():
    os.makedirs("input", exist_ok=True)
    test_prompt = "Suspenseful electronic soundtrack with pulsing synthesizers at 110 BPM in D minor, featuring distant percussion hits, atmospheric pads creating tension, wide stereo field with cavernous reverb, and mastered with moderate compression for cinematic impact."
    print("\n=== Testing Async API with Direct Prompt ===")
    output_file = await generate_music_async(test_prompt)
    
    prompt_file = "prompts/music_prompt.txt"
    if os.path.exists(prompt_file):
        print("\n=== Testing Async API with Prompt File ===")
        with open(prompt_file, 'r') as f:
            file_prompt = f.read().strip()
        if file_prompt:
            output_file = await generate_music_async(file_prompt)
        else:
            print(f"Error: Empty prompt in file {prompt_file}")
    else:
        print(f"\nSkipping prompt file test - file {prompt_file} does not exist")
        print("You can create this file by running generate_and_merge.py first")
    if output_file:
        print("\nSuccess! Async music generation complete.")
        print(f"Generated file: {output_file}")
        print("You can now use merge_audio_video.py to combine this with a video")
    else:
        print("\nAsync music generation failed. Please check the errors above.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate music using CassetteAI API (async only)")
    parser.add_argument("--prompt", type=str, help="Music prompt to use (overrides default test prompt)")
    parser.add_argument("--prompt-file", type=str, help="Path to file containing the music prompt")
    parser.add_argument("--duration", type=int, default=10, help="Duration of music in seconds (minimum: 10)")
    parser.add_argument("--output-folder", type=str, default="input", help="Folder to save generated music (default: input)")
    parser.add_argument("--output-filename", type=str, default="game_music.wav", help="Output filename (default: game_music.wav)")
    args = parser.parse_args()
    os.makedirs(args.output_folder, exist_ok=True)
    if args.prompt_file:
        print(f"\n=== Using Prompt from File: {args.prompt_file} ===")
        output_file = generate_music_from_prompt_file(
            args.prompt_file, 
            args.duration, 
            args.output_folder,
            args.output_filename
        )
    elif args.prompt:
        print(f"\n=== Using Provided Prompt ===")
        output_file = asyncio.run(generate_music_async(
            args.prompt, 
            args.duration, 
            args.output_folder,
            args.output_filename
        ))
    else:
        asyncio.run(async_main())
    # Success/failure messages are handled in the called functions 