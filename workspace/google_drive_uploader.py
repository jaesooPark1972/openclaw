"""
Google Drive Uploader for OpenClaw
Uses credentials from .kilocode/mcp.json or environment variables.
"""

import os
import json
import logging
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# Load credentials from mcp.json
MCP_JSON_PATH = Path("d:/OpenClaw/.kilocode/mcp.json")
TOKEN_JSON_PATH = Path("d:/OpenClaw/workspace/data/gdrive_token.json")

def get_drive_service():
    creds = None
    
    # 1. Try to load from explicit token file
    if TOKEN_JSON_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_JSON_PATH), ['https://www.googleapis.com/auth/drive.file'])
        except Exception as e:
            print(f"[GDrive] Token file invalid: {e}")

    # 2. If no valid creds, try to construct from mcp.json
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"[GDrive] Refresh failed: {e}")
        
        if not creds:
            # Load from mcp.json
            if MCP_JSON_PATH.exists():
                try:
                    with open(MCP_JSON_PATH, 'r') as f:
                        data = json.load(f)
                        gdrive_config = data.get("mcpServers", {}).get("google-drive", {}).get("env", {})
                        
                        client_id = gdrive_config.get("GOOGLE_CLIENT_ID")
                        client_secret = gdrive_config.get("GOOGLE_CLIENT_SECRET")
                        refresh_token = gdrive_config.get("GOOGLE_REFRESH_TOKEN")
                        
                        if client_id and client_secret and refresh_token:
                            creds = Credentials(
                                None, # No access token initially
                                refresh_token=refresh_token,
                                token_uri="https://oauth2.googleapis.com/token",
                                client_id=client_id,
                                client_secret=client_secret,
                                scopes=['https://www.googleapis.com/auth/drive.file']
                            )
                            # Force refresh to get access token
                            creds.refresh(Request())
                            
                            # Save for later
                            with open(TOKEN_JSON_PATH, 'w') as token_file:
                                token_file.write(creds.to_json())
                except Exception as e:
                    print(f"[GDrive] Config load failed: {e}")

    if not creds or not creds.valid:
        print("[GDrive] Authentication failed. Please check mcp.json.")
        return None

    return build('drive', 'v3', credentials=creds)

def upload_to_drive(file_path: str, folder_id: str = None) -> str:
    """Uploads a file to Google Drive. Returns the file ID."""
    service = get_drive_service()
    if not service:
        return None

    path = Path(file_path)
    if not path.exists():
        print(f"[GDrive] File not found: {file_path}")
        return None

    file_metadata = {'name': path.name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(str(path), resumable=True)

    try:
        print(f"[GDrive] Uploading {path.name}...")
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        print(f"[GDrive] Upload complete. ID: {file.get('id')}")
        return file.get('webViewLink')
    except Exception as e:
        print(f"[GDrive] Upload error: {e}")
        return None

if __name__ == "__main__":
    # Test upload if run directly
    import sys
    if len(sys.argv) > 1:
        upload_to_drive(sys.argv[1])
    else:
        print("Usage: python google_drive_uploader.py <file_path>")
