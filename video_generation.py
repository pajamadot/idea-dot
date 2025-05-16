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

async def generate_video_async(
    prompt: str,
    duration: str = "5",
    negative_prompt: str = "blur, distort, and low quality",
    cfg_scale: float = 0.5,
    output_folder: str = "input",
    output_filename: str = "game_video.mp4"
) -> Optional[str]:
    """
    Generate video using Kling 2.0 Master Text to Video API and download it to the specified folder.
    Asynchronous version using run_async.
    """
    print(f"Generating video asynchronously with prompt: {prompt}")
    print(f"Requested duration: {duration} seconds")
    print(f"Aspect ratio: 16:9")
    os.makedirs(output_folder, exist_ok=True)
    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        print("Error: FAL_KEY environment variable not set")
        return None

    try:
        result = await fal_client.run_async(
            "fal-ai/kling-video/v2/master/text-to-video",
            arguments={
                "prompt": prompt,
                "duration": duration,
                "aspect_ratio": "16:9",
                "negative_prompt": negative_prompt,
                "cfg_scale": cfg_scale
            }
        )
        
        if not result or "video" not in result or "url" not in result["video"]:
            print("Error: Failed to generate video or invalid response")
            return None

        video_url = result["video"]["url"]
        print(f"Video generated successfully. URL: {video_url}")
        
        response = requests.get(video_url)
        if response.status_code != 200:
            print(f"Error downloading video file: HTTP {response.status_code}")
            return None

        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Video saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error generating video asynchronously: {e}")
        return None

def generate_video_from_prompt_file(
    prompt_file: str,
    duration: str = "5",
    negative_prompt: str = "blur, distort, and low quality",
    cfg_scale: float = 0.5,
    output_folder: str = "input",
    output_filename: str = "game_video.mp4"
) -> Optional[str]:
    """
    Read a video prompt from a file and generate video using it (async).
    """
    try:
        with open(prompt_file, 'r') as f:
            prompt = f.read().strip()
        if not prompt:
            print(f"Error: Empty prompt in file {prompt_file}")
            return None
        # Run the async function in an event loop
        return asyncio.run(generate_video_async(
            prompt,
            duration,
            negative_prompt,
            cfg_scale,
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
    test_prompt = "A cinematic shot of a futuristic cityscape at sunset, with flying cars and neon lights reflecting off glass buildings. The camera slowly pans upward to reveal a massive space station in orbit."
    print("\n=== Testing Async API with Direct Prompt ===")
    output_file = await generate_video_async(test_prompt)
    
    prompt_file = "prompts/video_prompt.txt"
    if os.path.exists(prompt_file):
        print("\n=== Testing Async API with Prompt File ===")
        with open(prompt_file, 'r') as f:
            file_prompt = f.read().strip()
        if file_prompt:
            output_file = await generate_video_async(file_prompt)
        else:
            print(f"Error: Empty prompt in file {prompt_file}")
    else:
        print(f"\nSkipping prompt file test - file {prompt_file} does not exist")
        print("You can create this file by running generate_and_merge.py first")
    
    if output_file:
        print("\nSuccess! Async video generation complete.")
        print(f"Generated file: {output_file}")
        print("You can now use merge_audio_video.py to combine this with audio")
    else:
        print("\nAsync video generation failed. Please check the errors above.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate video using Kling 2.0 Master Text to Video API")
    parser.add_argument("--prompt", type=str, help="Video prompt to use (overrides default test prompt)")
    parser.add_argument("--prompt-file", type=str, help="Path to file containing the video prompt")
    parser.add_argument("--duration", type=str, default="5", choices=["5", "10"], help="Duration of video in seconds (default: 5)")
    parser.add_argument("--negative-prompt", type=str, default="blur, distort, and low quality", help="Negative prompt to avoid certain elements")
    parser.add_argument("--cfg-scale", type=float, default=0.5, help="CFG scale for prompt adherence (default: 0.5)")
    parser.add_argument("--output-folder", type=str, default="input", help="Folder to save generated video (default: input)")
    parser.add_argument("--output-filename", type=str, default="game_video.mp4", help="Output filename (default: game_video.mp4)")
    
    args = parser.parse_args()
    os.makedirs(args.output_folder, exist_ok=True)
    
    if args.prompt_file:
        print(f"\n=== Using Prompt from File: {args.prompt_file} ===")
        output_file = generate_video_from_prompt_file(
            args.prompt_file,
            args.duration,
            args.negative_prompt,
            args.cfg_scale,
            args.output_folder,
            args.output_filename
        )
    elif args.prompt:
        print(f"\n=== Using Provided Prompt ===")
        output_file = asyncio.run(generate_video_async(
            args.prompt,
            args.duration,
            args.negative_prompt,
            args.cfg_scale,
            args.output_folder,
            args.output_filename
        ))
    else:
        asyncio.run(async_main())
    # Success/failure messages are handled in the called functions 