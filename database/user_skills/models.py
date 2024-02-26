from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class UserSkills(Base):
    __tablename__ = "user_skills"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), primary_key=True, nullable=False)
    level = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    @staticmethod
    def serialize_user_skills(user_skills):
        serialized_user_skills = {}
        index = 0
        for user_skill in user_skills:
            serialized_user_skills[index] = {
                "user_id": str(user_skill.user_id),
                "skill_id": str(user_skill.skill_id),
                "level": str(user_skill.level),
                "experience": str(user_skill.experience),
                "created_at": str(user_skill.created_at)
            }
            index += 1
        return serialized_user_skills
