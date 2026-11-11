# UNKNOWN FILES automation starter

This starter creates one narrated vertical MP4 each time GitHub Actions runs.

## Included
- A small built-in library of mystery/story scripts.
- Simple 1080×1920 story cards.
- English text-to-speech narration via gTTS.
- FFmpeg video rendering.
- GitHub Actions schedule: 07:00, 12:00 and 18:00 UTC (08:00, 13:00 and 19:00 in Nigeria).

## Install in your repository
Upload these files and folders to the repository root. Keep `.github/workflows/daily-video.yml` at that exact path.

## Run and download
Open **Actions** → **Generate UNKNOWN FILES video** → **Run workflow**. When it finishes, open the run and download the `unknown-files-video-...` artifact. It contains the MP4 and story text.

## Honest limitations
This first version uses a built-in story library, not an AI language model. It creates one video per scheduled run (three per day). gTTS requires internet access. It creates downloadable videos but does not publish them to Facebook. Facebook's Page publishing API requires an eligible Page and a Page access token; Professional Mode personal profiles are not the same as Pages.

Never put passwords, API tokens, or secrets in source files. For any later integration, use GitHub Actions Secrets. Public repositories expose their source code. GitHub scheduled runs may be delayed and are subject to GitHub's current usage limits.
