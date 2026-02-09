# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred Provider: OpenAI TTS (tts-1)
- Preferred voice: "Nova" (Clear, multilingual, handles Korean/English naturally)
- Default speaker: Telegram (jayhomebot)
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### 🎵 Vivace Control (Music & Tech)
Manage the Vivace Nexus system.

- **Use 'render_video' to convert the latest music into an MP4 video.**

- **Send Latest Music**: `python skills/vivace_control.py send_latest '{"chat_id": "7480526781"}'`
- **Generate Music**: `python skills/vivace_control.py generate_music '{"title": "My Song", "prompt": "Piano ballad"}'`
- **Render Video**: `python skills/vivace_control.py render_video '{"prompt": "default"}'`
- **Deploy Team**: `python skills/vivace_control.py deploy_team '{"task": "Make a website"}'`

