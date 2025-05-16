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
    # Make sure OPENAI_API_KEY environment variable is set or pass directly
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Define the prompt
    prompt = """
    Create and return one valid JSON object with exactly two string fields:

    "video_prompt" – a single, compact sentence that will generate a 4‑6 second perfectly looping gameplay video clip, containing (in order, comma‑separated)
      1️⃣ game genre + core mechanic,
      2️⃣ environment/setting (terrain, weather, time‑of‑day, mood),
      3️⃣ main character appearance & motion (silhouette, outfit, current animation pose),
      4️⃣ up to three key enemies or interactive objects and what they're doing,
      5️⃣ gameplay moment unfolding right now,
      6️⃣ cinematic camera move,
      7️⃣ art style & render look,
      8️⃣ lighting & colour palette,
      9️⃣ UI/HUD elements in frame,
      🔟 video specs & tags (e.g., "4 K 60 fps, 16:9, seamless loop, highly detailed, trending on ArtStation, cinematic depth of field").

    "music_prompt" – one vivid sentence that, using the exact string in "video_prompt" as sole context, instructs an AI music generator to create a perfectly looping 4‑6 second soundtrack, specifying music genre, primary instruments, tempo in BPM, rhythmic feel, dominant key or mode, mood adjectives matching the setting, signature SFX layers synced to on‑screen action, spatial mix notes (reverb type, stereo width, depth of field), and mastering style (loudness target, tape‑saturated warmth or crystalline clarity).
    """
    
    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # Use an appropriate model
        messages=[
            {"role": "system", "content": "You are a creative assistant that generates JSON content."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
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