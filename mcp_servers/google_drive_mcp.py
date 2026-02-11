
import os
import io
import sys
import logging
import glob
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find_env_file():
    """Find .env file in common locations"""
    possible_paths = [
        r"D:/OpenClaw/.env",
        r"d:/OpenClaw/.env",
        ".env",
        "../.env",
        "../../.env"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"Found .env at: {path}")
            return path
    logger.warning("No .env file found")
    return None

def get_drive_service():
    """Initialize Google Drive API service with error handling"""
    try:
        # Find and load env file
        env_path = find_env_file()
        if env_path and os.path.exists(env_path):
            load_dotenv(env_path)
            logger.info(f"Loaded env from: {env_path}")
        else:
            # Try loading from current directory
            load_dotenv()
            logger.info("Attempted load_dotenv() without path")
        
        # Debug: log available env vars (masked)
        refresh_token = os.getenv("GOOGLE_DRIVE_REFRESH_TOKEN") or os.getenv("GOOGLE_DRIVE_TOKEN")
        client_id = os.getenv("GOOGLE_CLIENT_ID") or os.getenv("GOOGLE_DRIVE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET") or os.getenv("GOOGLE_DRIVE_CLIENT_SECRET")
        
        logger.info(f"Refresh token present: {bool(refresh_token)}")
        logger.info(f"Client ID present: {bool(client_id)}")
        logger.info(f"Client secret present: {bool(client_secret)}")
        
        if not all([refresh_token, client_id, client_secret]):
            missing = []
            if not refresh_token: missing.append("GOOGLE_DRIVE_REFRESH_TOKEN")
            if not client_id: missing.append("GOOGLE_CLIENT_ID")
            if not client_secret: missing.append("GOOGLE_CLIENT_SECRET")
            logger.error(f"Missing credentials: {missing}")
            return None

        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret
        )
        
        service = build('drive', 'v3', credentials=creds)
        logger.info("Google Drive service initialized successfully")
        return service
        
    except Exception as e:
        logger.error(f"Failed to initialize Drive service: {e}", exc_info=True)
        return None

# Initialize FastMCP Server
mcp = FastMCP("Google-Drive-Py")

@mcp.tool()
async def gdrive_list_files(query: str = None, page_size: int = 10, folder_id: str = None) -> str:
    """Lists files in Google Drive matching the query. Query follows Google Drive API syntax."""
    service = get_drive_service()
    if not service:
        return "❌ Error: Google Drive service not initialized. Check credentials."

    try:
        q_parts = []
        if folder_id:
            q_parts.append(f"'{folder_id}' in parents")
        if query:
            # Simple name search convenience
            if "name contains" not in query and "=" not in query:
                q_parts.append(f"name contains '{query}'")
            else:
                q_parts.append(query)
        
        q = " and ".join(q_parts) if q_parts else None
        
        results = service.files().list(
            q=q, pageSize=page_size, fields="files(id, name, mimeType, parents)"
        ).execute()
        items = results.get('files', [])

        if not items:
            return "📂 No files found."
        
        output = ["📂 Google Drive Search Results:"]
        for item in items:
            output.append(f"- {item['name']} (ID: {item['id']}, Type: {item['mimeType']})")
        
        return "\n".join(output)
    except Exception as e:
        return f"❌ Error listing files: {str(e)}"

@mcp.tool()
async def gdrive_read_file_content(file_id: str) -> str:
    """Reads the content of a text file from Google Drive."""
    service = get_drive_service()
    if not service:
        return "❌ Error: Service not initialized."

    try:
        # Check mime type first to avoid downloading binary as text
        file_meta = service.files().get(fileId=file_id).execute()
        
        # If it's a google doc, export it
        if file_meta['mimeType'] == 'application/vnd.google-apps.document':
            request = service.files().export_media(fileId=file_id, mimeType='text/plain')
        else:
            request = service.files().get_media(fileId=file_id)
            
        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        return file_content.getvalue().decode('utf-8', errors='replace')
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"

@mcp.tool()
async def gdrive_create_folder(folder_name: str, parent_id: str = None) -> str:
    """Creates a new folder in Google Drive."""
    service = get_drive_service()
    if not service: return "❌ Service Error"
    
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]
        
    try:
        file = service.files().create(body=file_metadata, fields='id').execute()
        return f"✅ Created folder: {folder_name} (ID: {file.get('id')})"
    except Exception as e:
        return f"❌ Error creating folder: {str(e)}"

@mcp.tool()
async def gdrive_upload_text(filename: str, content: str, folder_id: str = None) -> str:
    """Uploads a text file to Google Drive."""
    service = get_drive_service()
    if not service: return "❌ Service Error"
    
    file_metadata = {'name': filename}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    media = MediaIoBaseUpload(io.BytesIO(content.encode('utf-8')), mimetype='text/plain', resumable=True)
    
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return f"✅ Uploaded file: {filename} (ID: {file.get('id')})"
    except Exception as e:
        return f"❌ Error uploading file: {str(e)}"

if __name__ == "__main__":
    mcp.run()
