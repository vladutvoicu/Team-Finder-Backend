from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, time
from typing import Literal, List


# PROJECTS

class Team_roles(BaseModel):
    role_id: UUID
    count: int


class Projects(BaseModel):
    org_id: UUID
    name: str
    period: Literal['Fixed', 'Ongoing']
    manager_id: UUID
    start_date: datetime
    deadline_date: datetime
    status: Literal['Not started', 'Starting', 'In Progress', 'Closing', 'Closed']
    description: str
    created_at: datetime = datetime.now().isoformat()
    tech_stack: List[UUID]
    team_roles: List[Team_roles]

# PROJECTS MEMBERS


class Project_members(BaseModel):
    user_id: UUID
    proj_id: UUID

# PROJECT ASSIGNMENTS


class Project_assignments(BaseModel):
    proj_id: UUID
    user_id: UUID
    proj_manager_id: UUID
    proposal: bool
    deallocated: bool
    dealloc_reason: str
    work_hours: int
    comment: str

# USER TEAM ROLES


class User_team_roles(BaseModel):
    user_id: UUID
    role_id: UUID
    proposal: bool



# PROJECT NEEDED ROLES

class Project_needed_roles(BaseModel):
    proj_id: UUID
    role_id: UUID
    count: int