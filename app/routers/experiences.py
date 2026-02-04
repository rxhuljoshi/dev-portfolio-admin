from fastapi import APIRouter, Depends, HTTPException
from app.models import Experience, ExperienceCreate, ExperienceUpdate, RoleBase
from app.database import get_supabase
from app.auth import verify_admin

router = APIRouter(prefix="/experiences", tags=["experiences"])

@router.get("/", response_model=list[Experience])
async def get_experiences():
    """Get all experiences with roles (public)."""
    supabase = get_supabase()
    
    # Get experiences
    exp_result = supabase.table("experiences").select("*").order("order_index").execute()
    
    experiences = []
    for exp in exp_result.data:
        # Get roles for each experience
        roles_result = supabase.table("roles").select("*").eq("experience_id", exp["id"]).order("order_index").execute()
        exp["roles"] = roles_result.data
        experiences.append(exp)
    
    return experiences

@router.post("/", response_model=Experience)
async def create_experience(experience: ExperienceCreate, admin = Depends(verify_admin)):
    """Create a new experience with roles (admin only)."""
    supabase = get_supabase()
    
    # Create experience
    exp_data = {
        "company": experience.company,
        "location": experience.location,
        "order_index": experience.order_index
    }
    exp_result = supabase.table("experiences").insert(exp_data).execute()
    
    if not exp_result.data:
        raise HTTPException(status_code=400, detail="Failed to create experience")
    
    exp_id = exp_result.data[0]["id"]
    
    # Create roles
    roles = []
    for role in experience.roles:
        role_data = {
            "experience_id": exp_id,
            "title": role.title,
            "period": role.period,
            "description": role.description,
            "skills": role.skills,
            "order_index": role.order_index
        }
        role_result = supabase.table("roles").insert(role_data).execute()
        if role_result.data:
            roles.append(role_result.data[0])
    
    result = exp_result.data[0]
    result["roles"] = roles
    return result

@router.put("/{experience_id}", response_model=Experience)
async def update_experience(experience_id: str, experience: ExperienceUpdate, admin = Depends(verify_admin)):
    """Update an experience (admin only)."""
    supabase = get_supabase()
    
    update_data = {k: v for k, v in experience.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = supabase.table("experiences").update(update_data).eq("id", experience_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    # Get roles
    roles_result = supabase.table("roles").select("*").eq("experience_id", experience_id).order("order_index").execute()
    result.data[0]["roles"] = roles_result.data
    
    return result.data[0]

@router.delete("/{experience_id}")
async def delete_experience(experience_id: str, admin = Depends(verify_admin)):
    """Delete an experience and its roles (admin only)."""
    supabase = get_supabase()
    
    # Roles will be deleted via cascade
    result = supabase.table("experiences").delete().eq("id", experience_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    return {"message": "Experience deleted"}

@router.post("/{experience_id}/roles")
async def add_role(experience_id: str, role: RoleBase, admin = Depends(verify_admin)):
    """Add a role to an experience (admin only)."""
    supabase = get_supabase()
    
    role_data = {
        "experience_id": experience_id,
        "title": role.title,
        "period": role.period,
        "description": role.description,
        "skills": role.skills,
        "order_index": role.order_index
    }
    
    result = supabase.table("roles").insert(role_data).execute()
    
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to add role")
    
    return result.data[0]

@router.delete("/roles/{role_id}")
async def delete_role(role_id: str, admin = Depends(verify_admin)):
    """Delete a role (admin only)."""
    supabase = get_supabase()
    
    result = supabase.table("roles").delete().eq("id", role_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Role not found")
    
    return {"message": "Role deleted"}
