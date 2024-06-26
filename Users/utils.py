from uuid import uuid4
from auth import AuthHandler
from datetime import datetime, timedelta
import secrets
from passlib.context import CryptContext
from database.db import db
from smtp import send_email

auth_handler = AuthHandler()
pwd_context = CryptContext(schemes=["bcrypt"])


def create_admin(data):
    user_data = data.model_dump()
    org_roles = db.get_organization_roles()
    user_id = str(uuid4())
    org_id = str(uuid4())
    user_data["id"] = user_id
    created_at = datetime.utcnow()
    hashed_password = auth_handler.get_password_hash(user_data.get("password"))
    db.create_organization(organization_id=org_id,
                           name=user_data.get("org_name"),
                           hq_address=user_data.get("hq_address"),
                           created_at=created_at)

    admin_obj, error = db.create_admin(name=user_data.get("name"),
                                       email=user_data.get("email"),
                                       password=hashed_password,
                                       created_at=created_at,
                                       org_id=org_id,
                                       user_id=user_id)

    for key in org_roles:
        if org_roles[key].get("name") == "admin":
            db.create_user_role(user_id=user_id, role_id=org_roles[key].get("id"))

    admin_obj["org_name"] = user_data.get("org_name")
    admin_obj["hq_address"] = user_data.get("hq_address")
    admin_obj["roles"] = ["admin"]
    del admin_obj["created_at"], admin_obj["org_id"]

    return admin_obj, error


def create_employee(data):
    user_data = data.model_dump()
    user_id = str(uuid4())
    user_data["id"] = user_id
    created_at = datetime.utcnow()
    hashed_password = auth_handler.get_password_hash(user_data.get("password"))
    token = user_data.get("token")
    signup_token = db.get_signup_token(token)

    if signup_token:
        org_id = signup_token[0].get("org_id")
        format = "%Y-%m-%d %H:%M:%S"
        current_time = datetime.utcnow()

        if datetime.strptime(signup_token[0].get("expires_at"), format) > current_time:
            employee_obj, error = db.create_employee(name=user_data.get("name"),
                                                     email=user_data.get("email"),
                                                     password=hashed_password,
                                                     created_at=created_at,
                                                     org_id=org_id,
                                                     user_id=user_id)

            db.delete_signup_token(token)
        else:
            return False, "Sign up token expired"
    else:
        return False, "Sign up token invalid"

    org_data = db.get_organization(org_id)
    employee_obj["org_name"] = org_data.get("name")
    employee_obj["hq_address"] = org_data.get("hq_address")
    employee_obj["roles"] = ["employee"]
    del employee_obj["created_at"], employee_obj["org_id"]

    return employee_obj, error


def account_exists(data):
    signup_data = data.model_dump()
    users_data = db.get_users()

    for key in users_data:
        if users_data[key].get("email") == signup_data.get("email"):
            return True
    return False


def login_user(data):
    login_data = data.model_dump()
    users_data = db.get_users()

    for key in users_data:
        if users_data[key].get("email") == login_data.get("email"):
            user_data = users_data[key]

            if auth_handler.verify_password(login_data.get("password"), user_data.get("password")):
                login_data["name"] = user_data.get("name")
                login_data["id"] = user_data.get("id")

                if user_data.get("org_id"):
                    org_data = db.get_organization(user_data.get("org_id"))
                    org_roles = db.get_organization_roles()
                    user_roles = db.user_roles_get(user_data.get("id"))

                    user_role_names = []
                    for role_id in user_roles:
                        if org_roles.get(role_id):
                            user_role_names.append(org_roles.get(role_id).get("name"))

                    login_data["roles"] = user_role_names
                    login_data["org_name"] = org_data.get("name")
                    login_data["hq_address"] = org_data.get("hq_address")
                    login_data["organization_status"] = org_data.get("demo")
                    return login_data, False
                else:
                    return login_data, "Authentication successful but not apart of an organization"
            else:
                return login_data, "Incorrect password"

    return login_data, "Incorrect email"


def get_user(id):
    users_data = db.get_users()
    user_data = users_data.get(id)

    org_roles = db.get_organization_roles()
    user_roles = db.user_roles_get(user_data.get("id"))

    user_role_names = []
    for role_id in user_roles:
        if org_roles.get(role_id):
            user_role_names.append(org_roles.get(role_id).get("name"))

    if not user_role_names:
        user_role_names.append("employee")

    org_data = db.get_organization(user_data.get("org_id"))

    user_data["roles"] = user_role_names
    user_data["org_name"] = org_data.get("name")
    user_data["hq_address"] = org_data.get("hq_address")
    user_data["organization_status"] = org_data.get("demo")

    del user_data["id"], user_data["password"], user_data["created_at"], user_data["org_id"]

    return user_data


def create_password_reset_token(email):
    format = "%Y-%m-%d %H:%M:%S"
    current_time = datetime.utcnow().strftime(format)
    expires_at = datetime.strptime(current_time, format) + timedelta(hours=12)
    id = secrets.token_urlsafe(16)

    token, error = db.create_password_reset_token(id, email, expires_at)

    if token:
        send_email(receiver_email=email,
                   token=token.get("id"))

    return token, error


def verify_password_reset_token(token):
    signup_tokens = db.get_password_reset_tokens()
    format = "%Y-%m-%d %H:%M:%S"
    current_time = datetime.utcnow()

    for token_obj in signup_tokens:
        if token_obj.get("id") == token:
            if datetime.strptime(token_obj.get("expires_at"), format) < current_time:
                return None, "Reset password token expired"
            else:
                user_data = db.get_user(token_obj.get("user_id"))
                return user_data.get("email"), None

    return None, "Reset password token invalid"


def reset_password(data):
    password_data = data.model_dump()
    password = password_data.get("password")
    token = password_data.get("token")

    hashed_password = auth_handler.get_password_hash(password)

    password_reset_token = db.get_password_reset_token(token)

    if password_reset_token:
        user_id = password_reset_token.get("user_id")
        format = "%Y-%m-%d %H:%M:%S"
        current_time = datetime.utcnow()

        if datetime.strptime(str(password_reset_token.get("expires_at")), format) > current_time:
            returned_data = db.reset_password(user_id=user_id, password=hashed_password)
            db.delete_password_reset_token(token)

            user_data = db.get_user(user_id)

            login_data = {}
            login_data["name"] = user_data.get("name")
            login_data["id"] = user_data.get("id")
            login_data["email"] = user_data.get("email")

            if user_data.get("org_id"):
                org_data = db.get_organization(user_data.get("org_id"))
                org_roles = db.get_organization_roles()
                user_roles = db.user_roles_get(user_data.get("id"))

                user_role_names = []
                for role_id in user_roles:
                    if org_roles.get(role_id):
                        user_role_names.append(org_roles.get(role_id).get("name"))

                login_data["roles"] = user_role_names
                login_data["org_name"] = org_data.get("name")
                login_data["hq_address"] = org_data.get("hq_address")
                login_data["organization_status"] = org_data.get("demo")
                return login_data, False
        else:
            return False, "Reset token expired"
    else:
        return False, "Reset token invalid"
