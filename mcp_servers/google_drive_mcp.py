
import os
import io
import sys
import logging
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
env_path = r"D:/OpenClaw/.env"
load_dotenv(env_path)

# Initialize FastMCP Server
mcp = FastMCP("Google-Drive-Py")

def get_drive_service():
    try:
        refresh_token = os.getenv("GOOGLE_DRIVE_REFRESH_TOKEN")
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        
        if not all([refresh_token, client_id, client_secret]):
            # Fallback for checking if env loaded correctly
            logger.error(f"Missing Google Drive credentials in .env. Loaded from {env_path}")
            return None

        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret
        )
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        logger.error(f"Failed to initialize Drive service: {e}")
        return None

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
