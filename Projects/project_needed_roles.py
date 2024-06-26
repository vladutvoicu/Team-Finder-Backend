from fastapi import APIRouter, Depends
from auth import AuthHandler
from uuid import UUID
from Projects.models import ProjectNeededRoles, UpdateProjectNeededRoles
from Projects.utils import create_project_needed_role, get_project_needed_roles, update_project_needed_role

auth_handler = AuthHandler()
project_needed_roles_router = APIRouter(tags=["Projects"])


@project_needed_roles_router.post("/api/projects/project_needed_roles", response_model=ProjectNeededRoles)
def create_project_needed_role_route(project_needed_roles_data: ProjectNeededRoles, user_id: str = Depends(auth_handler.auth_wrapper)):
    return create_project_needed_role(project_needed_roles_data)


@project_needed_roles_router.put("/api/projects/project_needed_roles", response_model=UpdateProjectNeededRoles)
def update_project_needed_role_put(project_needed_roles_data: UpdateProjectNeededRoles, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_project_needed_role(project_needed_roles_data)


@project_needed_roles_router.get("/api/projects/project_needed_roles")
def project_needed_roles_get(proj_id: UUID, user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_project_needed_roles(proj_id, user_id)
