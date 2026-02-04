from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Experience models
class RoleBase(BaseModel):
    title: str
    period: str
    description: str
    skills: list[str]
    order_index: int

class RoleCreate(RoleBase):
    experience_id: str

class Role(RoleBase):
    id: str
    experience_id: str

class ExperienceBase(BaseModel):
    company: str
    location: str
    order_index: int

class ExperienceCreate(ExperienceBase):
    roles: list[RoleBase]

class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    location: Optional[str] = None
    order_index: Optional[int] = None

class Experience(ExperienceBase):
    id: str
    created_at: datetime
    roles: list[Role] = []

# Project models
class ProjectBase(BaseModel):
    title: str
    description: str
    github_url: str
    live_url: Optional[str] = None
    tags: list[str]
    colors: list[str]
    is_featured: bool = False
    order_index: int

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    tags: Optional[list[str]] = None
    colors: Optional[list[str]] = None
    is_featured: Optional[bool] = None
    order_index: Optional[int] = None

class Project(ProjectBase):
    id: str

# Cool Stuff models
class CoolStuffBase(BaseModel):
    image_url: str
    prompt: str
    order_index: int

class CoolStuffCreate(CoolStuffBase):
    pass

class CoolStuffUpdate(BaseModel):
    image_url: Optional[str] = None
    prompt: Optional[str] = None
    order_index: Optional[int] = None

class CoolStuff(CoolStuffBase):
    id: str

# Skill models
class SkillBase(BaseModel):
    name: str
    category: str
    order_index: int

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    order_index: Optional[int] = None

class Skill(SkillBase):
    id: str

# Content models
class ContentBase(BaseModel):
    id: str
    value: str

class ContentUpdate(BaseModel):
    value: str

class Content(ContentBase):
    updated_at: datetime
