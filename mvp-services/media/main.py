from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import json
from typing import Optional, Dict, Any
import os
from minio import Minio
from minio.error import S3Error
import uuid
from datetime import datetime

# Configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "minioadmin") 
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")
MINIO_BUCKET = os.getenv("MINIO_BUCKET_NAME", "bvckz-files")

# Initialize FastAPI
app = FastAPI(
    title="BvckZ Media Service",
    description="Image composition and preview generation for BvckZ MVP",
    version="0.1.0"
)

# Initialize MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Ensure bucket exists
try:
    if not minio_client.bucket_exists(MINIO_BUCKET):
        minio_client.make_bucket(MINIO_BUCKET)
except S3Error as e:
    print(f"Error creating bucket: {e}")

class DesignRequest(BaseModel):
    left_design: Optional[str] = None
    center_color: str = "blue"
    right_pattern: Optional[str] = None
    width: int = 800
    height: int = 600

class PreviewResponse(BaseModel):
    preview_url: str
    file_id: str
    created_at: str

def get_color_rgb(color_name: str) -> tuple:
    """Convert color name to RGB tuple"""
    colors = {
        "blue": (59, 130, 246),
        "green": (34, 197, 94),
        "red": (239, 68, 68), 
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "gray": (107, 114, 128),
        "orange": (245, 158, 11)
    }
    return colors.get(color_name.lower(), (59, 130, 246))

def create_gradient(width: int, height: int, color1: tuple, color2: tuple) -> Image.Image:
    """Create gradient background"""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            ratio = x / width
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio) 
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pixels[x, y] = (r, g, b)
    
    return img

def add_text_overlay(img: Image.Image, text: str, position: str = "center") -> Image.Image:
    """Add text overlay to image"""
    draw = ImageDraw.Draw(img)
    
    # Try to use a better font, fallback to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    if position == "center":
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
    elif position == "top":
        x = (img.width - text_width) // 2
        y = 20
    else:  # bottom
        x = (img.width - text_width) // 2
        y = img.height - text_height - 20
    
    # Add text with outline
    outline_color = "black" if sum(get_color_rgb("white")) > 400 else "white"
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    
    draw.text((x, y), text, font=font, fill="white")
    return img

def generate_t_shirt_preview(design: DesignRequest) -> Image.Image:
    """Generate 3-panel T-shirt preview"""
    panel_width = design.width // 3
    panel_height = design.height
    
    # Create main image
    preview = Image.new('RGB', (design.width, design.height), (240, 240, 240))
    
    # Left panel (additional design)
    left_color = get_color_rgb("gray")
    left_img = create_gradient(panel_width, panel_height, left_color, 
                              (left_color[0] - 50, left_color[1] - 50, left_color[2] - 50))
    
    if design.left_design:
        design_texts = {
            "logo": "LOGO",
            "pattern": "◆◇◆",
            "text": "ТЕКСТ"
        }
        text = design_texts.get(design.left_design, design.left_design.upper())
        left_img = add_text_overlay(left_img, text, "center")
    else:
        left_img = add_text_overlay(left_img, "Левая\nсторона", "center")
    
    # Center panel (main t-shirt)
    center_color = get_color_rgb(design.center_color)
    center_img = create_gradient(panel_width, panel_height, center_color,
                                (center_color[0] - 80, center_color[1] - 80, center_color[2] - 80))
    center_img = add_text_overlay(center_img, "ОСНОВНАЯ\nФУТБОЛКА", "center")
    
    # Right panel (national pattern)
    right_color = get_color_rgb("orange")
    right_img = create_gradient(panel_width, panel_height, right_color,
                               (right_color[0] - 60, right_color[1] - 60, right_color[2] - 60))
    
    if design.right_pattern:
        pattern_texts = {
            "kazakh": "🏺 ⚡ 🌸",
            "uzbek": "🌟 ❋ 🔸",
            "kyrgyz": "⬢ ⬡ ◊",
            "abstract": "◈ ◉ ◎"
        }
        text = pattern_texts.get(design.right_pattern, f"{design.right_pattern.upper()}\nОРНАМЕНТ")
        right_img = add_text_overlay(right_img, text, "center")
    else:
        right_img = add_text_overlay(right_img, "Национальный\nорнамент", "center")
    
    # Compose final image
    preview.paste(left_img, (0, 0))
    preview.paste(center_img, (panel_width, 0))
    preview.paste(right_img, (panel_width * 2, 0))
    
    # Add borders
    draw = ImageDraw.Draw(preview)
    draw.line([(panel_width, 0), (panel_width, panel_height)], fill="white", width=2)
    draw.line([(panel_width * 2, 0), (panel_width * 2, panel_height)], fill="white", width=2)
    
    return preview

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "media", "timestamp": datetime.utcnow().isoformat()}

@app.post("/render", response_model=PreviewResponse)
async def render_preview(design: DesignRequest):
    """Generate and store T-shirt preview"""
    try:
        # Generate preview image
        preview_img = generate_t_shirt_preview(design)
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        preview_img.save(img_bytes, format='PNG', quality=95)
        img_bytes.seek(0)
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = f"previews/{file_id}.png"
        
        # Upload to MinIO
        minio_client.put_object(
            MINIO_BUCKET,
            filename,
            img_bytes,
            img_bytes.getbuffer().nbytes,
            content_type="image/png"
        )
        
        # Generate public URL
        preview_url = f"http://{MINIO_ENDPOINT}/{MINIO_BUCKET}/{filename}"
        
        return PreviewResponse(
            preview_url=preview_url,
            file_id=file_id,
            created_at=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview generation failed: {str(e)}")

@app.get("/preview/{file_id}")
async def get_preview(file_id: str):
    """Get preview image by file ID"""
    try:
        filename = f"previews/{file_id}.png"
        
        # Get object from MinIO
        response = minio_client.get_object(MINIO_BUCKET, filename)
        img_data = response.read()
        response.close()
        response.release_conn()
        
        return StreamingResponse(
            io.BytesIO(img_data),
            media_type="image/png",
            headers={"Content-Disposition": f"inline; filename={file_id}.png"}
        )
        
    except S3Error as e:
        if e.code == "NoSuchKey":
            raise HTTPException(status_code=404, detail="Preview not found")
        else:
            raise HTTPException(status_code=500, detail=f"Storage error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving preview: {str(e)}")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload file to storage"""
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Only image files are allowed")
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"uploads/{file_id}.{extension}"
        
        # Upload to MinIO
        minio_client.put_object(
            MINIO_BUCKET,
            filename,
            file.file,
            length=-1,
            part_size=10*1024*1024,
            content_type=file.content_type
        )
        
        # Generate public URL
        file_url = f"http://{MINIO_ENDPOINT}/{MINIO_BUCKET}/{filename}"
        
        return {
            "file_id": file_id,
            "filename": filename,
            "url": file_url,
            "content_type": file.content_type,
            "uploaded_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/templates")
async def get_design_templates():
    """Get available design templates"""
    templates = {
        "left_designs": [
            {"id": "logo", "name": "Логотип", "description": "Простой логотип или текст"},
            {"id": "pattern", "name": "Узор", "description": "Геометрический узор"},
            {"id": "abstract", "name": "Абстракция", "description": "Абстрактный дизайн"}
        ],
        "colors": [
            {"id": "blue", "name": "Синий", "hex": "#3b82f6"},
            {"id": "green", "name": "Зелёный", "hex": "#22c55e"},
            {"id": "red", "name": "Красный", "hex": "#ef4444"},
            {"id": "black", "name": "Чёрный", "hex": "#000000"},
            {"id": "white", "name": "Белый", "hex": "#ffffff"}
        ],
        "patterns": [
            {"id": "kazakh", "name": "Казахский орнамент", "description": "Традиционные казахские узоры"},
            {"id": "uzbek", "name": "Узбекский орнамент", "description": "Традиционные узбекские узоры"},  
            {"id": "kyrgyz", "name": "Киргизский орнамент", "description": "Традиционные киргизские узоры"},
            {"id": "abstract", "name": "Абстрактный", "description": "Современный абстрактный узор"}
        ]
    }
    return templates

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
