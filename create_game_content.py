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
    Generate engaging Twitter content using GPT-4.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""
    Create a viral-worthy, slightly controversial tweet about this game concept:
    Video: {video_prompt}
    Music: {music_prompt}
    
    Requirements:
    1. Keep it under 280 characters for the main tweet body
    2. Start with a strong, attention-grabbing hook that might be slightly controversial
    3. Create emotional engagement through:
       - Provocative questions
       - Bold statements
       - Industry challenges
       - Future predictions
    4. Include a clear call-to-action that encourages debate (e.g., "Would you play this?", "Drop a ❤️ if you want to try this", "RT if you think this is the future of gaming")
    5. Add 3-5 relevant emojis to enhance readability and engagement
    6. Include AT LEAST 20 strategic hashtags in this format:
       <Tweet body>
       <Line break>
       #hashtag1 #hashtag2 #hashtag3 ...
       
    Include the following categories of hashtags:
       - REQUIRED: #AIGeneratedGameplay
       - GAMING INDUSTRY (5-6): #gamedev #indiegame #gamedevelopment #gamingcommunity #esports #VGdevelopment
       - GAMING PLATFORMS (3-4): #PCgaming #mobilegaming #consolegaming #PlayStation #Xbox #NintendoSwitch
       - GAMING GENRES (3-4): #RPG #FPS #strategy #openworld #simulation #adventure #sportsGame
       - TECH & AI (3-4): #AI #ArtificialIntelligence #MachineLearning #AIArt #AIgames #tech #futuretech
       - VIRAL & TRENDING (3-4): #viral #trending #insane #mindblowing #nextlevel #epicgaming
       - EMOTIONS & REACTIONS (2-3): #stunning #mindblowing #gorgeous #awesome #epicwin
       - CALL TO ACTION (1-2): #MustPlay #MustSee #CheckThisOut #RT

    Format:
       <Controversial hook>
       <Emotional engagement>
       <Call to action>
       <Line break>
       #hashtag1 #hashtag2 #hashtag3 ... (at least 20 hashtags)

    Controversial Elements (use 1-2):
    - Challenge industry norms
    - Question traditional game design
    - Suggest revolutionary changes
    - Compare to existing games
    - Make bold predictions
    - Address current gaming controversies
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a viral game content strategist and copywriter for an AI-driven game studio. Your tweets are known for their high engagement rates and ability to go viral through slightly controversial but thought-provoking content. You excel at creating emotionally resonant content that makes viewers stop scrolling and engage in discussion. You're not afraid to challenge industry norms while maintaining professionalism. You're an expert at hashtag strategy and know exactly which gaming hashtags are trending and will maximize engagement."},
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
    image_path = os.path.join(input_dir, IMAGE_FILENAME)
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