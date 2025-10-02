# TikTok → Facebook Auto Uploader

This project automates downloading the latest TikTok video from a given account and re-uploading it to a Facebook Page using the **Facebook Graph API**.  
It runs daily via **GitHub Actions** and ensures no duplicate posts are uploaded.

---

## 🚀 Features

-   Fetch the **latest TikTok video** using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).
-   Automatically **downloads** the video and caption.
-   Uploads to your **Facebook Page** using the Graph API.
-   Tracks the **last uploaded video ID** to prevent reposting the same video.
-   Cleans up downloaded videos after posting.
-   Fully automated with **GitHub Actions** (cron schedule or manual run).

---

## ⚙️ Setup

### 1. Clone this repo

```bash
git clone https://github.com/mikartisan/tiktok-to-facebook-post-automation.git
cd tiktok-to-facebook-post-automation
```

### 2. Add Facebook credentials

You need a **Page Access Token** with the `pages_manage_posts` and `pages_read_engagement` permissions.

In your repo, go to:

**Settings → Secrets and variables → Actions**

Add:

-   `PAGE_ACCESS_TOKEN`
-   `PAGE_ID`

---

### 3. Update TikTok username

In tiktok.py, change:
`USERNAME = "twice_tiktok_official"`

to your own TikTok username (without @).

## 🤖 GitHub Actions Workflow

The workflow is defined in .github/workflows/tiktok-to-fb.yml.

It:

1.  Runs every day at **6PM UTC** (configurable via cron).
2.  Restores the last uploaded TikTok video ID (last_video_id.txt).
3.  Runs the Python script:

    -   Skips if no new TikTok video.
    -   Downloads & uploads if a new one is found.

4.  Saves the updated last_video_id.txt as an artifact for the next run.

### Run manually

You can also trigger it manually from the **Actions** tab.

## 📝 Notes

-   last_video_id.txt is stored as a **GitHub Action artifact**, not in your repo.
-   Artifacts are visible in each workflow run summary and expire after **90 days** by default.
-   If you want permanent tracking inside your repo, you could commit the file instead of using artifacts.

## 🛠️ Tech Used

-   [yt-dlp](https://github.com/yt-dlp/yt-dlp) – TikTok scraping & downloads
-   Requests – Uploading to Facebook
-   GitHub Actions – Automation

## ⚠️ Disclaimer

This tool is for **personal use only**.Scraping/downloading from TikTok and reuploading to Facebook may violate their **Terms of Service**.
