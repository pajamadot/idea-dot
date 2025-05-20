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
        "gentle shy schoolgirl", 
        "confident fashionable idol", 
        "elegant graceful princess", 
        "energetic sporty girl", 
        "mysterious magical girl", 
        "cute cheerful girl-next-door", 
        "sophisticated mature woman",
        "playful cat-girl hybrid", 
        "dreamy fairy-like girl",
        "passionate dancer in traditional outfit"
    ]
    
    # Define dance styles for variety
    dance_styles = [
        "graceful ballet", 
        "upbeat j-pop choreography", 
        "elegant traditional Japanese dance", 
        "energetic hip-hop", 
        "rhythmic contemporary", 
        "playful idol dance", 
        "flowing ribbon dance",
        "expressive interpretive dance", 
        "precise technical choreography",
        "free-spirited improvisational dance"
    ]
    
    # Define settings/backgrounds
    settings = [
        "cherry blossom garden", 
        "neon-lit city street at night", 
        "magical fairy forest", 
        "sunset beach", 
        "elegant ballroom", 
        "dreamy clouds with floating islands", 
        "cozy cafe interior",
        "futuristic cityscape", 
        "mystical ancient temple",
        "enchanted garden with glowing flowers"
    ]
    
    # Define lighting/mood options
    lighting_moods = [
        "soft golden hour glow", 
        "dramatic stage lighting", 
        "dreamy pastel lighting", 
        "magical sparkling particles", 
        "warm intimate lighting", 
        "cool moonlit atmosphere", 
        "colorful rainbow lighting",
        "gentle ambient mood lighting", 
        "dramatic silhouette backlighting",
        "ethereal glowing aura"
    ]
    
    # Define outfit styles
    outfit_styles = [
        "flowing delicate dress", 
        "stylish modern school uniform", 
        "elaborate fantasy costume", 
        "cute casual outfit", 
        "elegant traditional kimono", 
        "fashionable contemporary clothes", 
        "magical girl transformation outfit",
        "glamorous stage performance costume", 
        "fairy-like ethereal gown",
        "sporty yet feminine activewear"
    ]

    # Define detailed facial features
    facial_features = [
        "gentle innocent smile with sparkling eyes", 
        "elegant refined features with a mysterious smile", 
        "cute expressive face with large adorable eyes", 
        "confident radiant smile with a playful wink", 
        "serene beautiful expression with long eyelashes", 
        "joyful bright smile with rosy cheeks", 
        "dreamy wistful expression with delicate features",
        "shy blushing face with a gentle gaze", 
        "charming dimpled smile with captivating eyes",
        "graceful noble features with a warm smile"
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
      1️⃣ CHARACTER: A beautiful anime {selected_character} with {selected_face}
      2️⃣ ACTIVITY: Performing a captivating {selected_dance} with graceful flowing movements
      3️⃣ SETTING: A stunning {selected_setting} that enhances the mood
      4️⃣ LIGHTING: {selected_lighting} that creates a romantic atmosphere
      5️⃣ OUTFIT: Wearing a {selected_outfit} that complements her movements
      6️⃣ CAMERA WORK: {camera_prompt}
      7️⃣ VISUAL STYLE: High-quality anime rendering in the {visual_style_category} style:
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
        # Default visual style prompt with anime focus
        visual_style_prompt = f"""
      1️⃣ CHARACTER: A beautiful anime {selected_character} with {selected_face}
      2️⃣ ACTIVITY: Performing a captivating {selected_dance} with graceful flowing movements
      3️⃣ SETTING: A stunning {selected_setting} that enhances the mood
      4️⃣ LIGHTING: {selected_lighting} that creates a romantic atmosphere
      5️⃣ OUTFIT: Wearing a {selected_outfit} that complements her movements
      6️⃣ CAMERA WORK: {camera_prompt}
      7️⃣ VISUAL STYLE: High-quality anime rendering in one of these styles:
         - Classic Anime: "90s anime aesthetic", "hand-drawn anime", "cel shaded anime", "Studio Ghibli inspired", "Makoto Shinkai style", "Kyoto Animation style"
         - Modern Anime: "detailed modern anime", "high-budget anime movie quality", "anime key visual style", "professional anime illustration style"
         - Stylized Anime: "anime watercolor style", "anime pop art style", "anime minimalist style", "anime with dramatic lighting"
         - Digital Anime: "digital anime illustration", "anime 3D rendering", "anime with digital effects", "anime with particle effects"
         - Game-Inspired: "Genshin Impact style anime", "JRPG character style", "visual novel aesthetic", "anime game cutscene style"
    """
    
    # Add the rest of the prompt
    remaining_prompt = f"""
      8️⃣ EMOTIONAL EXPRESSION: Her expression conveys deep emotion, captivating the viewer
      9️⃣ DYNAMIC SEQUENCE: The dance unfolds as a visual story with a beginning, middle, and climax - starting with gentle movements, building to impressive technical dance elements, and culminating in an emotionally powerful finale with perfect timing and rhythm
      🔟 COMPOSITION & QUALITY: {selected_composition}. 4K, highly detailed, professional anime production quality, trending on pixiv, perfect lighting

    "music_prompt" – a detailed description for creating a beautiful, emotional soundtrack that perfectly complements the anime girl's dance. Include:
      - Music genre: Emotional, beautiful, and captivating (e.g., "emotional lo-fi with Japanese instruments", "dreamy electronic pop", "orchestral anime theme with piano")
      - Instruments to use: (e.g., "gentle piano melody with soft strings", "electronic beats with traditional Japanese instruments", "orchestral arrangement with female vocals")
      - Tempo and rhythm: Matching the dance movements (e.g., "flowing 80 BPM with gentle rhythm", "moderate tempo with emotional swells", "dynamic pacing that follows the dance")
      - Emotional quality: The feeling it should evoke (e.g., "wistful nostalgia with hopeful undertones", "deep romantic longing", "joyful yet touching emotional journey")
      - Production style: Sound characteristics (e.g., "crystal clear production with subtle reverb", "warm analog feeling with soft compression", "spacious mix with perfect balance")

    "social_media_prompt" – a purely poetic, beautiful mini-story (3-6 lines) to accompany the video when shared on social media, followed by aesthetic anime hashtags. The content should:
      - Tell a brief, emotionally touching story related to the dancing anime girl
      - Use elegant, poetic language with beautiful imagery that complements the visual
      - Include delicate, artistic elements that create an emotional connection
      - Evoke feelings of beauty, wonder, serenity, or gentle emotion
      - Be purely focused on artistic beauty and emotional resonance
      - End with the following required hashtags, plus a few additional aesthetic ones:
         ✦ REQUIRED TAGS: #Catgirl #AnimeGirl #Kawaii #Cosplay #AnimeArt #MangaArt #CuteOverload #Aesthetic #FantasyArt #DigitalArt #AIart #AI美女 #AI美少女 #AIGC
         ✦ Additional elegant character tags (e.g., #DancingBeauty #GracefulMoments)
         ✦ Additional artistic aesthetic tags (e.g., #VisualPoetry #AnimeLove)
         ✦ Additional emotional mood tags (e.g., #SereneBeauty #GentleEmotions)
      
      Example story formats (create something original in a similar style):
      
      Example 1:
      "In a garden of cherry blossoms, she dances with whispers of eternity.
      Each step creates ripples across time, each gesture paints memories in the air.
      Like poetry in motion, her soul speaks what words cannot express.
      ✨🌸✨
      #Catgirl #AnimeGirl #Kawaii #Cosplay #AnimeArt #MangaArt #CuteOverload #Aesthetic #FantasyArt #DigitalArt #AIart #AI美女 #AI美少女 #AIGC #CherryBlossomDance #VisualPoetry #DancingBeauty"
      
      Example 2:
      "Her dance is a secret language of the heart.
      Time suspends in the space between heartbeats, enchanted.
      With each graceful turn, emotions bloom like flowers after rain.
      This moment—a painting brought to life, a dream given form.
      ✨🌙💫
      #Catgirl #AnimeGirl #Kawaii #Cosplay #AnimeArt #MangaArt #CuteOverload #Aesthetic #FantasyArt #DigitalArt #AIart #AI美女 #AI美少女 #AIGC #DreamlikeScene #SereneVibes #GentleEmotions"
      
      Example 3:
      "Dancing between shadow and light, she carries moonlight in her movements.
      Yesterday's silence transformed into today's visual melody.
      Her dance tells stories of fleeting beauty, of moments to be treasured.
      For those with hearts to see—this ephemeral beauty is eternal.
      💕✨🌙
      #Catgirl #AnimeGirl #Kawaii #Cosplay #AnimeArt #MangaArt #CuteOverload #Aesthetic #FantasyArt #DigitalArt #AIart #AI美女 #AI美少女 #AIGC #MoonlitDance #VisualEmotion #EphemeralBeauty"
    
    IMPORTANT: For all prompts, make sure they work well together to create a cohesive, emotionally resonant experience. The video prompt should produce a beautiful, appealing anime girl dancing that feels artistic and emotionally moving. The music should perfectly match the mood and movement of the dance. The social media text should be completely original and purely focused on artistic beauty, poetic expression, and emotional resonance - never mentioning games, gaming, or gameplay in any way.
    """
    
    # Combine all parts of the prompt
    prompt = base_prompt + visual_style_prompt + remaining_prompt
    
    # Call the OpenAI API with higher temperature for more creativity
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a highly talented anime director, music composer, and poetic writer specializing in creating beautiful, emotionally resonant artistic content. You excel at creating visually stunning anime scenes, perfectly matched musical compositions, and elegant poetic expressions. Your social media posts embody pure artistic beauty because you masterfully craft enchanting poetic mini-stories that capture delicate emotions and visual beauty. You understand the art of creating content that moves people emotionally through refined aesthetics and elegant expression. Your writing evokes a sense of wonder, beauty, and emotional depth that resonates with those who appreciate artistic excellence."},
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
                         video_file: str = "video_prompt.txt", 
                         music_file: str = "music_prompt.txt", 
                         social_file: str = "social_media_prompt.txt") -> None:
    """
    Saves the generated prompts to text files.
    
    Args:
        video_prompt: The generated video prompt
        music_prompt: The generated music prompt
        social_media_prompt: The generated social media prompt
        video_file: Filename for the video prompt
        music_file: Filename for the music prompt
        social_file: Filename for the social media prompt
    """
    with open(video_file, 'w') as f:
        f.write(video_prompt)
    
    with open(music_file, 'w') as f:
        f.write(music_prompt)
    
    with open(social_file, 'w') as f:
        f.write(social_media_prompt)
    
    print(f"Prompts saved to {video_file}, {music_file}, and {social_file}")

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