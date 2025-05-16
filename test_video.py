import os
import asyncio
from video_generation import generate_video_async
from services.utils import load_env_vars

# Load environment variables
load_env_vars()

async def test_video_generation():
    """
    Test the video generation functionality with a sample prompt.
    """
    print("\n=== Testing Video Generation ===")
    
    # Test prompt
    test_prompt = """A cinematic shot of a futuristic cityscape at sunset, with flying cars and neon lights 
    reflecting off glass buildings. The camera slowly pans upward to reveal a massive space station in orbit. 
    The scene is bathed in warm orange and purple hues, with dramatic shadows and atmospheric fog."""
    
    print(f"Using test prompt: {test_prompt}")
    print("Duration: 5 seconds")
    print("Aspect ratio: 16:9")
    
    # Generate video
    output_file = await generate_video_async(
        prompt=test_prompt,
        duration="5",
        negative_prompt="blur, distort, and low quality",
        cfg_scale=0.5,
        output_folder="input"
    )
    
    if output_file:
        print("\nSuccess! Video generation complete.")
        print(f"Generated video saved to: {output_file}")
    else:
        print("\nVideo generation failed. Please check the errors above.")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_video_generation()) 