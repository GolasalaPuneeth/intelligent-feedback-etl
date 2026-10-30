from .models import FeedbackRecord,PayloadErrorLogs
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


# class Repo(Irepo):
#     def save_feedback_record(self,data: dict[str, Any]):
#         with Session(engine) as session:
#             session.add(FeedbackRecord(**data))
#             session.commit()

#     def check_record_persist(self, hash:str):
#         with Session(engine) as session:
#             statement = select(FeedbackRecord).where(FeedbackRecord.payload_hash == hash)
#             results = session.exec(statement).first() is not None
#             return results

class Repo(Irepo):
    def save_feedback_record(self, data: dict[str, Any]) -> None:
        with Session(engine) as session:
            try:
                session.add(FeedbackRecord(**data))
                session.commit()
            except Exception:
                session.rollback()
                raise

    def check_record_persist(self, hash: str) -> bool:
        with Session(engine) as session:
            try:
                statement = select(FeedbackRecord).where(
                    FeedbackRecord.payload_hash == hash
                )
                return session.exec(statement).first() is not None
            except Exception:
                session.rollback()
                raise
    def add_error_log_info(self, data:PayloadErrorLogs):
        with Session(engine) as session:
            try:
                session.add(data)
                session.commit()
                return True
            except Exception:
                session.rollback()
                raise
       