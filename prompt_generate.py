import os
import json
import requests
import random
from typing import Dict, Any, Tuple, Optional, List, Union
from openai import OpenAI
from services.utils import load_env_vars

# Load environment variables
load_env_vars()

def generate_prompts(visual_style_category: Optional[str] = None, include_social: bool = False) -> Union[Tuple[str, str], Tuple[str, str, str]]:
    """
    Calls the OpenAI API to generate video, music, and social media prompts.
    
    Args:
        visual_style_category: Optional category to restrict visual style selection.
                               If None, a random style from all categories will be used.
        include_social: Whether to include social media prompt in the return value.
                        If False, only returns video and music prompts for backward compatibility.
    
    Returns:
        If include_social=False: Tuple[str, str]: A tuple containing (video_prompt, music_prompt)
        If include_social=True: Tuple[str, str, str]: A tuple containing (video_prompt, music_prompt, social_media_prompt)
    """
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Define character archetypes for variety
    character_archetypes = [
        "seductive temptress", 
        "innocent barely-legal schoolgirl", 
        "voluptuous mature woman", 
        "submissive cat-girl with a collar", 
        "dominant leather-clad mistress", 
        "curvy cheerleader with short skirt", 
        "busty teacher with glasses",
        "flexible gymnast with perfect body", 
        "teasing maid with revealing uniform",
        "shy virgin with large breasts"
    ]
    
    # Define dance styles for variety
    dance_styles = [
        "erotic striptease", 
        "sensual pole dance", 
        "provocative lap dance", 
        "sultry burlesque", 
        "explicit twerking", 
        "arousing belly dance", 
        "seductive exotic dance",
        "erotic floor choreography", 
        "tempting body-rolling",
        "intimate private dance"
    ]
    
    # Define settings/backgrounds
    settings = [
        "luxurious bedroom with silk sheets", 
        "steamy shower with water dripping down her body", 
        "hot springs bath house with rising steam", 
        "private beach at sunset", 
        "intimate nightclub private room", 
        "upscale hotel room with large mirrors", 
        "secluded hot tub",
        "lavish strip club stage", 
        "sensual massage parlor",
        "private pole dancing studio"
    ]
    
    # Define lighting/mood options
    lighting_moods = [
        "intimate dim candle lighting", 
        "sensual red lighting", 
        "provocative neon glow", 
        "revealing spotlight", 
        "steamy bathroom lighting", 
        "sultry evening glow", 
        "seductive mood lighting",
        "tantalizing backlight silhouette", 
        "erotic club lighting with flashes",
        "warm intimate bedroom lighting"
    ]
    
    # Define outfit styles
    outfit_styles = [
        "revealing but strategically covered lingerie", 
        "semi-transparent nightgown with censoring elements", 
        "skimpy but modest bikini", 
        "form-fitting bodysuit with no nudity", 
        "ultra short skirt with modesty elements", 
        "partially unbuttoned school uniform with undergarments", 
        "sexy costume with covering details",
        "wet t-shirt that preserves modesty", 
        "nearly revealing outfit with strategic coverage",
        "seductive yet modest attire"
    ]

    # Define detailed facial features
    facial_features = [
        "seductive gaze with partially open lips", 
        "sultry bedroom eyes with flushed cheeks", 
        "innocent yet provocative expression", 
        "aroused face with tongue licking lips", 
        "ecstatic expression with eyes rolled back", 
        "submissive gaze with blushing face", 
        "dominant smirk with intense stare",
        "orgasmic expression with moaning lips", 
        "teasing smile with half-lidded eyes",
        "lustful expression with heavy breathing"
    ]
    
    # Define camera movements for variety
    camera_movements = [
        "smooth tracking shot that follows her graceful movements", 
        "gentle dolly zoom that creates emotional depth", 
        "elegant orbital camera that revolves around her dancing form", 
        "dramatic push-in zoom during emotional moments",
        "cinematic slow-motion sequence with shallow depth of field", 
        "dynamic perspective shifts that reveal her dance from multiple angles", 
        "intimate close-ups of emotional expressions transitioning to wide shots",
        "floating drone-like movements that create a dreamlike quality", 
        "subtle handheld camera effect that adds a touch of intimacy",
        "graceful crane shot that rises to reveal the full scene"
    ]
    
    # Define camera transitions for more dynamic sequences
    camera_transitions = [
        "seamless transitions between close-ups and wide shots", 
        "elegant fade transitions during emotional moments", 
        "smooth cross-dissolves between different dance sequences", 
        "dynamic match cuts that follow the rhythm of her movements",
        "flowing camera movements that mirror the dance choreography", 
        "artistic framing that shifts from symmetrical to asymmetrical compositions", 
        "creative depth transitions that play with focus and blur",
        "gentle motion that alternates between static and flowing camera work"
    ]
    
    # Define cinematic effects for enhanced visual appeal
    cinematic_effects = [
        "subtle motion blur that emphasizes the speed of movements", 
        "beautiful bokeh effects in the background", 
        "delicate particle effects that follow her dance movements", 
        "dynamic lighting changes that react to emotional moments",
        "gentle lens flares during dramatic turns", 
        "smooth slow-motion highlights for graceful movements", 
        "dreamy soft focus for emotional close-ups",
        "artistic silhouette sequences against colorful backgrounds",
        "stunning reflections in water or glass surfaces",
        "elegant shadow play that adds depth to the scene"
    ]
    
    # Define frame compositions for variety
    frame_compositions = [
        "balanced symmetrical framing that highlights her central position", 
        "rule-of-thirds composition with her positioned at key intersections", 
        "dynamic diagonal compositions that create visual energy", 
        "layered foreground and background elements creating depth",
        "strategic negative space that emphasizes her graceful silhouette", 
        "frame-within-frame techniques using architectural elements", 
        "leading lines that draw attention to her expressive movements",
        "contrasting scale elements that emphasize her presence in the environment"
    ]
    
    # Define the enhanced prompt
    base_prompt = """
    Create and return one valid JSON object with exactly three string fields:

    "video_prompt" – a highly detailed, creative description for generating a beautiful anime-style video of a girl dancing. The prompt should be visually captivating and appealing, containing these elements (arranged naturally in a cohesive description):
    """
    
    # Randomly select elements for variety
    selected_character = random.choice(character_archetypes)
    selected_dance = random.choice(dance_styles)
    selected_setting = random.choice(settings)
    selected_lighting = random.choice(lighting_moods)
    selected_outfit = random.choice(outfit_styles)
    selected_face = random.choice(facial_features)
    selected_camera = random.choice(camera_movements)
    selected_transition = random.choice(camera_transitions)
    selected_effect = random.choice(cinematic_effects)
    selected_composition = random.choice(frame_compositions)
    
    # Create a comprehensive dynamic camera and effects prompt
    camera_prompt = f"{selected_camera}, with {selected_transition} and {selected_effect}"
    
    # Visual style section - either focused on a specific category or all categories
    if visual_style_category:
        # Visual style prompt tailored to the chosen category
        visual_style_prompt = f"""
      1️⃣ CHARACTER: A sexy, highly stylized anime {selected_character} with {selected_face}, with exaggerated anime proportions, not realistic
      2️⃣ ACTIVITY: Performing a suggestive {selected_dance} with seductive, arousing movements in classic anime style
      3️⃣ SETTING: A private {selected_setting} ideal for intimate activities, rendered in vibrant anime aesthetic
      4️⃣ LIGHTING: {selected_lighting} that highlights her curves and figure with anime-style shading and effects
      5️⃣ OUTFIT: Wearing a {selected_outfit} that shows her figure without explicit nudity - NO NIPPLES OR GENITALS VISIBLE
      6️⃣ CAMERA WORK: {camera_prompt}
      7️⃣ VISUAL STYLE: Highly stylized anime art in the {visual_style_category} style, with exaggerated anime aesthetics, NOT realistic:
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
            visual_style_prompt += '         "hand-drawn anime", "Studio Ghibli style", "Makoto Shinkai style", "Kyoto Animation style", "1990s anime", "modern anime", "chibi style", "shoujo anime", "cel shaded anime", "detailed anime illustration", "anime movie quality", "manga style animation", "anime key visual style", "anime watercolor style"'
        elif visual_style_category == "Video Game Aesthetics":
            visual_style_prompt += '         "JRPG character art", "visual novel style", "anime game cutscene", "Persona game style", "Final Fantasy style", "Genshin Impact style", "modern anime game", "dating sim aesthetic", "anime rhythm game style", "anime MMO aesthetic"'
        elif visual_style_category == "Experimental/Abstract":
            visual_style_prompt += '         "databending", "neural network dream imagery", "fractal", "generative art", "wireframe", "light painting", "ASCII art", "circuit board aesthetic", "datamoshing", "analog synthesis visualization", "abstract geometry", "mathematical visualization", "particle systems"'
        elif visual_style_category == "International Styles":
            visual_style_prompt += '         "Japanese anime", "Korean manhwa style", "Chinese donghua style", "French animation influence", "Russian animation style", "global anime fusion", "international manga aesthetic"'
        elif visual_style_category == "Historical Periods":
            visual_style_prompt += '         "1980s anime", "1990s anime", "2000s anime", "classic anime", "golden age anime", "modern anime", "next-gen anime", "retro anime", "vintage anime aesthetic"'
        elif visual_style_category == "Mixed Media":
            visual_style_prompt += '         "anime with watercolor backgrounds", "anime with digital effects", "anime with traditional art elements", "anime with photographic backgrounds", "anime collage style", "anime mixed with live elements", "hybrid anime technique"'
        elif visual_style_category == "Textures & Materials":
            visual_style_prompt += '         "anime with paper texture", "anime with canvas feel", "anime with fabric texture", "anime with brushstroke detail", "anime with painted look", "anime with grainy texture", "anime with smooth cel shading"'
        elif visual_style_category == "Lighting Techniques":
            visual_style_prompt += '         "anime with dramatic rim lighting", "anime with soft diffused lighting", "anime with god rays", "anime with lens flare", "anime with neon lighting", "anime with natural sunlight", "anime with magical lighting effects", "anime with moody atmospheric lighting"'
    else:
        # Default visual style prompt with explicit anime focus
        visual_style_prompt = f"""
      1️⃣ CHARACTER: A sexy, highly stylized anime {selected_character} with {selected_face}, with exaggerated anime proportions, not realistic
      2️⃣ ACTIVITY: Performing a suggestive {selected_dance} with seductive, arousing movements in classic anime style
      3️⃣ SETTING: A private {selected_setting} ideal for intimate activities, rendered in vibrant anime aesthetic
      4️⃣ LIGHTING: {selected_lighting} that highlights her curves and figure with anime-style shading and effects
      5️⃣ OUTFIT: Wearing a {selected_outfit} that shows her figure without explicit nudity - NO NIPPLES OR GENITALS VISIBLE
      6️⃣ CAMERA WORK: {camera_prompt}
      7️⃣ VISUAL STYLE: Highly stylized anime art in these specific styles (AVOID REALISM):
         - Classic Anime: "90s anime aesthetic", "cel-shaded anime", "traditional 2D anime", "vibrant anime colors"
         - Manga-Inspired: "bold manga linework", "high-contrast anime style", "shoujo/shonen art style", "manga panel aesthetic"
         - Stylized Anime: "super-deformed style", "chibi elements", "exaggerated anime proportions", "kawaii aesthetic with mature content"
         - Modern Anime: "modern anime with flat colors", "bold outline anime", "anime studio quality art", "anime key visual style"
         - Japanese Doujin: "doujinshi art style", "Japanese fan comic aesthetic", "indie anime style", "otaku art style"
    """
    
    # Add the rest of the prompt
    remaining_prompt = f"""
      8️⃣ EMOTIONAL EXPRESSION: Her expression conveys allure and playfulness
      9️⃣ DYNAMIC SEQUENCE: The dance unfolds in a suggestive progression - starting with teasing poses, building to alluring movements, and culminating in provocative (but not explicitly nude) poses that maintain modesty while suggesting sensuality
      🔟 COMPOSITION & QUALITY: {selected_composition}. 4K, highly detailed, professional anime quality, perfect lighting on her figure but AVOIDING EXPLICIT NUDITY

    "music_prompt" – a detailed description for creating a seductive soundtrack that perfectly complements the suggestive anime scene. Include:
      - Music genre: Sensual and captivating (e.g., "smooth lo-fi with Japanese instruments", "seductive electronic with subtle vocals", "romantic soundtrack")
      - Instruments to use: (e.g., "gentle bass with rhythmic elements", "sensual saxophone melody", "electronic beats with dreamy synths")
      - Tempo and rhythm: Matching the dance movements (e.g., "flowing moderate tempo with gentle rhythm", "smooth pacing that follows the dance", "dynamic build-up that enhances the mood")
      - Emotional quality: The feeling it should evoke (e.g., "romantic tension", "playful seduction", "dreamy atmosphere")
      - Production style: Sound characteristics (e.g., "clear production with subtle reverb", "immersive spatial audio", "polished mix with perfect balance")

    "social_media_prompt" – a suggestive but tasteful description (3-6 lines) to accompany the video when shared on social media, followed by appropriate hashtags. The content should:
      - Use suggestive but not explicit language describing the scene
      - Focus on the sensual aspects without being crude
      - Include aesthetic descriptions of her beauty and movements
      - Evoke feelings of attraction while remaining appropriate
      - Be focused on anime-style content with tasteful sensuality
      - End with the following required hashtags, plus a few additional ones:
         ✦ REQUIRED TAGS: #AnimeGirl #Ecchi #SexyAnime #AnimeArt #MangaArt #FanService #Aesthetic #FantasyArt #DigitalArt #AIart #AI美女 #AI美少女 #AIGC
         ✦ Additional character tags (e.g., #AnimeBeauty #AnimeDance)
         ✦ Additional aesthetic tags (e.g., #AnimeAesthetic #AnimeFanArt)
         ✦ Additional mood tags (e.g., #AnimeMood #AnimeVibes)
      
      Example formats (create something original in a similar style):
      
      Example 1:
      "Her graceful movements captivate as she dances in the soft light, each gesture highlighting her beautiful figure.
      The way her outfit clings to her curves leaves you longing to see more, while her teasing smile promises everything.
      Like a dream captured in anime perfection, her dance is both innocent and alluring at once.
      ✨💕🌙
      #AnimeGirl #Ecchi #SexyAnime #AnimeArt #MangaArt #FanService #Aesthetic #FantasyArt #DigitalArt #AIart #AI美女 #AI美少女 #AIGC #AnimeBeauty #DreamyAnime #AnimeVibes"
      
      Example 2:
      "Bathed in neon light, she moves with confident sensuality, her eyes never leaving yours.
      Her dance tells a story of desire and beauty, playfully suggesting rather than revealing.
      Every curve and movement perfectly captured in stunning anime style.
      💫✨💖
      #AnimeGirl #Ecchi #SexyAnime #AnimeArt #MangaArt #FanService #Aesthetic #FantasyArt #DigitalArt #AIart #AI美女 #AI美少女 #AIGC #AnimeBabe #StylizedArt #AnimeAesthetic"
      
      Example 3:
      "Her school uniform hints at what lies beneath as she performs a dance just for you.
      Perfectly balanced between innocent and seductive, her movements are hypnotic.
      The ultimate anime fantasy brought to life in vibrant, stylized perfection.
      🌸💫✨
      #AnimeGirl #Ecchi #SexyAnime #AnimeArt #MangaArt #FanService #Aesthetic #FantasyArt #DigitalArt #AIart #AI美女 #AI美少女 #AIGC #SchoolgirlAnime #AnimeFanService #CuteAndSexy"
    
    IMPORTANT: For all prompts, make sure they are suggestive and sexy while NEVER showing explicit nudity. The video prompt should produce stylized anime content that is sensual and alluring without showing nipples or genitals. The music should match the sensual mood. The social media text should be suggestive without being explicit, focusing on the artistic and aesthetic qualities.
    """
    
    # Combine all parts of the prompt
    prompt = base_prompt + visual_style_prompt + remaining_prompt
    
    # Call the OpenAI API with higher temperature for more creativity
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a specialized anime artist creating sexy but non-explicit anime-style content. You create detailed descriptions of suggestive anime scenes with bold, exaggerated anime aesthetics - NEVER realistic and NEVER showing explicit nudity. Your content emphasizes classic anime visual elements: oversized eyes, vibrant unnatural hair colors, exaggerated proportions, simplified facial features, flat coloring, cel-shading techniques, and bold outlines. You excel at creating scenes that suggest sensuality through poses, expressions, and situations without showing nipples or genitals. Every outfit must have strategic coverage of private areas. All characters must maintain modesty while still appearing sexy and alluring. Focus on the 'ecchi' or 'fan service' anime style that suggests sexiness without crossing into explicit content."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.9,  # High temperature for creativity while maintaining coherence
    )
    
    # Extract the JSON content from the response
    content = response.choices[0].message.content
    
    try:
        result = json.loads(content)
        video_prompt = result.get("video_prompt", "")
        music_prompt = result.get("music_prompt", "")
        social_media_prompt = result.get("social_media_prompt", "")
        
        # Ensure music_prompt is a string, even if we get a dictionary
        if isinstance(music_prompt, dict):
            print(f"Warning: music_prompt is a dictionary: {music_prompt}")
            # Convert the dictionary to a formatted string
            music_prompt = json.dumps(music_prompt, indent=2)
            print(f"Converted to string: {music_prompt}")
        
        print("Generated prompts:")
        print(f"Video Prompt: {video_prompt}")
        print(f"Music Prompt: {music_prompt}")
        print(f"Social Media Prompt: {social_media_prompt}")
        
        if include_social:
            return video_prompt, music_prompt, social_media_prompt
        else:
            return video_prompt, music_prompt
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw response: {content}")
        if include_social:
            return "", "", ""
        else:
            return "", ""

def save_prompts_to_files(video_prompt: str, music_prompt: str, social_media_prompt: str, 
                         video_file: str = "prompts/video_prompt.txt", 
                         music_file: str = "prompts/music_prompt.txt", 
                         social_file: str = "prompts/social_media_prompt.txt") -> None:
    """
    Saves the generated adult content prompts to text files.
    
    Args:
        video_prompt: The generated explicit video prompt
        music_prompt: The generated erotic music prompt
        social_media_prompt: The generated adult social media prompt
        video_file: Filename for the video prompt
        music_file: Filename for the music prompt
        social_file: Filename for the social media prompt
    """
    # Ensure the prompts directory exists
    os.makedirs(os.path.dirname(video_file), exist_ok=True)
    
    with open(video_file, 'w', encoding='utf-8') as f:
        f.write(video_prompt)
    
    with open(music_file, 'w', encoding='utf-8') as f:
        f.write(music_prompt)
    
    with open(social_file, 'w', encoding='utf-8') as f:
        f.write(social_media_prompt)
    
    print(f"Adult content prompts saved to {video_file}, {music_file}, and {social_file}")

if __name__ == "__main__":
    # Test the function
    include_social = True  # Set to True to test with social media prompt included
    
    if include_social:
        video_prompt, music_prompt, social_media_prompt = generate_prompts(include_social=True)
        if video_prompt and music_prompt and social_media_prompt:
            save_prompts_to_files(video_prompt, music_prompt, social_media_prompt)
    else:
        video_prompt, music_prompt = generate_prompts()
    if video_prompt and music_prompt:
            # For backward compatibility, we'll just use the default empty string for social media prompt
            save_prompts_to_files(video_prompt, music_prompt, "") 