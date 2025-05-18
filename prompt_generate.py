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

    "video_prompt" – a highly detailed, creative description that will generate a unique gameplay video clip. The prompt should be highly experimental and visually distinctive, containing (in no particular order, but all elements must be included):
      1️⃣ game genre + innovative core mechanic (e.g., "gravity-shifting platformer" or "time-bending stealth"),
      2️⃣ unique environment/setting with specific mood and atmosphere (e.g., "bioluminescent underwater ruins" or "floating islands in a storm"),
      3️⃣ distinctive main character with unique abilities (e.g., "shapeshifting shadow mage" or "mechanical dragon rider"),
      4️⃣ creative enemies/obstacles with unique behaviors (e.g., "mirror-image doppelgangers" or "living architecture"),
      5️⃣ dynamic gameplay moment with special effects (e.g., "character splits into three time-clones" or "environment morphs between seasons"),
      6️⃣ cinematic camera move that enhances the action (e.g., "dramatic slow-mo zoom" or "dynamic orbit shot"),
      7️⃣ VISUAL STYLE - randomly select ONE visual style from this extensive list:
         - Traditional Art Styles: "watercolor painting", "oil painting", "charcoal sketch", "ink wash", "ukiyo-e woodblock print", "fresco", "medieval manuscript illumination", "stained glass"
         - Modern Art Movements: "cubist", "surrealist", "impressionist", "expressionist", "art nouveau", "art deco", "pop art", "bauhaus", "brutalist", "minimalist", "abstract expressionism"
         - Digital & Contemporary: "vaporwave", "glitch art", "low poly", "pixel art", "voxel", "isometric", "vector art", "flat design", "3D render", "photogrammetry", "procedural generation"
         - Film & Photography: "film noir", "technicolor", "sepia tone", "analog photography", "infrared photography", "tilt-shift", "long exposure", "time-lapse", "daguerreotype", "polaroid"
         - Animation Styles: "hand-drawn animation", "stop motion", "claymation", "rotoscope", "anime", "cartoon", "cel shading", "South Park paper cut-out", "silhouette animation"
         - Video Game Aesthetics: "16-bit SNES", "32-bit PS1", "Nintendo 64 low-poly", "Dreamcast", "GameBoy 4-color", "PS2 era", "modern AAA", "Unity engine", "Unreal Engine"
         - Experimental/Abstract: "databending", "neural network dream imagery", "fractal", "generative art", "wireframe", "holographic", "light painting", "ASCII art", "circuit board aesthetic"
         - International Styles: "Russian constructivism", "Mexican muralism", "Chinese ink painting", "Aboriginal dot painting", "Indian miniature painting", "Persian miniature", "African mask-inspired"
         - Historical Periods: "ancient Egyptian", "Byzantine mosaic", "Gothic", "Renaissance", "Baroque", "Rococo", "Victorian", "1920s", "1950s", "1980s", "1990s web design", "Y2K aesthetic"
         - Mixed Media: "collage", "decoupage", "photomontage", "assemblage", "found object art", "paper cutting", "textile art", "mosaic"
         - Textures & Materials: "chalk", "crayon", "pencil sketch", "blueprint", "newspaper print", "risograph", "screen printing", "woodcut", "linocut", "etching", "lithography"
         - Lighting Techniques: "chiaroscuro", "noir lighting", "golden hour", "blue hour", "bioluminescence", "neon", "strobe effect", "volumetric lighting", "ray tracing", "global illumination"
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
    
    IMPORTANT: For the video_prompt, do not follow a predictable format. Arrange the required elements in a creative, natural-sounding description where the elements flow together coherently but in a random order. The final prompt should read as a cohesive, imaginative description rather than a mechanical list of elements.
    """
    
    # Call the OpenAI API with higher temperature for more creativity
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a highly experimental game designer and visual artist who specializes in creating the most unique, visually striking, and unconventional gaming concepts. You love to break visual boundaries and create art styles that have never been seen before. You're known for your wildly creative style combinations and unexpected aesthetic choices."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=1.0,  # Maximum temperature for extreme creativity and randomness
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