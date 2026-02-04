from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.models import CoolStuff, CoolStuffCreate, CoolStuffUpdate
from app.database import get_supabase
from app.auth import verify_admin
import uuid

router = APIRouter(prefix="/coolstuff", tags=["cool stuff"])

@router.get("/", response_model=list[CoolStuff])
async def get_cool_stuff():
    """Get all cool stuff items (public)."""
    supabase = get_supabase()
    result = supabase.table("cool_stuff").select("*").order("order_index").execute()
    return result.data

@router.post("/", response_model=CoolStuff)
async def create_cool_stuff(cool_stuff: CoolStuffCreate, admin = Depends(verify_admin)):
    """Create a new cool stuff item (admin only)."""
    supabase = get_supabase()
    
    result = supabase.table("cool_stuff").insert(cool_stuff.model_dump()).execute()
    
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to create cool stuff")
    
    return result.data[0]

@router.post("/upload")
async def upload_image(file: UploadFile = File(...), admin = Depends(verify_admin)):
    """Upload an image to Supabase storage (admin only)."""
    supabase = get_supabase()
    
    # Generate unique filename
    file_ext = file.filename.split(".")[-1] if file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{file_ext}"
    
    # Read file content
    content = await file.read()
    
    # Upload to Supabase storage
    result = supabase.storage.from_("cool-stuff").upload(filename, content)
    
    if hasattr(result, 'error') and result.error:
        raise HTTPException(status_code=400, detail=f"Upload failed: {result.error}")
    
    # Get public URL
    public_url = supabase.storage.from_("cool-stuff").get_public_url(filename)
    
    return {"url": public_url, "filename": filename}

@router.put("/{cool_stuff_id}", response_model=CoolStuff)
async def update_cool_stuff(cool_stuff_id: str, cool_stuff: CoolStuffUpdate, admin = Depends(verify_admin)):
    """Update a cool stuff item (admin only)."""
    supabase = get_supabase()
    
    update_data = {k: v for k, v in cool_stuff.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = supabase.table("cool_stuff").update(update_data).eq("id", cool_stuff_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Cool stuff not found")
    
    return result.data[0]

@router.delete("/{cool_stuff_id}")
async def delete_cool_stuff(cool_stuff_id: str, admin = Depends(verify_admin)):
    """Delete a cool stuff item (admin only)."""
    supabase = get_supabase()
    
    result = supabase.table("cool_stuff").delete().eq("id", cool_stuff_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Cool stuff not found")
    
    return {"message": "Cool stuff deleted"}
