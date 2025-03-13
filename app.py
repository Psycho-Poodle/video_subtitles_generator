import os
import tempfile
import gradio as gr
import moviepy.editor as mp
import subprocess
import assemblyai as aai
import yt_dlp
import shutil
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AssemblyAI API settings
API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not API_KEY:
    raise ValueError("API key for AssemblyAI is not set. Please check your .env file.")
aai.settings.api_key = API_KEY

# Step 1: Download YouTube video if URL is provided
def download_youtube(youtube_url, output_path):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': output_path,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    return output_path

# Step 2: Extract audio from video
def extract_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    return audio_path

# Step 3: Transcribe the audio with AssemblyAI
def transcribe_audio(audio_path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    
    if transcript.status == aai.TranscriptStatus.error:
        return None, f"Transcription Error: {transcript.error}"
    
    subtitle_path = os.path.join(tempfile.gettempdir(), "subtitle.srt")
    with open(subtitle_path, 'w', encoding='utf-8') as f:
        f.write(transcript.export_subtitles_srt())
    
    return subtitle_path, "Transcription completed successfully"

# Step 4: Add subtitles to video with improved path handling
def add_subtitles(video_path, subtitle_path, output_path):
    # Create a temporary copy of the subtitle file in the same directory as the output
    output_dir = os.path.dirname(output_path)
    temp_subtitle = os.path.join(output_dir, "temp_subtitle.srt")
    
    # Copy subtitle file to output directory
    shutil.copy(subtitle_path, temp_subtitle)
    
    # Use the file name only for the subtitles filter
    subtitle_filename = os.path.basename(temp_subtitle)
    
    # Escape any special characters in paths
    subtitle_filename = subtitle_filename.replace("'", "'\\''")
    
    # Build the FFmpeg command with proper path handling
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles={subtitle_filename}:force_style='Fontname=Arial,Fontsize=30,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=3,Outline=1'",
        "-c:a", "copy",
        "-y",  # Override output file if it exists
        output_path
    ]
    
    # Change working directory to where the subtitle file is
    current_dir = os.getcwd()
    os.chdir(output_dir)
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            return output_path, "Subtitles added successfully!"
        else:
            return None, f"Error adding subtitles: {result.stderr}"
    finally:
        # Change back to original directory and clean up
        os.chdir(current_dir)
        try:
            os.remove(temp_subtitle)
        except:
            pass

# Main processing function for Gradio with progress tracking
def process_video(video_input, youtube_url, progress=gr.Progress()):
    # Create temp directory for processing
    temp_dir = tempfile.mkdtemp()
    
    # Start progress tracking (0-100%)
    progress(0, desc="Starting process...")
    
    # Input handling
    if youtube_url:
        input_video = os.path.join(temp_dir, "youtube_video.mp4")
        status_msg = f"Downloading YouTube video: {youtube_url}"
        progress(5, desc="Downloading YouTube video...")
        yield None, status_msg
        try:
            download_youtube(youtube_url, input_video)
        except Exception as e:
            yield None, f"Error downloading YouTube video: {str(e)}"
            return
    else:
        input_video = video_input
        if not input_video:
            yield None, "Please provide either a video file or a YouTube URL"
            return
    
    # Extract audio
    audio_path = os.path.join(temp_dir, "extracted_audio.mp3")
    status_msg = "Extracting audio from video..."
    progress(20, desc="Extracting audio...")
    yield None, status_msg
    try:
        extract_audio(input_video, audio_path)
    except Exception as e:
        yield None, f"Error extracting audio: {str(e)}"
        return
    
    # Transcribe audio
    status_msg = "Transcribing audio..."
    progress(40, desc="Transcribing audio...")
    yield None, status_msg
    try:
        subtitle_path, msg = transcribe_audio(audio_path)
        if not subtitle_path:
            yield None, msg
            return
    except Exception as e:
        yield None, f"Error during transcription: {str(e)}"
        return
    
    # Add subtitles to video
    output_path = os.path.join(temp_dir, "output_with_subtitles.mp4")
    status_msg = "Adding subtitles to video..."
    progress(70, desc="Adding subtitles...")
    yield None, status_msg
    try:
        result_path, msg = add_subtitles(input_video, subtitle_path, output_path)
        if not result_path:
            yield None, msg
            return
        
        progress(95, desc="Finalizing...")
        time.sleep(1)  # Small delay to ensure UI updates
        progress(100, desc="Complete!")
        yield result_path, "Process completed successfully! Your video with subtitles is ready."
    except Exception as e:
        yield None, f"Error adding subtitles: {str(e)}"

# Create Gradio Interface
with gr.Blocks(title="Video Subtitle Generator") as app:
    gr.Markdown(
        """
        # 🎬 Video Subtitle Generator
        
        Upload a video file or provide a YouTube URL to generate subtitles.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            video_input = gr.Video(label="Upload Video")
            youtube_url = gr.Textbox(label="Or Enter YouTube URL")
            submit_btn = gr.Button("Generate Subtitles", variant="primary")
            
        with gr.Column(scale=1):
            output_video = gr.Video(label="Video with Subtitles")
            status = gr.Textbox(label="Status", value="Ready to process")
    
    submit_btn.click(
        fn=process_video,
        inputs=[video_input, youtube_url],
        outputs=[output_video, status],
        show_progress=True
    )

# Launch app
if __name__ == "__main__":
    app.launch(debug=True)