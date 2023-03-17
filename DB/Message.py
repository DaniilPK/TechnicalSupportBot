from sqlalchemy import BigInteger, Integer, select,ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from DB.basemodel import BaseModel
from DB import Users


class Messages(BaseModel):
    __tablename__ = 'Messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    userID: Mapped[int] = mapped_column(BigInteger, ForeignKey("Users.userID", ondelete='CASCADE'))
    messageChatID: Mapped[int] = mapped_column(BigInteger)


async def newMessage(session: AsyncSession, userID, messageChatID):
    message = Messages(
        userID = userID,
        messageChatID=messageChatID)
    session.add(message)
    return await session.commit()

async def SearchMessage(session: AsyncSession,messageChatID):
    return (await session.execute(select(Messages.userID).where(
        Messages.messageChatID == messageChatID))).scalars().unique().one_or_none()

