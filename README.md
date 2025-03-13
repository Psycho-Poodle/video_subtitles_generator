# **Video Subtitle Generator**

![Demo](https://img.shields.io/badge/Demo-HuggingFace-blue)  
[![Open in Hugging Face](https://img.shields.io/badge/🤗-Open%20in%20HuggingFace-yellow)](https://huggingface.co/spaces/pyschopoodle/Vidoes-subtitles-generator)

This project is a **Video Subtitle Generator** that allows you to upload a video or provide a YouTube URL, and it will automatically generate subtitles for the video using AssemblyAI's transcription service. The project is built using Python, Gradio for the user interface, and FFmpeg for video processing.

---

## **Features**
- **Upload a video file** or **provide a YouTube URL** to generate subtitles.
- Automatically extracts audio from the video.
- Uses AssemblyAI for accurate audio transcription.
- Adds subtitles to the video with customizable styling.
- Supports both local execution and deployment on Hugging Face Spaces.

---
## **Demo Videos**

### Original Video
[Download Original Video](https://github.com/Psycho-Poodle/Video-Subtitle-Generator/raw/main/input_video.mp4)

### Output Video with Subtitles
[Download Output Video](https://github.com/Psycho-Poodle/Video-Subtitle-Generator/raw/main/output_video.mp4)




## **Demo**
You can try the project directly on Hugging Face:  
👉 [Hugging Face Demo](https://huggingface.co/spaces/pyschopoodle/Vidoes-subtitles-generator)

**Note**: The Hugging Face deployment currently has issues with YouTube links due to cookie restrictions. To use YouTube links, clone the repository and run the project locally.


---

## **Prerequisites**
- Python 3.8 or higher
- FFmpeg installed on your system
- Docker (optional, for containerized deployment)

---

## **Setup and Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/Video-Subtitle-Generator.git
cd Video-Subtitle-Generator
```

### **2. Install Dependencies**
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### **3. Set Up AssemblyAI API Key**
- Sign up for an API key at [AssemblyAI](https://www.assemblyai.com/).
- Create a `.env` file in the project root and add your API key:
  ```plaintext
  ASSEMBLYAI_API_KEY=your_api_key_here
  ```

### **4. Install FFmpeg**
- On Ubuntu:
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```
- On macOS (using Homebrew):
  ```bash
  brew install ffmpeg
  ```
- On Windows: Download from [FFmpeg's official website](https://ffmpeg.org/download.html).

---

## **Running the Project Locally**

### **1. Run the Application**
```bash
python app.py
```

### **2. Access the Gradio UI**
Open your browser and navigate to:  
👉 [http://127.0.0.1:7860](http://127.0.0.1:7860)

### **3. Use the Application**
- Upload a video file or provide a YouTube URL.
- Click **Generate Subtitles**.
- Wait for the process to complete. The final video with subtitles will be displayed.

---

## **Docker Deployment**

### **1. Build the Docker Image**
```bash
docker build -t video-subtitle-generator .
```

### **2. Run the Docker Container**
```bash
docker run -p 7860:7860 video-subtitle-generator
```

### **3. Access the Application**
Open your browser and navigate to:  
👉 [http://127.0.0.1:7860](http://127.0.0.1:7860)

---

## **Hugging Face Deployment**
The project is deployed on Hugging Face Spaces. However, due to cookie restrictions, YouTube links may not work in the Hugging Face environment. To use YouTube links, clone the repository and run the project locally.

---

## **How It Works**
1. **Input Handling**: Accepts a video file or YouTube URL.
2. **Audio Extraction**: Extracts audio from the video using `moviepy`.
3. **Transcription**: Transcribes the audio using AssemblyAI's API.
4. **Subtitle Addition**: Adds subtitles to the video using FFmpeg.
5. **Output**: Returns the video with embedded subtitles.

---

## **Customization**
You can customize the subtitle style by modifying the `add_subtitles` function in `app.py`. For example:
```python
force_style='Fontname=Arial,Fontsize=30,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=3,Outline=1'
```

---

## **Troubleshooting**
- **YouTube Links Not Working on Hugging Face**: This is due to cookie restrictions. Run the project locally to use YouTube links.
- **FFmpeg Errors**: Ensure FFmpeg is installed and accessible in your system's PATH.
- **AssemblyAI API Errors**: Verify that your API key is correctly set in the `.env` file.

---

## **Contributing**
Contributions are welcome! If you find any issues or have suggestions, feel free to open an issue or submit a pull request.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**
- [AssemblyAI](https://www.assemblyai.com/) for the transcription API.
- [Gradio](https://gradio.app/) for the user interface.
- [FFmpeg](https://ffmpeg.org/) for video processing.

---

Enjoy generating subtitles for your videos! 🎬