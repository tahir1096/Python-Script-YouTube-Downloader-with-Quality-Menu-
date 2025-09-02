import os

def download_video(url, choice, download_path="downloads"):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    formats = {
        "1": 'bestvideo[height<=360]+bestaudio/best[height<=360]',
        "2": 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        "3": 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        "4": 'bestaudio/best'
    }

    if choice not in formats:
        print("❌ Invalid choice.")
        return

    command = f'yt-dlp -o "{download_path}/%(title)s.%(ext)s" -f "{formats[choice]}" "{url}"'
    os.system(command)
    print("\n✅ Download Completed!")

def main():
    print("🎥 YouTube Video Downloader 🎥")
    url = input("Enter YouTube video URL: ")

    print("\nChoose Quality:")
    print("1. 360p")
    print("2. 720p")
    print("3. 1080p")
    print("4. Audio Only (MP3)")

    choice = input("Enter your choice (1-4): ")
    download_video(url, choice)

if __name__ == "__main__":
    main()
