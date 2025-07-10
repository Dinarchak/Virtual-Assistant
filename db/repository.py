from sqlalchemy import extract, func, create_engine, select
from .models import LifePeriod, Process, ProcessType
from .schemas import (
    BarQuerySchema,
    ScaleQuerySchema,
    DailyTimeSchema
)
from sqlalchemy.orm import Session
from schemas import *
from typing import List


class Repository:
    def __init__(self, engine):
        self.eng = engine
    
    def bar_query(self, start_time, end_time) -> List[BarQuerySchema]:
        with Session(self.eng) as session:
            query = (session.query(Process.name, func.sum(LifePeriod.delta))
                .where(LifePeriod.start >= start_time, LifePeriod.end <= end_time)
                .join(Process)
                .group_by(LifePeriod.process_id).all())
            
        valid_query = [BarQuerySchema(name=i[0], delta=i[1]) for i in query]
        return valid_query
    
    def scale_query(self, start_time, end_time) -> List[ScaleQuerySchema]:
        with Session(self.eng) as session:
            query = (session.query(Process.name, LifePeriod.start, LifePeriod.end)
                .where(LifePeriod.start >= start_time, LifePeriod.end <= end_time)
                .join(Process))
        
        valid_query = [ScaleQuerySchema(name=i[0], start=i[1], end=i[2]) for i in query]
        return valid_query
    
    def daily_time_query(self, start_time, end_time) -> List[DailyTimeSchema]:
        with Session(self.eng) as session:
            query = (session.query(Process.name, func.sum(LifePeriod.delta), extract('day', LifePeriod.start))
                .where(LifePeriod.start >= start_time,
                        LifePeriod.end <= end_time,
                        extract('day', LifePeriod.start) == extract('day', LifePeriod.end))
                .join(Process, isouter=True)
                .group_by(Process.name, extract('day', LifePeriod.start))
                .order_by(extract('day', LifePeriod.start)))
        valid_query = [DailyTimeSchema(name=i[0], delta=i[1], day=i[2]) for i in query]
        return valid_query
    
    def add_app(self, name: str, type_name: int) -> None:
        with Session(self.eng) as session:
            type = session.scalars(
                select(ProcessType).where(ProcessType.name == type_name)
                ).first()
            procs = Process(name=name, type_id=type.id)
            session.add(procs)
            session.commit()

    def delete_app(self, name: str) -> None:
        with Session(self.eng) as session:
            procs = session.scalars(
                select(Process).where(Process.name == name)
                ).first()
            if procs is None:
                return False
            session.delete(procs)
        session.commit()
        return True
    
    def get_apps(self) -> List[Process]:
        with Session(self.eng) as session:
            return list(session.scalars(select(Process)))
        
    def record_app_life_periods(self, closed_list: List[LifePeriod]) -> None:
        with Session(self.eng) as session:
            session.add_all(closed_list)
            session.commit()

    def get_all_processes(self) -> List[Process]:
        with Session(self.eng) as session:
            return list(session.scalars(select(Process)))