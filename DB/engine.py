from typing import AsyncContextManager, Callable
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from DB.basemodel import BaseModel


async def create_session_pool(db, echo: bool = True) -> Callable[[], AsyncContextManager[AsyncSession]]:
    engine = create_async_engine(url=db, echo=echo, _is_async=True)

    async with engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.create_all)

    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool
