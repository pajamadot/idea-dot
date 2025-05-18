# AI Game Idea Generator

A complete workflow for creating and sharing AI-generated game concepts with viral social media content. This system generates unique game ideas, creates visual assets, produces music, and automatically composes viral social media posts.

## Features

- **Two-Stage Video Generation**: 
  - Creates high-quality images using FLUX-Pro Ultra API
  - Animates those images into videos using Wan-2.1 Image-to-Video API
- **Music Generation**: Produces unique game soundtracks using CassetteAI
- **Viral Social Media Content**: Generates attention-grabbing tweets with strategic hashtags
- **Wide Visual Style Variety**: Supports 100+ visual styles across 12 categories
- **Experimental Aesthetics**: Creates unique, boundary-pushing visual concepts
- **Automated Workflow**: Handles the entire content creation pipeline

## System Requirements

- Python 3.6+
- FFmpeg (installed and available in your PATH)
- API Keys:
  - OpenAI API key (for prompt generation and tweet creation)
  - FAL.ai API key (for image, video, and music generation)
- Twitter API credentials (optional, for automatic posting)

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/ai-game-content-generator.git
cd ai-game-content-generator
```

2. **Install required Python packages**:
```bash
# Using pip with requirements.txt (recommended)
pip install -r requirements.txt

# Or manually install each package
pip install openai requests fal-client python-dotenv tweepy asyncio
```

3. **Install FFmpeg**:
   - **Windows**: 
     - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
     - Add the bin directory to your system PATH
     - Verify installation with `ffmpeg -version`
   - **macOS**: 
     ```bash
     brew install ffmpeg
     ```
   - **Linux**: 
     ```bash
     sudo apt install ffmpeg
     ```

4. **Environment Setup**:

   a. Create a `.env.local` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   FAL_KEY=your_fal_api_key_here

   # Optional Twitter API credentials (for posting)
   TWITTER_BEARER_TOKEN=your_twitter_bearer_token
   TWITTER_CONSUMER_KEY=your_twitter_consumer_key
   TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
   TWITTER_ACCESS_TOKEN=your_twitter_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
   ```

   b. Obtain API keys from:
   - OpenAI API: [https://platform.openai.com/](https://platform.openai.com/)
   - FAL.ai API: [https://fal.ai/dashboard](https://fal.ai/dashboard)
   - Twitter API (optional): [https://developer.twitter.com/](https://developer.twitter.com/)

5. **Verify installation**:
```bash
# Test if the environment is correctly set up
python -c "from services.utils import load_env_vars; load_env_vars(); print('Environment loaded successfully')"
```

## Project Structure

```
.
├── create_game_content.py    # Main workflow orchestrator
├── prompt_generate.py        # Generates creative prompts
├── video_generation.py       # Handles two-stage video generation
├── music_generation.py       # Generates music
├── merge_audio_video.py      # Combines video and audio
├── generate_and_merge.py     # Alternative workflow script
├── daily_scheduler.py        # Runs content creation on a schedule
├── start_scheduler.bat       # Windows batch file to start scheduler
├── services/                 # Utility services
│   ├── tweet.py              # Twitter posting functionality
│   ├── twitter_auth.py       # Twitter authentication
│   └── utils.py              # Utility functions
├── input/                    # Generated media inputs
├── output/                   # Final media outputs
├── prompts/                  # Generated text prompts
└── requirements.txt          # Python dependencies
```

## Usage

### Main Workflow - Complete Content Creation

The easiest way to generate complete game content is to run:

```bash
python create_game_content.py
```

This will:
1. Generate creative game concept prompts
2. Generate a high-quality game image using FLUX-Pro Ultra
3. Animate that image into a video using Wan-2.1
4. Generate matching game music
5. Merge the video and audio
6. Create a viral tweet for sharing
7. Optionally post to Twitter

### Advanced Usage - Component by Component

#### 1. Generate Prompts Only

```bash
python prompt_generate.py
```

This generates creative game concept prompts and saves them to files.

#### 2. Generate Image and Video Only

```bash
python video_generation.py --prompt "Your gameplay concept prompt"
# or
python video_generation.py --prompt-file prompts/video_prompt.txt
```

#### 3. Generate Music Only

```bash
python music_generation.py --prompt "Your music concept prompt"
# or
python music_generation.py --prompt-file prompts/music_prompt.txt
```

#### 4. Merge Audio and Video Only

```bash
python merge_audio_video.py --video-file input/game_video.mp4 --audio-file input/game_music.wav --output-file output/final_game_content.mp4
```

#### 5. Alternative Workflow

```bash
python generate_and_merge.py
```

This runs an alternative workflow with more command-line options.

## Visual Style Categories

The system supports 100+ visual styles across 12 categories:

1. **Traditional Art Styles**: watercolor, oil painting, charcoal sketch, ukiyo-e, etc.
2. **Modern Art Movements**: cubist, surrealist, impressionist, art deco, etc.
3. **Digital & Contemporary**: vaporwave, glitch art, low poly, pixel art, etc.
4. **Film & Photography**: film noir, technicolor, infrared photography, etc.
5. **Animation Styles**: hand-drawn, stop motion, claymation, anime, etc.
6. **Video Game Aesthetics**: 16-bit SNES, PS1, GameBoy 4-color, etc.
7. **Experimental/Abstract**: neural network imagery, fractals, ASCII art, etc.
8. **International Styles**: Russian constructivism, Chinese ink painting, etc.
9. **Historical Periods**: Byzantine, Renaissance, 1980s, Y2K aesthetic, etc.
10. **Mixed Media**: collage, photomontage, textile art, etc.
11. **Textures & Materials**: chalk, blueprint, risograph, woodcut, etc.
12. **Lighting Techniques**: chiaroscuro, noir lighting, volumetric lighting, etc.

## Technical Details

### Image Generation (FLUX-Pro Ultra)

The system uses FAL.ai's FLUX-Pro Ultra API to generate high-quality images with these parameters:
- Resolution: 1080p
- Aspect ratio: 16:9
- Safety features: Enabled
- Format: JPEG

### Video Generation (Wan-2.1)

The system animates images into videos using FAL.ai's Wan-2.1 Image-to-Video API:
- Frame rate: 16 FPS
- Number of frames: 81 (5 seconds)
- Resolution: 720p
- Inference steps: 30
- Guide scale: 5
- Shift: 5

### Music Generation

Uses CassetteAI through FAL.ai to generate 10-second audio clips that match the visual style.

### Tweet Generation

Creates viral, controversial tweets with:
- Strong attention-grabbing hooks
- Emotional engagement elements
- Clear calls-to-action
- 20+ strategic hashtags across multiple categories

## Scheduled Content Creation (Optional)

For automated content creation, use the scheduler:

```bash
# Windows
start_scheduler.bat

# Linux/Mac
python daily_scheduler.py
```

This runs the content creation process on a daily schedule.

## Troubleshooting

### Common Issues

1. **API Key Errors**: Make sure your `.env.local` file contains valid API keys.
2. **FFmpeg Missing**: Ensure FFmpeg is installed and in your system PATH.
3. **Directory Errors**: The system will create required directories automatically.
4. **Twitter Posting Errors**: Verify your Twitter API credentials if using auto-posting.

### Log Files

The system creates log files in the project directory:
- `error.log`: Contains error messages
- `output.log`: Contains standard output

## Credits

This project uses the following APIs:
- [OpenAI API](https://openai.com/blog/openai-api) for prompt and tweet generation
- [FLUX-Pro Ultra on FAL.ai](https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra/api) for image generation
- [Wan-2.1 on FAL.ai](https://fal.ai/models/fal-ai/wan-i2v/api) for image-to-video conversion
- [CassetteAI on FAL.ai](https://fal.ai/models/cassetteai/music-generator/api) for music generation
- [Twitter API](https://developer.twitter.com/en/docs/twitter-api) for social media posting

## License

This project is licensed under the MIT License - see the LICENSE file for details.
