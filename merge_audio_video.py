import os
import subprocess
import argparse
import json
import sys
from pathlib import Path

def check_ffmpeg_installed():
    """Check if ffmpeg is installed and accessible"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=False)
        return True
    except FileNotFoundError:
        return False

def get_media_duration(file_path):
    """Get the duration of a media file using ffprobe"""
    if not os.path.exists(file_path):
        print(f"Error: File does not exist: {file_path}")
        return None
        
    try:
        cmd = [
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'json', 
            file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
    except FileNotFoundError:
        print("Error: ffprobe command not found. Please make sure FFmpeg is installed and in your PATH.")
        print("You can download FFmpeg from: https://ffmpeg.org/download.html")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe: {e}")
        print(f"Error output: {e.stderr}")
        return None
    except Exception as e:
        print(f"Unexpected error processing {file_path}: {e}")
        return None

def find_first_video_file(folder_path):
    """Find the first MP4 video file in the folder"""
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and file.lower().endswith('.mp4'):
            return file_path
    
    return None

def find_first_audio_file(folder_path):
    """Find the first WAV audio file in the folder"""
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and file.lower().endswith('.wav'):
            return file_path
    
    return None

def merge_audio_video(video_path, audio_path, output_path):
    """Merge audio and video files, with length equal to min(audio, video)"""
    if not os.path.exists(video_path):
        print(f"Error: Video file does not exist: {video_path}")
        return False
    
    if not os.path.exists(audio_path):
        print(f"Error: Audio file does not exist: {audio_path}")
        return False
    
    # Check if ffmpeg is installed
    if not check_ffmpeg_installed():
        print("Error: ffmpeg command not found. Please make sure FFmpeg is installed and in your PATH.")
        print("You can download FFmpeg from: https://ffmpeg.org/download.html")
        return False
        
    # Get durations
    video_duration = get_media_duration(video_path)
    audio_duration = get_media_duration(audio_path)
    
    if video_duration is None or audio_duration is None:
        print("Failed to get media durations. Attempting to merge without duration constraint.")
        # Proceed without duration constraint if ffprobe failed
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-shortest',  # Use shortest input as duration constraint
            '-y',  # Always overwrite output file
            output_path
        ]
    else:
        # Use the shorter duration
        target_duration = min(video_duration, audio_duration)
        print(f"Video duration: {video_duration:.2f}s")
        print(f"Audio duration: {audio_duration:.2f}s")
        print(f"Output duration will be: {target_duration:.2f}s")
        
        # Standard video + audio merge
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-t', str(target_duration),
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-y',  # Always overwrite output file
            output_path
        ]
    
    try:
        print("Running ffmpeg with command:")
        print(" ".join(cmd))
        subprocess.run(cmd, check=True)
        print(f"Successfully merged files to: {output_path}")
        return True
    except FileNotFoundError:
        print("Error: ffmpeg command not found. Please make sure FFmpeg is installed and in your PATH.")
        print("You can download FFmpeg from: https://ffmpeg.org/download.html")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error merging files: {e}")
        print(f"Error output: {e.stderr if hasattr(e, 'stderr') else 'No error output'}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Merge MP4 video and WAV audio files from input folder')
    parser.add_argument('-i', '--input', help='Input folder path (default: ./input)')
    parser.add_argument('-o', '--output', help='Output folder path (default: ./output)')
    parser.add_argument('--output-filename', help='Output filename (default: merged_media.mp4)')
    parser.add_argument('--ffmpeg-path', help='Path to FFmpeg executable if not in PATH')
    
    args = parser.parse_args()
    
    # Set custom FFmpeg path if provided
    if args.ffmpeg_path:
        if os.path.exists(args.ffmpeg_path):
            ffmpeg_dir = os.path.dirname(args.ffmpeg_path)
            os.environ["PATH"] += os.pathsep + ffmpeg_dir
            print(f"Added {ffmpeg_dir} to PATH")
        else:
            print(f"Warning: Provided FFmpeg path does not exist: {args.ffmpeg_path}")
    
    # Set default input/output folders if not provided
    input_folder = args.input if args.input else './input'
    output_folder = args.output if args.output else './output'
    output_filename = args.output_filename if args.output_filename else 'merged_media.mp4'
    
    # Create folders if they don't exist
    if not os.path.exists(input_folder):
        print(f"Creating input folder: {input_folder}")
        os.makedirs(input_folder)
    
    if not os.path.exists(output_folder):
        print(f"Creating output folder: {output_folder}")
        os.makedirs(output_folder)
    
    # Find first MP4 video and WAV audio files
    video_path = find_first_video_file(input_folder)
    audio_path = find_first_audio_file(input_folder)
    
    # Check if files were found
    if not video_path:
        print(f"No MP4 video file found in {input_folder}")
        return
    
    if not audio_path:
        print(f"No WAV audio file found in {input_folder}")
        return
    
    print(f"Found video: {video_path}")
    print(f"Found audio: {audio_path}")
    
    # Set output path
    output_path = os.path.join(output_folder, output_filename)
    
    # Merge the files
    success = merge_audio_video(video_path, audio_path, output_path)
    
    if not success:
        print("\nPlease ensure FFmpeg is installed correctly. You can download it from https://ffmpeg.org/download.html")
        print("After installing, make sure the FFmpeg bin directory is added to your system PATH.")
        print("Alternatively, you can specify the FFmpeg path using the --ffmpeg-path option:")
        print(f"python {sys.argv[0]} --ffmpeg-path=C:\\path\\to\\ffmpeg.exe")

if __name__ == "__main__":
    main() 