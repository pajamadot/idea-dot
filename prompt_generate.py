import os
import json
import requests
from typing import Dict, Any, Tuple
from openai import OpenAI
from services.utils import load_env_vars

# Load environment variables
load_env_vars()

def generate_prompts() -> Tuple[str, str]:
    """
    Calls the OpenAI API to generate video and music prompts.
    
    Returns:
        Tuple[str, str]: A tuple containing (video_prompt, music_prompt)
    """
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Define the enhanced prompt
    prompt = """
    Create and return one valid JSON object with exactly two string fields:

    "video_prompt" – a single, compact sentence that will generate a 4‑6 second perfectly looping gameplay video clip. The prompt should be highly creative and unique, containing (in order, comma‑separated):
      1️⃣ game genre + innovative core mechanic (e.g., "gravity-shifting platformer" or "time-bending stealth"),
      2️⃣ unique environment/setting with specific mood and atmosphere (e.g., "bioluminescent underwater ruins" or "floating islands in a storm"),
      3️⃣ distinctive main character with unique abilities (e.g., "shapeshifting shadow mage" or "mechanical dragon rider"),
      4️⃣ creative enemies/obstacles with unique behaviors (e.g., "mirror-image doppelgangers" or "living architecture"),
      5️⃣ dynamic gameplay moment with special effects (e.g., "character splits into three time-clones" or "environment morphs between seasons"),
      6️⃣ cinematic camera move that enhances the action (e.g., "dramatic slow-mo zoom" or "dynamic orbit shot"),
      7️⃣ distinctive art style with unique visual elements (e.g., "hand-painted watercolor" or "neon-noir cyberpunk"),
      8️⃣ creative lighting & color palette that sets the mood (e.g., "aurora borealis lighting" or "monochrome with selective color"),
      9️⃣ minimal but stylish HUD elements (e.g., "floating holographic displays" or "environment-integrated UI"),
      🔟 video specs & artistic direction (e.g., "4K 60fps, 16:9, seamless loop, highly detailed, trending on ArtStation, cinematic depth of field").

    "music_prompt" – one vivid sentence that creates a unique soundtrack matching the video's mood and action. Include:
      - Innovative music genre or fusion (e.g., "orchestral dubstep" or "ambient metal")
      - Unique instruments or sound design (e.g., "glass harmonica and digital glitches" or "prepared piano and field recordings")
      - Specific tempo and rhythm pattern (e.g., "irregular 7/8 time signature" or "polyrhythmic 120 BPM")
      - Creative mood and atmosphere (e.g., "dreamlike tension" or "cosmic wonder")
      - Dynamic sound effects synced to gameplay (e.g., "reality-bending sound design" or "environmental audio storytelling")
      - Spatial audio design (e.g., "binaural soundscape" or "3D audio positioning")
      - Mastering style that enhances the experience (e.g., "analog warmth with digital precision" or "immersive surround mix")
    """
    
    # Call the OpenAI API with higher temperature for more creativity
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a highly creative game designer and composer who specializes in innovative and unique concepts."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.9,  # Increased temperature for more creative variations
    )
    
    # Extract the JSON content from the response
    content = response.choices[0].message.content
    
    try:
        result = json.loads(content)
        video_prompt = result.get("video_prompt", "")
        music_prompt = result.get("music_prompt", "")
        
        print("Generated prompts:")
        print(f"Video Prompt: {video_prompt}")
        print(f"Music Prompt: {music_prompt}")
        
        return video_prompt, music_prompt
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw response: {content}")
        return "", ""

def save_prompts_to_files(video_prompt: str, music_prompt: str, video_file: str = "video_prompt.txt", music_file: str = "music_prompt.txt") -> None:
    """
    Saves the generated prompts to text files.
    
    Args:
        video_prompt: The generated video prompt
        music_prompt: The generated music prompt
        video_file: Filename for the video prompt
        music_file: Filename for the music prompt
    """
    with open(video_file, 'w') as f:
        f.write(video_prompt)
    
    with open(music_file, 'w') as f:
        f.write(music_prompt)
    
    print(f"Prompts saved to {video_file} and {music_file}")

if __name__ == "__main__":
    # Test the function
    video_prompt, music_prompt = generate_prompts()
    
    if video_prompt and music_prompt:
        save_prompts_to_files(video_prompt, music_prompt) 