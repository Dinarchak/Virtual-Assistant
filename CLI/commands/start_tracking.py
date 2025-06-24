import psutil
import os
from typing import List, Dict
from db.models import Process, LifePeriod
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from settings import config

# список процессов, завершенных в течение последник 5 секунд
closed_list: List[LifePeriod] = []

# вспомогательный словарь, ключ - Process.name, значение - Process.id
process_ids: Dict[str, int] = {}


def find_procs_by_name(processes: List[Process]) -> List[psutil.Process]:
    """Выдает информацию о запущенных процессах из списка processes

    Args:
        processes (List[Process]): список отслеживаемых процессов

    Returns:
        List[psutil.Process]: список всех запущенных процессов
    """
    res = []
    for procs in processes:
        for p in psutil.process_iter(["name", "exe", "cmdline"]):
            if procs.name == p.info['name'] or \
                    p.info['exe'] and \
                    os.path.basename(p.info['exe']) == procs.name or \
                    p.info['cmdline'] and p.info['cmdline'][0] == procs.name:
                res.append(p)
                break
    return res


def process_end_callback(procs: psutil.Process) -> None:
    """Вызывается когда некоторый процесс останавливается.
    Фиксирует в списке closed_list новый период работы процесса.
    Args:
        procs (psutil.Process): экзепляр остановленного процесса
    """
    now = datetime.now()
    started_at = datetime.fromtimestamp(procs.create_time())

    if started_at.day == now.day:
        closed_list.append(LifePeriod(process_id=process_ids[procs.info['name']],
                                  start=started_at,
                                  end=now,
                                  delta=(now - started_at).total_seconds()))
        return
    
    next_day_start = started_at + timedelta(days=1)
    next_day_start -= timedelta(hours=started_at.hour,
                                minutes=started_at.minute,
                                seconds=started_at.second,
                                microseconds=started_at.microsecond)

    closed_list.append(LifePeriod(process_id=process_ids[procs.info['name']],
                                start=started_at,
                                end=next_day_start,
                                delta=(next_day_start - started_at).total_seconds()))
    closed_list.append(LifePeriod(process_id=process_ids[procs.info['name']],
                                start=next_day_start,
                                end=now,
                                delta=(now - next_day_start).total_seconds()))
        


def start_tracking() -> None:
    """Мониторинг работы процессов.
    """
    engine = create_engine(config['db_url'], echo=True)
    with Session(engine) as session:
        all_processes = list(session.scalars(select(Process)))
        print(type(all_processes), all_processes)
        for procs in all_processes:
            process_ids[procs.name] = procs.id
        while True:
            closed_list.clear()
            processes = find_procs_by_name(all_processes)
            # каждые 5 секунд проверяет, какие процессы работают
            psutil.wait_procs(processes,
                              callback=process_end_callback,
                              timeout=5)
            # записать в БД завершенные периоды работы процессов
            if len(closed_list) > 0:
                session.add_all(closed_list)
                session.commit()
