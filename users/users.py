from fastapi import APIRouter, HTTPException
from users.models import AdminCreate, AuthResponse, EmployeeCreate, UserLogin
from users.utils import create_admin, get_users, login_user, account_exists

user_router = APIRouter()


@user_router.post("/api/users/admin", response_model=AuthResponse)
def admin_create(user_data: AdminCreate):
    # Check if account exists with the provided email
    if not account_exists(user_data):
        admin_obj, error = create_admin(user_data)
        if error:
            raise HTTPException(status_code=500, detail="Failed to create user: " + error)
        return admin_obj
    else:
        raise HTTPException(status_code=409, detail="User with this email already exists")


@user_router.post("/api/users/employee")
def employee_create(user_data: EmployeeCreate):
    pass


@user_router.post("/api/users/login", response_model=AuthResponse)
def user_login(user_data: UserLogin):
    login_obj, error = login_user(user_data)
    if error:
        raise HTTPException(status_code=500, detail=error)
    return login_obj


@user_router.get("/api/users")
def users_get():
    return get_users()
