import uuid
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    admin_id = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    hq_address = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    @staticmethod
    def serialize_organizations(organizations):
        serialize_organization = {}
        for organization in organizations:
            serialize_organization[str(organization.id)] = {
                "id": str(organization.id),
                "admin_id": str(organization.admin_id),
                "name": str(organization.name),
                "hq_address": str(organization.hq_address),
                "created_at": str(organization.created_at)
            }
        return serialize_organization
