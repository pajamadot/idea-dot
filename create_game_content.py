import os
import asyncio
import json
from openai import OpenAI
from services.utils import load_env_vars
from music_generation import generate_music_async
from video_generation import generate_video_async
from merge_audio_video import merge_audio_video
from services.tweet import tweet

# Load environment variables
load_env_vars()

# Constants for consistent filenames
MUSIC_FILENAME = "game_music.wav"
VIDEO_FILENAME = "game_video.mp4"
FINAL_FILENAME = "final_game_content.mp4"

async def generate_twitter_content(video_prompt: str, music_prompt: str) -> str:
    """
    Generate engaging Twitter content using GPT-4.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""
    Create a viral-worthy tweet about this innovative game concept:
    Video: {video_prompt}
    Music: {music_prompt}
    
    Requirements:
    1. Keep it under 280 characters
    2. Start with a strong visual hook that captures attention
    3. Create emotional engagement through tension, action, or curiosity
    4. Include a clear call-to-action (e.g., "Would you play this?", "Drop a ❤️ if you want to try this")
    5. Add 2-5 relevant emojis to enhance readability and engagement
    6. Include 4-6 hashtags:
       - Always include #AIGeneratedGameplay
       - 1-2 broad gaming tags (e.g., #gamedev, #indiegame)
       - 1-2 niche/mood tags based on the game's style (e.g., #pixelart, #scifi, #synthwave)
    7. Format:
       <Tweet body>
       <Line break>
       #hashtags

    Game Concept Guidelines:
    - Think beyond traditional genres (e.g., not just platformers, RPGs, or shooters)
    - Consider experimental mechanics like:
      * Games that blend physical and digital worlds
      * Social experiments disguised as games
      * Games that evolve based on player emotions
      * Games that use real-world data or events
      * Games that challenge traditional gameplay conventions
    - Explore unique themes like:
      * Philosophical concepts
      * Abstract emotions
      * Social commentary
      * Environmental awareness
      * Cultural experiences
    - Consider innovative gameplay elements:
      * Games that require multiple devices
      * Games that use AI to adapt to players
      * Games that incorporate real-time world events
      * Games that blend different art forms
      * Games that challenge player perceptions
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a viral game content strategist and copywriter for an AI-driven game studio. Your expertise lies in creating innovative, boundary-pushing game concepts that challenge traditional gaming norms. You excel at presenting experimental and avant-garde game ideas in an engaging way that makes viewers stop scrolling. You're known for your ability to make unconventional game concepts feel accessible and exciting."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,  # Increased temperature for more creative variations
    )
    
    return response.choices[0].message.content.strip()

async def create_game_content():
    """
    Main function to orchestrate the entire content creation workflow.
    """
    print("\n=== Starting Game Content Creation ===")
    
    # Create necessary directories
    input_dir = "input"
    output_dir = "output"
    prompts_dir = "prompts"
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(prompts_dir, exist_ok=True)  # Create prompts directory
    
    # Define file paths
    music_path = os.path.join(input_dir, MUSIC_FILENAME)
    video_path = os.path.join(input_dir, VIDEO_FILENAME)
    final_path = os.path.join(output_dir, FINAL_FILENAME)
    
    # Step 1: Generate prompts
    print("\n1. Generating prompts...")
    from prompt_generate import generate_prompts, save_prompts_to_files
    
    video_prompt, music_prompt = generate_prompts()
    if not video_prompt or not music_prompt:
        print("Failed to generate prompts. Exiting.")
        return
    
    # Save prompts to files
    save_prompts_to_files(
        video_prompt,
        music_prompt,
        os.path.join(prompts_dir, "video_prompt.txt"),  # Use os.path.join for proper path handling
        os.path.join(prompts_dir, "music_prompt.txt")   # Use os.path.join for proper path handling
    )
    
    # Step 2: Generate media content
    print("\n2. Generating media content...")
    
    # Generate music
    print("\nGenerating music...")
    music_file = await generate_music_async(
        prompt=music_prompt,
        duration=10,  # Minimum duration for music
        output_folder=input_dir,
        output_filename=MUSIC_FILENAME  # Use consistent filename
    )
    
    if not music_file:
        print("Music generation failed. Exiting.")
        return
    
    # Generate video
    print("\nGenerating video...")
    video_file = await generate_video_async(
        prompt=video_prompt,
        duration="5",  # Video duration
        output_folder=input_dir,
        output_filename=VIDEO_FILENAME  # Use consistent filename
    )
    
    if not video_file:
        print("Video generation failed. Exiting.")
        return
    
    # Step 3: Merge audio and video
    print("\n3. Merging audio and video...")
    success = merge_audio_video(video_file, music_file, final_path)
    if not success:
        print("Failed to merge audio and video. Exiting.")
        return
    
    # Step 4: Generate Twitter content
    print("\n4. Generating Twitter content...")
    twitter_content = await generate_twitter_content(video_prompt, music_prompt)
    
    # Step 5: Print results
    print("\n=== Content Creation Complete ===")
    print("\nTwitter Content:")
    print(twitter_content)
    print(f"\nFinal Video: {final_path}")
    
    # Optional: Post to Twitter
    post_to_twitter = input("\nWould you like to post this to Twitter? (y/n): ").lower()
    if post_to_twitter == 'y':
        try:
            tweet_id = tweet(twitter_content, final_path)
            if tweet_id:
                print(f"Successfully posted to Twitter! Tweet ID: {tweet_id}")
            else:
                print("Failed to post to Twitter.")
        except Exception as e:
            print(f"Error posting to Twitter: {e}")

if __name__ == "__main__":
    asyncio.run(create_game_content()) 