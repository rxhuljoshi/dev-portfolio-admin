from fastapi import APIRouter, Depends, HTTPException
from app.models import Project, ProjectCreate, ProjectUpdate
from app.database import get_supabase
from app.auth import verify_admin

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=list[Project])
async def get_projects():
    """Get all projects (public)."""
    supabase = get_supabase()
    result = supabase.table("projects").select("*").order("order_index").execute()
    return result.data

@router.get("/featured", response_model=list[Project])
async def get_featured_projects():
    """Get featured projects (public)."""
    supabase = get_supabase()
    result = supabase.table("projects").select("*").eq("is_featured", True).order("order_index").execute()
    return result.data

@router.post("/", response_model=Project)
async def create_project(project: ProjectCreate, admin = Depends(verify_admin)):
    """Create a new project (admin only)."""
    supabase = get_supabase()
    
    result = supabase.table("projects").insert(project.model_dump()).execute()
    
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to create project")
    
    return result.data[0]

@router.put("/{project_id}", response_model=Project)
async def update_project(project_id: str, project: ProjectUpdate, admin = Depends(verify_admin)):
    """Update a project (admin only)."""
    supabase = get_supabase()
    
    update_data = {k: v for k, v in project.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = supabase.table("projects").update(update_data).eq("id", project_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return result.data[0]

@router.delete("/{project_id}")
async def delete_project(project_id: str, admin = Depends(verify_admin)):
    """Delete a project (admin only)."""
    supabase = get_supabase()
    
    result = supabase.table("projects").delete().eq("id", project_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"message": "Project deleted"}
