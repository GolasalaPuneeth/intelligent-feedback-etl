from .models import FeedbackRecord
from .db import engine
from sqlmodel import select,Session
from sqlmodel.ext.asyncio.session import AsyncSession
from .Irepository import Irepo
from typing import Any

# async def create_trx_log(tranxlogs: TransactionLogs, session: AsyncSession) -> TransactionLogs:
#     """Inserts a new student into the database."""
#     session.add(tranxlogs)
#     await session.commit()
#     await session.refresh(tranxlogs)
#     return tranxlogs

# def tranx_device_logs(data: TransactionLogs,sync_session:Session):
#     sync_session.add(data)
#     sync_session.commit()

class Repo(Irepo):
    def save_feedback_record(self,data: dict[str, Any]):
        with Session(engine) as session:
            session.add(FeedbackRecord(**data))
            session.commit()

    def check_record_persist(self, hash:str):
        with Session(engine) as session:
            statement = select(FeedbackRecord).where(FeedbackRecord.payload_hash == hash)
            results = session.exec(statement).first() is not None
            # print(results)
            # for hero in results:
            #     print(hero)
            return results
