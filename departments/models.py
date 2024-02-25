from pydantic import BaseModel
from uuid import UUID


class Department(BaseModel):
    org_id: UUID
    name: str
    manager_id: UUID
