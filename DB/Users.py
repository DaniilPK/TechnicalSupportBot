from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, select, DateTime, Boolean, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DB.Message import Messages
from DB.basemodel import BaseModel


class Users(BaseModel):
    __tablename__ = 'Users'

    userID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ban: Mapped[int] = mapped_column(Boolean, default=False)
    #client_ban: Mapped[int] = mapped_column(Boolean, default=False)
    regTm: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    child = relationship(Messages, backref="parent", passive_deletes=True)


async def search_or_create_user(session: AsyncSession, user_id: int):
    user = await session.execute(select(Users.ban).where(Users.userID == user_id))
    Users_ban = user.fetchone()
    if Users_ban is None:
        user = Users(userID=user_id)
        session.add(user)
        await session.commit()
        return False
    else:
        return Users_ban[0]


async def update_status(session: AsyncSession, user_id: int, status: str, value: bool):
    await session.execute(update(Users).where(Users.userID == user_id)
                          .values({status: value}))
    return await session.commit()
