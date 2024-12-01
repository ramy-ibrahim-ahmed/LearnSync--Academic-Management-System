from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_schemas.user import User
from ..schemas.user import UserCreate


class UserModel:
    def __init__(self, db_client: AsyncSession):
        self.db_client = db_client

    async def read_user_by_id(self, user_id: int):
        result = await self.db_client.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def read_user_by_email(self, email: str):
        result = await self.db_client.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def read_users(self, skip: int = 0, limit: int = 100):
        result = await self.db_client.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_user(self, user: UserCreate):
        db_user = User(email=user.email, role=user.role)
        self.db_client.add(db_user)
        await self.db_client.commit()
        await self.db_client.refresh(db_user)
        return db_user
