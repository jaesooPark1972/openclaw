"""
GLM-OCR MCP Server for OpenClaw Integration
Provides document OCR capabilities via the Rust API server.
"""
from mcp.server.fastmcp import FastMCP
import httpx
import os

# Define the MCP server
mcp = FastMCP("GLM-OCR-Service")

API_URL = os.environ.get("GLM_OCR_API_URL", "http://localhost:8090/api/ocr")
REQUEST_TIMEOUT = float(os.environ.get("GLM_OCR_TIMEOUT", "300"))

@mcp.tool()
async def analyze_document_layout(image_path: str) -> str:
    """
    Analyzes a document image or PDF using the GLM-OCR engine via the high-performance Rust API.
    Returns structured markdown content, perfect for complex layouts, tables, and formulas.
    
    Args:
        image_path (str): Absolute path to the local image or PDF file.
    
    Returns:
        str: Markdown formatted OCR result or error message.
    """
    if not os.path.isabs(image_path):
        return f"Error: Please provide an absolute path to the file."
    
    if not os.path.exists(image_path):
        return f"Error: File not found at {image_path}"
    
    file_size = os.path.getsize(image_path)
    print(f"📄 Sending document to OCR engine: {image_path} ({file_size:,} bytes)")
    
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            # Prepare multipart upload with proper file handling
            with open(image_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(image_path), f, 'application/octet-stream')
                }
                response = await client.post(API_URL, files=files)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    markdown = data.get("markdown", "")
                    meta = data.get("meta", {})
                    processing_time = meta.get("processing_time_seconds", "N/A")
                    return f"## OCR Analysis Result\n\n{markdown}\n\n---\n*Processed in {processing_time}s*"
                else:
                    error_msg = data.get('error', 'Unknown error')
                    return f"OCR Failed: {error_msg}"
            else:
                return f"API Error: {response.status_code} - {response.text}"

    except httpx.TimeoutException:
        return f"Timeout Error: OCR request timed out after {REQUEST_TIMEOUT}s"
    except httpx.ConnectError:
        return f"Connection Error: Cannot connect to OCR service at {API_URL}. Is the Rust server running?"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def check_ocr_service_health() -> str:
    """
    Checks if the GLM-OCR Rust service is running and healthy.
    
    Returns:
        str: Health status message.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{API_URL.replace('/api/ocr', '/health')}")
            if response.status_code == 200:
                return "✅ GLM-OCR Service is healthy and ready."
            else:
                return f"⚠️ Service returned status {response.status_code}"
    except Exception as e:
        return f"❌ Service is not accessible: {str(e)}"

if __name__ == "__main__":
    print("🚀 Starting GLM-OCR MCP Server...")
    print(f"📡 API URL: {API_URL}")
    print(f"⏱️  Timeout: {REQUEST_TIMEOUT}s")
    mcp.run()
