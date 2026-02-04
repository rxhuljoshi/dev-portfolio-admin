from fastapi import APIRouter, Depends, HTTPException
from app.models import Content, ContentUpdate, Skill, SkillCreate, SkillUpdate
from app.database import get_supabase
from app.auth import verify_admin

router = APIRouter(tags=["content"])

# Content endpoints
@router.get("/content/{content_id}", response_model=Content)
async def get_content(content_id: str):
    """Get content by ID (public)."""
    supabase = get_supabase()
    result = supabase.table("content").select("*").eq("id", content_id).single().execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return result.data

@router.get("/content", response_model=list[Content])
async def get_all_content():
    """Get all content (public)."""
    supabase = get_supabase()
    result = supabase.table("content").select("*").execute()
    return result.data

@router.put("/content/{content_id}", response_model=Content)
async def update_content(content_id: str, content: ContentUpdate, admin = Depends(verify_admin)):
    """Update or create content (admin only)."""
    supabase = get_supabase()
    
    # Upsert - update if exists, create if not
    data = {"id": content_id, "value": content.value}
    result = supabase.table("content").upsert(data).execute()
    
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to update content")
    
    return result.data[0]

# Skills endpoints
@router.get("/skills", response_model=list[Skill])
async def get_skills():
    """Get all skills (public)."""
    supabase = get_supabase()
    result = supabase.table("skills").select("*").order("order_index").execute()
    return result.data

@router.get("/skills/category/{category}", response_model=list[Skill])
async def get_skills_by_category(category: str):
    """Get skills by category (public)."""
    supabase = get_supabase()
    result = supabase.table("skills").select("*").eq("category", category).order("order_index").execute()
    return result.data

@router.post("/skills", response_model=Skill)
async def create_skill(skill: SkillCreate, admin = Depends(verify_admin)):
    """Create a new skill (admin only)."""
    supabase = get_supabase()
    
    result = supabase.table("skills").insert(skill.model_dump()).execute()
    
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to create skill")
    
    return result.data[0]

@router.put("/skills/{skill_id}", response_model=Skill)
async def update_skill(skill_id: str, skill: SkillUpdate, admin = Depends(verify_admin)):
    """Update a skill (admin only)."""
    supabase = get_supabase()
    
    update_data = {k: v for k, v in skill.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = supabase.table("skills").update(update_data).eq("id", skill_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return result.data[0]

@router.delete("/skills/{skill_id}")
async def delete_skill(skill_id: str, admin = Depends(verify_admin)):
    """Delete a skill (admin only)."""
    supabase = get_supabase()
    
    result = supabase.table("skills").delete().eq("id", skill_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return {"message": "Skill deleted"}
