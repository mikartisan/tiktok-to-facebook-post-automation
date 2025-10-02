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
