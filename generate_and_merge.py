import os
import argparse
import subprocess
import time
import asyncio
from prompt_generate import generate_prompts, save_prompts_to_files
from services.utils import load_env_vars

# Load environment variables
load_env_vars()

async def async_generate_music(music_prompt_file, duration, input_dir):
    """Generate music using the async API"""
    try:
        from music_generation import generate_music_async
        
        # Read prompt from file
        with open(music_prompt_file, 'r') as f:
            music_prompt = f.read().strip()
        
        print(f"\nGenerating music asynchronously...")
        music_file = await generate_music_async(music_prompt, duration=duration, output_folder=input_dir)
        
        if not music_file:
            print("Async music generation failed. You'll need to generate music manually.")
            print("Make sure you have the FAL_KEY environment variable set.")
            return None
        else:
            print(f"Async music generation successful: {music_file}")
            return music_file
    except ImportError as e:
        print(f"Error importing async music generation module: {e}")
        print("Make sure you have the fal_client package installed:")
        print("pip install fal-client requests")
        return None
    except Exception as e:
        print(f"Unexpected error in async music generation: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate prompts, create media, and merge them")
    parser.add_argument("--ffmpeg-path", help="Path to FFmpeg executable if not in PATH")
    parser.add_argument("--skip-prompt-generation", action="store_true", help="Skip prompt generation and use existing files")
    parser.add_argument("--generate-music", action="store_true", help="Automatically generate music using CassetteAI API")
    parser.add_argument("--music-duration", type=int, default=6, help="Duration of music in seconds (default: 6)")
    parser.add_argument("--async", dest="use_async", action="store_true", help="Use async API for music generation")
    args = parser.parse_args()
    
    # Create necessary directories
    input_dir = "input"
    output_dir = "output"
    prompts_dir = "prompts"
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(prompts_dir, exist_ok=True)
    
    video_prompt_file = os.path.join(prompts_dir, "video_prompt.txt")
    music_prompt_file = os.path.join(prompts_dir, "music_prompt.txt")
    
    # Step 1: Generate prompts
    if not args.skip_prompt_generation:
        print("Generating prompts...")
        video_prompt, music_prompt = generate_prompts()
        
        if video_prompt and music_prompt:
            save_prompts_to_files(
                video_prompt, 
                music_prompt, 
                video_prompt_file, 
                music_prompt_file
            )
        else:
            print("Failed to generate prompts. Exiting.")
            return
    else:
        print("Skipping prompt generation. Using existing files.")
        # Read existing prompt files
        try:
            with open(video_prompt_file, 'r') as f:
                video_prompt = f.read().strip()
            with open(music_prompt_file, 'r') as f:
                music_prompt = f.read().strip()
            print(f"Loaded existing video prompt: {video_prompt}")
            print(f"Loaded existing music prompt: {music_prompt}")
        except FileNotFoundError:
            print("Warning: Could not find existing prompt files. Please run without --skip-prompt-generation first.")
            return
    
    # Step 2a: Generate music if requested
    music_file = None
    if args.generate_music:
        if args.use_async:
            # Use async version
            music_file = asyncio.run(async_generate_music(
                music_prompt_file, 
                args.music_duration,
                input_dir
            ))
        else:
            try:
                print("\nGenerating music using CassetteAI API...")
                # Import here to avoid dependency if not using this feature
                from music_generation import generate_music_from_prompt_file
                
                music_file = generate_music_from_prompt_file(
                    music_prompt_file, 
                    duration=args.music_duration,
                    output_folder=input_dir
                )
                
                if not music_file:
                    print("Music generation failed. You'll need to generate music manually.")
                    print("Make sure you have the FAL_KEY environment variable set.")
                else:
                    print(f"Music generation successful: {music_file}")
            except ImportError:
                print("Error: Could not import music_generation module.")
                print("Make sure you have the fal_client package installed:")
                print("pip install fal-client requests")
    
    # Step 2b: Instructions for manual media generation
    print("\n--- Media Generation Steps ---")
    if not args.generate_music:
        print("1. Use the video_prompt with your video generation tool to create an MP4 file")
        print("2. Use the music_prompt with your audio generation tool to create a WAV file")
    else:
        print("1. Use the video_prompt with your video generation tool to create an MP4 file")
        if music_file:
            print(f"2. Music already generated: {os.path.basename(music_file)}")
        else:
            print("2. Music generation failed. Use the music_prompt with your audio generation tool to create a WAV file")
    
    print("3. Place the generated files in the 'input' directory")
    print(f"4. Make sure your MP4 file is named with a '.mp4' extension")
    if not args.generate_music or not music_file:
        print(f"5. Make sure your WAV file is named with a '.wav' extension")
    
    # Optional - wait for user to generate and place files
    user_input = input("\nPress Enter when you've placed the generated files in the input directory, or 'q' to quit: ")
    if user_input.lower() == 'q':
        return
    
    # Step 3: Run the merge_audio_video.py script
    merge_cmd = ["python", "merge_audio_video.py"]
    if args.ffmpeg_path:
        merge_cmd.extend(["--ffmpeg-path", args.ffmpeg_path])
    
    print("\nRunning merge_audio_video.py...")
    subprocess.run(merge_cmd)
    
    print("\nProcess complete!")
    print("Check the 'output' directory for your merged video.")

if __name__ == "__main__":
    main() 