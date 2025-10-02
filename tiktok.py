import json
import subprocess
import os
from pathlib import Path
import requests

# --- CONFIG ---
USERNAME = "twice_tiktok_official"
SAVE_DIR = Path("downloads")
SAVE_DIR.mkdir(exist_ok=True)

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")
LAST_ID_FILE = SAVE_DIR / "last_video_id.txt"


def get_latest_video(username: str):
    """Fetch latest TikTok video metadata"""
    url = f"https://www.tiktok.com/@{username}"
    cmd = ["python", "-m", "yt_dlp", "-J", "--flat-playlist", url]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        if "entries" not in data or not data["entries"]:
            print("⚠️ No videos found.")
            return None

        latest = data["entries"][0]
        return {
            "id": latest.get("id"),
            "url": latest.get("url"),
            "caption": latest.get("title") or "No caption"
        }

    except subprocess.CalledProcessError as e:
        print("❌ yt-dlp error:", e.stderr)
        return None


def download_video(url: str, video_id: str):
    """Download TikTok video"""
    video_path = SAVE_DIR / f"{video_id}.mp4"
    cmd = [
        "python", "-m", "yt_dlp",
        "-o", str(video_path),
        url
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"🎉 Download complete: {video_path}")
        return video_path
    except subprocess.CalledProcessError as e:
        print("❌ Download failed:", e.stderr)
        return None


def post_to_facebook(video_path: Path, caption: str):
    """Upload video to Facebook Page"""
    url = f"https://graph-video.facebook.com/v18.0/{PAGE_ID}/videos"
    params = {
        "access_token": PAGE_ACCESS_TOKEN,
        "description": caption
    }

    try:
        with open(video_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, data=params, files=files)

        if response.status_code == 200:
            print("✅ Uploaded to Facebook:", response.json())
            return True
        else:
            print("❌ Facebook upload error:", response.text)
            return False

    except Exception as e:
        print("❌ Exception uploading to Facebook:", e)
        return False


def get_last_uploaded_id():
    """Read last uploaded TikTok ID from file"""
    if LAST_ID_FILE.exists():
        return LAST_ID_FILE.read_text().strip()
    return None


def save_last_uploaded_id(video_id: str):
    """Save last uploaded TikTok ID to file"""
    LAST_ID_FILE.write_text(video_id)


if __name__ == "__main__":
    latest = get_latest_video(USERNAME)
    if not latest:
        exit()

    last_uploaded = get_last_uploaded_id()
    if latest["id"] == last_uploaded:
        print("⏩ Already uploaded this video. Skipping...")
        exit()

    # Download latest TikTok video
    video_path = download_video(latest["url"], latest["id"])
    if video_path:
        # Upload to Facebook
        success = post_to_facebook(video_path, latest["caption"])

        if success:
            # Save last uploaded ID
            save_last_uploaded_id(latest["id"])

            # Delete local video file
            video_path.unlink(missing_ok=True)
            print(f"🗑️ Deleted local file {video_path}")
