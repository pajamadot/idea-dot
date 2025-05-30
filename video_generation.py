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

async def generate_image_async(
    prompt: str,
    output_folder: str = "input",
    output_filename: str = "game_image.jpg",
    num_images: int = 1,
    enable_safety_checker: bool = True,
    safety_tolerance: str = "2",
    output_format: str = "jpeg",
    aspect_ratio: str = "16:9"
) -> Optional[str]:
    """
    Generate image using FLUX-Pro Ultra API and download it to the specified folder.
    """
    print(f"Generating image with prompt: {prompt}")
    print(f"Aspect ratio: {aspect_ratio}")
    os.makedirs(output_folder, exist_ok=True)
    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        print("Error: FAL_KEY environment variable not set")
        return None

    try:
        result = await fal_client.run_async(
            "fal-ai/flux-pro/v1.1-ultra",
            arguments={
                "prompt": prompt,
                "num_images": num_images,
                "enable_safety_checker": enable_safety_checker,
                "safety_tolerance": safety_tolerance,
                "output_format": output_format,
                "aspect_ratio": aspect_ratio
            }
        )
        
        if not result or "images" not in result or len(result["images"]) == 0:
            print("Error: Failed to generate image or invalid response")
            return None

        image_url = result["images"][0]["url"]
        print(f"Image generated successfully. URL: {image_url}")
        
        response = requests.get(image_url)
        if response.status_code != 200:
            print(f"Error downloading image file: HTTP {response.status_code}")
            return None

        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Image saved to: {output_path}")
        return {
            "file_path": output_path,
            "url": image_url
        }
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

async def generate_video_async(
    image_url: str,
    prompt: str = "",
    output_folder: str = "input",
    output_filename: str = "game_video.mp4",
    negative_prompt: str = "blur, distort, and low quality",
    duration: str = "10",  # "5" or "10"
    aspect_ratio: str = "16:9",  # "16:9", "9:16", or "1:1"
    cfg_scale: float = 0.5,  # Classifier Free Guidance scale
    num_frames: int = 81,  # Keep for backward compatibility (not used with Kling)
    frames_per_second: int = 16,  # Keep for backward compatibility (not used with Kling)
    resolution: str = "720p",  # Keep for backward compatibility (not used with Kling)
    num_inference_steps: int = 30,  # Keep for backward compatibility (not used with Kling)
    guide_scale: int = 5,  # Keep for backward compatibility (not used with Kling)
    shift: int = 5,  # Keep for backward compatibility (not used with Kling)
    enable_safety_checker: bool = True,  # Keep for backward compatibility (not used with Kling)
    enable_prompt_expansion: bool = False,  # Keep for backward compatibility (not used with Kling)
    acceleration: str = "regular",  # Keep for backward compatibility (not used with Kling)
) -> Optional[str]:
    """
    Generate video from an image using Kling 2.1 Master Image-to-Video API and download it to the specified folder.
    """
    print(f"Generating video from image: {image_url}")
    print(f"Video prompt: {prompt}")
    os.makedirs(output_folder, exist_ok=True)
    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        print("Error: FAL_KEY environment variable not set")
        return None

    try:
        result = await fal_client.run_async(
            "fal-ai/kling-video/v2.1/master/image-to-video",
            arguments={
                "prompt": prompt,
                "image_url": image_url,
                "duration": duration,
                "aspect_ratio": aspect_ratio,
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
        print(f"Error generating video: {e}")
        return None

async def generate_game_video_async(
    prompt: str,
    output_folder: str = "input",
    image_filename: str = "game_image.jpg",
    video_filename: str = "game_video.mp4"
) -> Optional[str]:
    """
    Two-stage process: 
    1. Generate an image from a prompt
    2. Generate a video from that image
    """
    print(f"\n=== Stage 1: Generating Image from Prompt ===")
    image_result = await generate_image_async(
        prompt=prompt,
        output_folder=output_folder,
        output_filename=image_filename
    )
    
    if not image_result:
        print("Image generation failed. Cannot proceed to video generation.")
        return None
    
    print(f"\n=== Stage 2: Generating Video from Image ===")
    video_path = await generate_video_async(
        image_url=image_result["url"],
        prompt=prompt,
        output_folder=output_folder,
        output_filename=video_filename
    )
    
    if not video_path:
        print("Video generation failed.")
        return None
    
    return video_path

def generate_video_from_prompt_file(
    prompt_file: str,
    duration: str = "5",
    negative_prompt: str = "blur, distort, and low quality",
    cfg_scale: float = 0.5,
    output_folder: str = "input",
    output_filename: str = "game_video.mp4",
    aspect_ratio: str = "16:9"
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
        return asyncio.run(generate_game_video_async(
            prompt=prompt,
            output_folder=output_folder,
            video_filename=output_filename
        ))
    except FileNotFoundError:
        print(f"Error: Prompt file not found: {prompt_file}")
        return None
    except Exception as e:
        print(f"Error reading prompt file: {e}")
        return None

async def async_main():
    os.makedirs("input", exist_ok=True)
    test_prompt = """
    A cinematic sequence in a breathtaking cyberpunk metropolis at twilight. The camera begins with a slow, dramatic tilt up from street level, revealing towering skyscrapers with holographic advertisements that cast vibrant neon reflections on rain-slicked streets. Flying vehicles weave between buildings, their anti-gravity engines leaving trails of blue light. 

    The scene transitions to a close-up of a massive digital billboard displaying a mysterious countdown, its red numbers reflected in the eyes of passersby. The camera then smoothly tracks a sleek, autonomous delivery drone as it navigates through a maze of floating platforms and suspended walkways. 

    As the sequence continues, we see a group of augmented humans with glowing cybernetic implants, their movements fluid and synchronized as they interact with floating holographic interfaces. The camera pulls back to reveal the entire cityscape, now illuminated by a spectacular aurora borealis that dances across the sky, its colors shifting between electric blue and deep purple. 

    The final shot shows a massive space elevator in the distance, its base surrounded by swirling clouds of steam and energy, while the top disappears into the aurora-lit clouds. The entire sequence is rendered in photorealistic detail with dynamic lighting, atmospheric effects, and smooth camera movements. 4K resolution, cinematic color grading, and professional cinematography.
    """
    print("\n=== Testing Two-Stage Video Generation ===")
    output_file = await generate_game_video_async(test_prompt)
    
    prompt_file = "prompts/video_prompt.txt"
    if os.path.exists(prompt_file):
        print("\n=== Testing Two-Stage Video Generation with Prompt File ===")
        with open(prompt_file, 'r') as f:
            file_prompt = f.read().strip()
        if file_prompt:
            output_file = await generate_game_video_async(file_prompt)
        else:
            print(f"Error: Empty prompt in file {prompt_file}")
    else:
        print(f"\nSkipping prompt file test - file {prompt_file} does not exist")
        print("You can create this file by running generate_and_merge.py first")
    
    if output_file:
        print("\nSuccess! Two-stage video generation complete.")
        print(f"Generated file: {output_file}")
        print("You can now use merge_audio_video.py to combine this with audio")
    else:
        print("\nTwo-stage video generation failed. Please check the errors above.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate video using two-stage Image-to-Video generation")
    parser.add_argument("--prompt", type=str, help="Prompt to use for image and video generation")
    parser.add_argument("--prompt-file", type=str, help="Path to file containing the prompt")
    parser.add_argument("--output-folder", type=str, default="input", help="Folder to save generated files (default: input)")
    parser.add_argument("--output-filename", type=str, default="game_video.mp4", help="Output video filename (default: game_video.mp4)")
    
    args = parser.parse_args()
    os.makedirs(args.output_folder, exist_ok=True)
    
    if args.prompt_file:
        print(f"\n=== Using Prompt from File: {args.prompt_file} ===")
        output_file = generate_video_from_prompt_file(
            args.prompt_file,
            output_folder=args.output_folder,
            output_filename=args.output_filename
        )
    elif args.prompt:
        print(f"\n=== Using Provided Prompt ===")
        output_file = asyncio.run(generate_game_video_async(
            prompt=args.prompt,
            output_folder=args.output_folder,
            video_filename=args.output_filename
        ))
    else:
        asyncio.run(async_main())
    # Success/failure messages are handled in the called functions 