import os
import shutil
import subprocess

VIDEO_FORMATS = {
    "1": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    "2": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "3": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
}

MP3_QUALITY = {
    "1": "64K",    # ~290 MB for 11 hours, fine for speech
    "2": "128K",   # ~630 MB for 11 hours
    "3": "192K",   # ~950 MB for 11 hours
}


def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print("❌ ffmpeg not found. It is required for MP3 conversion and merging video+audio.")
        print("   Install it and make sure it is in your PATH, then try again.")
        return False
    return True


def download_video(url, choice, download_path="downloads", mp3_quality="128K"):
    os.makedirs(download_path, exist_ok=True)

    if not check_ffmpeg():
        return

    cmd = [
        "yt-dlp",
        "--no-playlist",
        "--continue",          # resume if interrupted (important for huge files)
        "--retries", "10",
        "--fragment-retries", "10",
        "-o", f"{download_path}/%(title)s.%(ext)s",
    ]

    if choice in VIDEO_FORMATS:
        cmd += ["-f", VIDEO_FORMATS[choice]]
    elif choice in ("4", "5"):
        cmd += [
            "-f", "bestaudio/best",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", mp3_quality,
        ]
        if choice == "5":
            # Split into one MP3 per chapter (if the video has chapters)
            cmd += ["--split-chapters",
                    "-o", f"chapter:{download_path}/%(title)s - %(section_number)02d %(section_title)s.%(ext)s"]
    else:
        print("❌ Invalid choice.")
        return

    cmd.append(url)

    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Download Completed!")
    except FileNotFoundError:
        print("❌ yt-dlp not found. Install it with: pip install -U yt-dlp")
    except subprocess.CalledProcessError:
        print("\n❌ Download failed. Re-run the same command to resume.")


def main():
    print("🎥 YouTube Video Downloader 🎥")
    url = input("Enter YouTube video URL: ").strip()

    print("\nChoose Format:")
    print("1. Video 360p")
    print("2. Video 720p")
    print("3. Video 1080p")
    print("4. Audio Only (MP3)")
    print("5. Audio Only (MP3, split by chapters)")

    choice = input("Enter your choice (1-5): ").strip()

    quality = "128K"
    if choice in ("4", "5"):
        print("\nMP3 Quality:")
        print("1. 64 kbps  (smallest, good for talks/podcasts)")
        print("2. 128 kbps (balanced)")
        print("3. 192 kbps (best)")
        q = input("Enter your choice (1-3) [2]: ").strip() or "2"
        quality = MP3_QUALITY.get(q, "128K")

    download_video(url, choice, mp3_quality=quality)


if __name__ == "__main__":
    main()
