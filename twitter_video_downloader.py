import os
import sys
import argparse
import subprocess
from typing import List, Optional
import tempfile

def download_twitter_video(url: str, output_dir: str) -> Optional[str]:
    """
    Download a video from Twitter using yt-dlp
    
    Args:
        url: Twitter URL
        output_dir: Directory to save the video
        
    Returns:
        Path to the downloaded video file or None if download failed
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a temporary filename in the output directory
    filename = os.path.join(output_dir, f"twitter_video_{hash(url) % 10000:04d}.mp4")
    
    # Find the yt-dlp executable
    yt_dlp_path = "yt-dlp"
    
    # Try to find yt-dlp in user's scripts directory
    user_scripts_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Python", "Python312", "Scripts", "yt-dlp.exe")
    if os.path.exists(user_scripts_path):
        yt_dlp_path = user_scripts_path
        print(f"Using yt-dlp from: {yt_dlp_path}")
    
    try:
        # Use yt-dlp to download the video
        print(f"Downloading video from {url}...")
        result = subprocess.run(
            [
                yt_dlp_path, 
                "--no-playlist",
                "--no-warnings",
                "-f", "best[ext=mp4]",
                "-o", filename,
                url
            ],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Check if file was downloaded
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            print(f"Successfully downloaded: {filename}")
            return filename
        else:
            print(f"Failed to download video from {url}: File not created or empty")
            return None
            
    except FileNotFoundError:
        print(f"Error: yt-dlp not found. Please install it with: pip install -U yt-dlp")
        print(f"Then add it to your PATH or specify its location in the script.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Failed to download video from {url}: {e}")
        print(f"Error output: {e.stderr}")
        return None
    except Exception as e:
        print(f"An error occurred while downloading from {url}: {e}")
        return None

def download_videos_from_list(url_list: List[str], output_dir: str) -> List[str]:
    """
    Download videos from a list of Twitter URLs
    
    Args:
        url_list: List of Twitter URLs
        output_dir: Directory to save the videos
        
    Returns:
        List of paths to downloaded video files
    """
    downloaded_files = []
    
    for url in url_list:
        url = url.strip()
        if not url:
            continue
            
        file_path = download_twitter_video(url, output_dir)
        if file_path:
            downloaded_files.append(file_path)
    
    return downloaded_files

def create_concat_file(video_files: List[str], concat_file: str) -> bool:
    """
    Create a concat file for ffmpeg
    
    Args:
        video_files: List of video file paths
        concat_file: Path to the concat file to create
        
    Returns:
        True if file was created successfully, False otherwise
    """
    try:
        with open(concat_file, 'w') as f:
            for video_file in video_files:
                # Use escaped absolute paths for compatibility
                abs_path = os.path.abspath(video_file).replace('\\', '\\\\')
                f.write(f"file '{abs_path}'\n")
        return True
    except Exception as e:
        print(f"Error creating concat file: {e}")
        return False

def concatenate_videos(video_files: List[str], output_file: str) -> bool:
    """
    Concatenate videos using ffmpeg
    
    Args:
        video_files: List of video file paths
        output_file: Path to the output concatenated video
        
    Returns:
        True if concatenation was successful, False otherwise
    """
    if not video_files:
        print("No videos to concatenate")
        return False
        
    # Create a temporary concat file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        concat_file = tmp.name
        
    # Write the file paths to the concat file
    if not create_concat_file(video_files, concat_file):
        return False
        
    try:
        # Use ffmpeg to concatenate the videos
        print(f"Concatenating {len(video_files)} videos...")
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",  # Copy streams without re-encoding
            output_file
        ]
        
        subprocess.run(cmd, check=True)
        
        print(f"Successfully created concatenated video: {output_file}")
        # Clean up the temporary concat file
        os.unlink(concat_file)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error concatenating videos: {e}")
        return False
    except Exception as e:
        print(f"An error occurred during video concatenation: {e}")
        return False
    finally:
        # Make sure we clean up the concat file
        if os.path.exists(concat_file):
            os.unlink(concat_file)

def read_urls_from_file(file_path: str) -> List[str]:
    """
    Read Twitter URLs from a file
    
    Args:
        file_path: Path to file containing URLs (one per line)
        
    Returns:
        List of URLs
    """
    urls = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                url = line.strip()
                if url and not url.startswith('#'):
                    urls.append(url)
        return urls
    except Exception as e:
        print(f"Error reading URLs from file: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Download Twitter videos and concatenate them")
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--url", help="Single Twitter URL to download")
    input_group.add_argument("--url-file", help="File containing Twitter URLs (one per line)")
    input_group.add_argument("--urls", nargs="+", help="Multiple Twitter URLs")
    
    # Output options
    parser.add_argument("--output-dir", default="twitter_videos", 
                        help="Directory to save downloaded videos (default: twitter_videos)")
    parser.add_argument("--output-file", default="concatenated_video.mp4",
                        help="Output concatenated video file (default: concatenated_video.mp4)")
    parser.add_argument("--no-concat", action="store_true",
                        help="Don't concatenate videos, just download them")
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Get list of URLs
    urls = []
    if args.url:
        urls = [args.url]
    elif args.url_file:
        urls = read_urls_from_file(args.url_file)
    elif args.urls:
        urls = args.urls
    
    if not urls:
        print("No URLs to process. Exiting.")
        return 1
        
    print(f"Processing {len(urls)} Twitter URLs...")
    
    # Download videos
    downloaded_files = download_videos_from_list(urls, args.output_dir)
    
    if not downloaded_files:
        print("No videos were downloaded. Exiting.")
        return 1
        
    print(f"Successfully downloaded {len(downloaded_files)} videos.")
    
    # Concatenate videos if requested
    if not args.no_concat:
        output_path = os.path.join(args.output_dir, args.output_file)
        if concatenate_videos(downloaded_files, output_path):
            print(f"Videos have been concatenated to: {output_path}")
            return 0
        else:
            print("Failed to concatenate videos.")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 