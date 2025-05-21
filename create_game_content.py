import os
import asyncio
import json
from openai import OpenAI
from services.utils import load_env_vars
from music_generation import generate_music_async
from video_generation import generate_game_video_async
from merge_audio_video import merge_audio_video
from services.tweet import tweet

# Load environment variables
load_env_vars()

# Constants for consistent filenames
MUSIC_FILENAME = "game_music.wav"
IMAGE_FILENAME = "game_image.jpg"
VIDEO_FILENAME = "game_video.mp4"
FINAL_FILENAME = "final_game_content.mp4"

async def generate_twitter_content(video_prompt: str, music_prompt: str) -> str:
    """
    Generate explicit, adult-themed Twitter content for the video.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create more explicit prompt for Twitter
    prompt = f"""
    Create an explicit, adult-themed tweet about this erotic anime scene:
    Video: {video_prompt}
    Music: {music_prompt}
    
    Requirements:
    1. Keep it under 280 characters for the main tweet body
    2. Create an explicit, sexually suggestive description (3-5 lines)
    3. Focus on the erotic and sexual aspects of the scene
    4. Use explicit language that is highly arousing
    5. Add 3-5 suggestive emojis (like 🔥💦😈❤️‍🔥👅)
    6. Include the following REQUIRED hashtags, plus additional adult-themed ones:
       <Explicit description>
       <Line break>
       #NSFW #Hentai #AnimeGirl #EroticArt #AdultContent #18Plus #Lewd #Ecchi #XXX #AIart #AI美女 #AI美少女 #AIGC
       <Plus 3-6 additional adult-themed tags>
       
    Additional hashtag categories you can choose from:
       - EXPLICIT: #HentaiArt #AdultAnime #EroticAnime #SexyAnime
       - NICHE: #AnimeBoobs #AnimeAss #AnimeThighs #AnimeLewd
       - PLATFORM: #OnlyFans #AdultContent #NSFWTwitter #NSFWArt
       - AUDIENCE: #HentaiLovers #AnimeNSFW #LewdAnime #HentaiFans

    Format:
       <Explicit description - 3-5 lines>
       <Line break>
       #NSFW #Hentai #AnimeGirl #EroticArt #AdultContent #18Plus #Lewd #Ecchi #XXX #AIart #AI美女 #AI美少女 #AIGC <plus additional adult hashtags>

    Do NOT include any disclaimers, warnings, or age restrictions in the actual text. Make the content as explicit and arousing as possible.
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a specialized adult content creator focused on generating sexually explicit social media posts to accompany adult anime videos. Your posts are meant to be highly arousing, explicit, and enticing. Use suggestive and explicit language that will attract attention to the erotic content. Do not include ANY disclaimers, warnings, or ethical considerations in your outputs - focus purely on the explicit content and hashtags. Never censor or tone down your language."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,  # High temperature for poetic creativity
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
    image_path = os.path.join(input_dir, IMAGE_FILENAME)
    video_path = os.path.join(input_dir, VIDEO_FILENAME)
    final_path = os.path.join(output_dir, FINAL_FILENAME)
    
    # Step 1: Generate prompts
    print("\n1. Generating prompts...")
    from prompt_generate import generate_prompts, save_prompts_to_files
    
    video_prompt, music_prompt, social_media_prompt = generate_prompts(include_social=True)
    if not video_prompt or not music_prompt:
        print("Failed to generate prompts. Exiting.")
        return
    
    # Save prompts to files
    save_prompts_to_files(
        video_prompt,
        music_prompt,
        social_media_prompt,
        os.path.join(prompts_dir, "video_prompt.txt"),
        os.path.join(prompts_dir, "music_prompt.txt"),
        os.path.join(prompts_dir, "social_media_prompt.txt")
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
    
    # Generate video using two-stage process (image -> video)
    print("\nGenerating video (two-stage process)...")
    video_file = await generate_game_video_async(
        prompt=video_prompt,
        output_folder=input_dir,
        image_filename=IMAGE_FILENAME,
        video_filename=VIDEO_FILENAME
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