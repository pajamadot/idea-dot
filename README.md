# Game Idea Generator and Media Merger

A complete workflow for generating game ideas, creating media assets, and merging them into a single video output.

## Features

- Generate creative video and music prompts using OpenAI's API
- Automatically create input and output folders
- Generate music using the CassetteAI API (with both sync and async options)
- Find and merge MP4 video files and WAV audio files
- Ensure the output length is the minimum of the audio and video durations
- Preserve video quality by using stream copying when possible
- Fallback option when FFmpeg probe fails to get durations

## Requirements

- Python 3.6+
- FFmpeg (must be installed and available in your PATH)
- OpenAI API key (for prompt generation)
- FAL.ai API key (for music generation)
- Video generation tool (that accepts text prompts)

## Installation

1. Make sure FFmpeg is installed on your system. If not, you can download it from [ffmpeg.org](https://ffmpeg.org/download.html) or install it using your system's package manager.

2. After installing FFmpeg, ensure that the FFmpeg bin directory is added to your system PATH.

3. Install the required Python packages:

```bash
pip install openai requests fal-client
```

4. Set your API keys as environment variables:

```bash
# On Windows
set OPENAI_API_KEY=your_openai_api_key_here
set FAL_KEY=your_fal_api_key_here

# On macOS/Linux
export OPENAI_API_KEY=your_openai_api_key_here
export FAL_KEY=your_fal_api_key_here
```

## Complete Workflow

The project consists of four main scripts:

1. `prompt_generate.py` - Generates creative prompts for video and audio
2. `music_generation.py` - Generates music using the CassetteAI API
3. `merge_audio_video.py` - Merges video and audio files
4. `generate_and_merge.py` - Orchestrates the entire workflow

### Step 1: Generate Prompts

Run the complete workflow:

```bash
python generate_and_merge.py
```

This will:
1. Generate a video prompt and a music prompt using OpenAI API
2. Save the prompts to the `prompts` directory
3. Guide you through the next steps

### Step 2: Create Media Assets

After generating prompts, you have two options:

#### Option A: Automatic Music Generation

Run the workflow with the `--generate-music` flag:

```bash
python generate_and_merge.py --generate-music
```

For better performance, you can use the async API version:

```bash
python generate_and_merge.py --generate-music --async
```

This will:
1. Generate prompts (or use existing ones if using `--skip-prompt-generation`)
2. Automatically generate music using the CassetteAI API
3. You'll only need to manually generate the video

#### Option B: Manual Creation

1. Use the video prompt with your preferred video generation tool to create an MP4 file
2. Use the music prompt with your preferred audio generation tool to create a WAV file
3. Place both files in the `input` directory

### Step 3: Merge Media Files

The script will automatically:
1. Find the first MP4 video file and first WAV audio file in the input folder
2. Merge them and save the result as `merged_media.mp4` in the output folder

### Using a Custom FFmpeg Path

If FFmpeg is not in your system PATH, you can specify the path:

```bash
python generate_and_merge.py --ffmpeg-path C:\path\to\ffmpeg.exe
```

### Skipping Prompt Generation

If you already have prompts and want to skip the generation step:

```bash
python generate_and_merge.py --skip-prompt-generation
```

### Setting Music Duration

You can specify the duration of generated music in seconds:

```bash
python generate_and_merge.py --generate-music --music-duration 10
```

## Individual Script Usage

### Prompt Generation

```bash
python prompt_generate.py
```

### Music Generation

You can run the music generation script directly with various options:

```bash
# Generate music with synchronous API (default)
python music_generation.py

# Generate music with asynchronous API
python music_generation.py --async

# Use a specific prompt
python music_generation.py --prompt "Your music prompt here"

# Use a prompt from a file
python music_generation.py --prompt-file path/to/prompt.txt

# Specify duration and output folder
python music_generation.py --duration 10 --output-folder custom_folder
```

This will:
1. Generate music using the specified prompt or a default test prompt
2. Save the generated audio file to the specified output folder

### Media Merging

```bash
python merge_audio_video.py
```

Optional arguments:
- `-i, --input`: Input folder path (default: `./input`)
- `-o, --output`: Output folder path (default: `./output`)
- `--output-filename`: Output filename (default: `merged_media.mp4`)
- `--ffmpeg-path`: Path to FFmpeg executable if not in PATH

## Supported File Types

- Video: MP4 files only
- Audio: WAV files only

## How the Merger Works

1. Creates input and output folders if they don't exist
2. Finds the first MP4 video file and first WAV audio file in the input folder
3. Gets the duration of both input files using `ffprobe`
4. Calculates the minimum duration between the audio and video
5. Merges the video and audio, limiting the output to the minimum duration
6. Saves the result to the output folder with the specified filename

If `ffprobe` fails to get the media durations, the script will fall back to using FFmpeg's `-shortest` option, which automatically uses the shortest input stream to determine the output length.

The video stream is copied without re-encoding for better performance, and the audio is encoded using the AAC codec for compatibility.

## Async vs Sync API

The music generation module supports both synchronous and asynchronous API calls:

- **Synchronous API** (default): Uses `fal_client.subscribe()` which blocks until the music generation is complete
- **Asynchronous API**: Uses `fal_client.submit_async()` and proper async/await patterns for better performance in async workflows

The async version is particularly useful for longer music generation tasks or when integrating with other async code.

## API Credits

This project uses the following APIs:
- [OpenAI API](https://openai.com/blog/openai-api) for prompt generation
- [CassetteAI Music Generator on FAL.ai](https://fal.ai/models/cassetteai/music-generator/api) for music generation
