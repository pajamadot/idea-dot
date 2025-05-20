import os
import json
import requests
from typing import Dict, Any, Tuple, Optional
from openai import OpenAI
from services.utils import load_env_vars

# Load environment variables
load_env_vars()

def generate_prompts(visual_style_category: Optional[str] = None) -> Tuple[str, str]:
    """
    Calls the OpenAI API to generate video and music prompts.
    
    Args:
        visual_style_category: Optional category to restrict visual style selection.
                               If None, a random style from all categories will be used.
    
    Returns:
        Tuple[str, str]: A tuple containing (video_prompt, music_prompt)
    """
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Define the enhanced prompt
    base_prompt = """
    Create and return one valid JSON object with exactly two string fields:

    "video_prompt" – a highly detailed, creative description that will generate a unique gameplay video clip. The prompt should be highly experimental and visually distinctive, containing (in no particular order, but all elements must be included):
      1️⃣ game genre + innovative core mechanic (e.g., "gravity-shifting platformer" or "time-bending stealth"),
      2️⃣ unique environment/setting with specific mood and atmosphere (e.g., "bioluminescent underwater ruins" or "floating islands in a storm"),
      3️⃣ distinctive main character with unique abilities (e.g., "shapeshifting shadow mage" or "mechanical dragon rider"),
      4️⃣ creative enemies/obstacles with unique behaviors (e.g., "mirror-image doppelgangers" or "living architecture"),
      5️⃣ dynamic gameplay moment with special effects (e.g., "character splits into three time-clones" or "environment morphs between seasons"),
      6️⃣ cinematic camera move that enhances the action (e.g., "dramatic slow-mo zoom" or "dynamic orbit shot"),
    """
    
    # Visual style section - either focused on a specific category or all categories
    if visual_style_category:
        # Visual style prompt tailored to the chosen category
        visual_style_prompt = f"""
      7️⃣ VISUAL STYLE - randomly select ONE visual style from the {visual_style_category} category:
    """
        
        # Add the appropriate styles based on the category
        if visual_style_category == "Traditional Art Styles":
            visual_style_prompt += '         "watercolor painting", "oil painting", "charcoal sketch", "ink wash", "ukiyo-e woodblock print", "fresco", "medieval manuscript illumination", "stained glass", "pastel drawing", "gouache painting"'
        elif visual_style_category == "Modern Art Movements":
            visual_style_prompt += '         "cubist", "surrealist", "impressionist", "expressionist", "art nouveau", "art deco", "pop art", "bauhaus", "brutalist", "minimalist", "abstract expressionism", "futurism", "dadaism", "fauvism", "de stijl"'
        elif visual_style_category == "Digital & Contemporary":
            visual_style_prompt += '         "vaporwave", "glitch art", "low poly", "vector art", "flat design", "3D render", "photogrammetry", "procedural generation", "holographic", "cyberpunk", "solarpunk"'
        elif visual_style_category == "Pixel Art Styles":
            visual_style_prompt += '         "8-bit pixel art", "16-bit pixel art", "32-bit pixel art", "isometric pixel art", "1-bit pixel art", "Game Boy 4-color pixel art", "pixel art dithering", "outlined pixel art", "hi-bit pixel art", "rotoscoped pixel art", "pixel art with limited palette", "MSX pixel art", "Commodore 64 pixel art", "CGA 4-color pixel art", "EGA 16-color pixel art", "demoscene pixel art"'
        elif visual_style_category == "Film & Photography":
            visual_style_prompt += '         "film noir", "technicolor", "sepia tone", "analog photography", "infrared photography", "tilt-shift", "long exposure", "time-lapse", "daguerreotype", "polaroid", "cinematic widescreen", "fisheye lens", "bokeh", "HDR photography", "cross-processed film"'
        elif visual_style_category == "Animation Styles":
            visual_style_prompt += '         "hand-drawn animation", "stop motion", "claymation", "rotoscope", "anime", "cartoon", "cel shading", "South Park paper cut-out", "silhouette animation", "motion graphics", "rubber hose animation", "limited animation", "Disney renaissance style", "UPA flat style", "puppet animation"'
        elif visual_style_category == "Video Game Aesthetics":
            visual_style_prompt += '         "16-bit SNES", "32-bit PS1", "Nintendo 64 low-poly", "Dreamcast", "GameBoy 4-color", "PS2 era", "modern AAA", "Unity engine", "Unreal Engine", "voxel-based", "2.5D", "text-based adventure", "vector graphics arcade", "wireframe"'
        elif visual_style_category == "Experimental/Abstract":
            visual_style_prompt += '         "databending", "neural network dream imagery", "fractal", "generative art", "wireframe", "light painting", "ASCII art", "circuit board aesthetic", "datamoshing", "analog synthesis visualization", "abstract geometry", "mathematical visualization", "particle systems"'
        elif visual_style_category == "International Styles":
            visual_style_prompt += '         "Russian constructivism", "Mexican muralism", "Chinese ink painting", "Aboriginal dot painting", "Indian miniature painting", "Persian miniature", "African mask-inspired", "Japanese Rinpa", "Scandinavian design", "Bauhaus", "Memphis design", "Celtic illumination", "Byzantine iconography"'
        elif visual_style_category == "Historical Periods":
            visual_style_prompt += '         "ancient Egyptian", "Byzantine mosaic", "Gothic", "Renaissance", "Baroque", "Rococo", "Victorian", "1920s", "1950s", "1980s", "1990s web design", "Y2K aesthetic", "medieval manuscript", "Art Nouveau", "Modernism"'
        elif visual_style_category == "Mixed Media":
            visual_style_prompt += '         "collage", "decoupage", "photomontage", "assemblage", "found object art", "paper cutting", "textile art", "mosaic", "mixed media painting", "encaustic", "sculpture photography", "digital collage", "hybrid illustration"'
        elif visual_style_category == "Textures & Materials":
            visual_style_prompt += '         "chalk", "crayon", "pencil sketch", "blueprint", "newspaper print", "risograph", "screen printing", "woodcut", "linocut", "etching", "lithography", "letterpress", "batik", "marbling", "cyanotype"'
        elif visual_style_category == "Lighting Techniques":
            visual_style_prompt += '         "chiaroscuro", "noir lighting", "golden hour", "blue hour", "bioluminescence", "neon", "strobe effect", "volumetric lighting", "ray tracing", "global illumination", "lens flare", "light leaks", "ambient occlusion", "rim lighting", "silhouette lighting"'
    else:
        # Default visual style prompt with all categories
        visual_style_prompt = """
      7️⃣ VISUAL STYLE - randomly select ONE visual style from this extensive list:
         - Traditional Art Styles: "watercolor painting", "oil painting", "charcoal sketch", "ink wash", "ukiyo-e woodblock print", "fresco", "medieval manuscript illumination", "stained glass", "pastel drawing", "gouache painting"
         - Modern Art Movements: "cubist", "surrealist", "impressionist", "expressionist", "art nouveau", "art deco", "pop art", "bauhaus", "brutalist", "minimalist", "abstract expressionism", "futurism", "dadaism", "fauvism", "de stijl"
         - Digital & Contemporary: "vaporwave", "glitch art", "low poly", "vector art", "flat design", "3D render", "photogrammetry", "procedural generation", "holographic", "cyberpunk", "solarpunk"
         - Pixel Art Styles: "8-bit pixel art", "16-bit pixel art", "32-bit pixel art", "isometric pixel art", "1-bit pixel art", "Game Boy 4-color pixel art", "pixel art dithering", "outlined pixel art", "hi-bit pixel art", "rotoscoped pixel art", "pixel art with limited palette", "MSX pixel art", "Commodore 64 pixel art", "CGA 4-color pixel art", "EGA 16-color pixel art", "demoscene pixel art"
         - Film & Photography: "film noir", "technicolor", "sepia tone", "analog photography", "infrared photography", "tilt-shift", "long exposure", "time-lapse", "daguerreotype", "polaroid", "cinematic widescreen", "fisheye lens", "bokeh", "HDR photography", "cross-processed film"
         - Animation Styles: "hand-drawn animation", "stop motion", "claymation", "rotoscope", "anime", "cartoon", "cel shading", "South Park paper cut-out", "silhouette animation", "motion graphics", "rubber hose animation", "limited animation", "Disney renaissance style", "UPA flat style", "puppet animation"
         - Video Game Aesthetics: "16-bit SNES", "32-bit PS1", "Nintendo 64 low-poly", "Dreamcast", "GameBoy 4-color", "PS2 era", "modern AAA", "Unity engine", "Unreal Engine", "voxel-based", "2.5D", "text-based adventure", "vector graphics arcade", "wireframe"
         - Experimental/Abstract: "databending", "neural network dream imagery", "fractal", "generative art", "wireframe", "light painting", "ASCII art", "circuit board aesthetic", "datamoshing", "analog synthesis visualization", "abstract geometry", "mathematical visualization", "particle systems"
         - International Styles: "Russian constructivism", "Mexican muralism", "Chinese ink painting", "Aboriginal dot painting", "Indian miniature painting", "Persian miniature", "African mask-inspired", "Japanese Rinpa", "Scandinavian design", "Bauhaus", "Memphis design", "Celtic illumination", "Byzantine iconography"
         - Historical Periods: "ancient Egyptian", "Byzantine mosaic", "Gothic", "Renaissance", "Baroque", "Rococo", "Victorian", "1920s", "1950s", "1980s", "1990s web design", "Y2K aesthetic", "medieval manuscript", "Art Nouveau", "Modernism"
         - Mixed Media: "collage", "decoupage", "photomontage", "assemblage", "found object art", "paper cutting", "textile art", "mosaic", "mixed media painting", "encaustic", "sculpture photography", "digital collage", "hybrid illustration"
         - Textures & Materials: "chalk", "crayon", "pencil sketch", "blueprint", "newspaper print", "risograph", "screen printing", "woodcut", "linocut", "etching", "lithography", "letterpress", "batik", "marbling", "cyanotype"
         - Lighting Techniques: "chiaroscuro", "noir lighting", "golden hour", "blue hour", "bioluminescence", "neon", "strobe effect", "volumetric lighting", "ray tracing", "global illumination", "lens flare", "light leaks", "ambient occlusion", "rim lighting", "silhouette lighting"
    """
    
    # Add the rest of the prompt
    remaining_prompt = """
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
    
    # Combine all parts of the prompt
    prompt = base_prompt + visual_style_prompt + remaining_prompt
    
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