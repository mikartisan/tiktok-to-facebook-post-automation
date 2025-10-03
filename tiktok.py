import json
import subprocess
from pathlib import Path
import os
import requests
import sys

USERNAME = "twice_tiktok_official"
SAVE_DIR = Path("downloads")
SAVE_DIR.mkdir(exist_ok=True)

LAST_ID_FILE = SAVE_DIR / "last_video_id.txt"

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

def get_latest_video(username: str):
    """Fetch metadata of the latest TikTok video."""
    url = f"https://www.tiktok.com/@{username}"
    cmd = ["python", "-m", "yt_dlp", "-J", "--flat-playlist", url]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        if "entries" not in data or not data["entries"]:
            print("⚠️ No videos found.")
            return None

        latest = data["entries"][0]  # newest video
        return {
            "id": latest.get("id"),
            "url": latest.get("url"),
            "caption": latest.get("title") or "No caption"
        }

    except subprocess.CalledProcessError as e:
        print("❌ yt-dlp error:", e.stderr)
        return None

def download_video(url: str, video_id: str):
    """Download TikTok video to disk."""
    video_path = SAVE_DIR / f"{video_id}.mp4"
    cmd = ["python", "-m", "yt_dlp", "-o", str(video_path), url]

    try:
        subprocess.run(cmd, check=True)
        print(f"🎉 Download complete: {video_path}")
        return video_path
    except subprocess.CalledProcessError as e:
        print("❌ Download failed:", e.stderr)
        return None

def post_to_facebook(video_path: Path, caption: str):
    """Upload video to Facebook Page via Graph API."""
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/videos"
    files = {"source": open(video_path, "rb")}
    data = {"description": caption, "access_token": PAGE_ACCESS_TOKEN}

    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        print("✅ Uploaded to Facebook:", response.json())
        return True
    else:
        print("❌ Upload failed:", response.text)
        return False

if __name__ == "__main__":
    latest = get_latest_video(USERNAME)
    if not latest:
        sys.exit(0)

    # Ensure last_video_id.txt exists (first run safety)
    if not LAST_ID_FILE.exists():
        LAST_ID_FILE.write_text("")

    # Load last uploaded video ID
    last_id = LAST_ID_FILE.read_text().strip()

    if latest["id"] == last_id:
        print(f"⏩ Skipping: Latest video ({latest['id']}) already uploaded.")
        sys.exit(0)

    print("🔗 Latest video URL:", latest['url'])
    print("📝 Caption:", latest['caption'])

    video_path = download_video(latest["url"], latest["id"])
    if video_path:
        # Prepend custom caption
        fb_caption = f"Twice Tiktok Update\n\n{latest['caption']}"
        if post_to_facebook(video_path, fb_caption):
            # Save latest ID only after successful upload
            LAST_ID_FILE.write_text(latest["id"])
            video_path.unlink()  # cleanup
            print("🧹 Cleaned up local file.")
