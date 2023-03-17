import logging

from sqlalchemy import BigInteger, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from DB import BaseModel


class Users(BaseModel):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    userID: Mapped[int] = mapped_column(BigInteger)
    messageChatID: Mapped[int] = mapped_column(BigInteger)


async def newMessage(session: AsyncSession, userID, messageChatID):
    user = Users(
        userID = userID,
        messageChatID=messageChatID)
    session.add(user)
    return await session.commit()

async def SearchMessage(session: AsyncSession,messageChatID):
    return (await session.execute(select(Users.userID).where(
        Users.messageChatID == messageChatID))).scalars().unique().one_or_none()

