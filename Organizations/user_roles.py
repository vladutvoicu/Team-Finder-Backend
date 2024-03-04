from fastapi import APIRouter
from Organizations.models import UserRole, RemoveRole
from Organizations.utils import *

user_roles_router = APIRouter()


@user_roles_router.post("/api/organizations/user_roles", response_model=UserRole)
def create_user_role_route(user_role_data: UserRole):
    return create_user_role(user_role_data)


@user_roles_router.get("/api/organizations/user_roles")
def user_roles_get(user_id):
    return get_user_roles(user_id)


@user_roles_router.delete("/api/organizations/user_roles")
def user_role_delete(removed_data: RemoveRole):
    return delete_user_role(removed_data)