import psutil
import os
from models import Process, LifePeriod
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

closed_list = []
process_ids = {}

def process_end_callback(procs):
    print(procs.info['name'], process_ids)
    closed_list.append(LifePeriod(process_id=process_ids[procs.info['name']], start=datetime.fromtimestamp(procs.create_time()), end=datetime.now()))


def find_procs_by_name(processes):
    res = []
    for procs in processes:
        for p in psutil.process_iter(["name", "exe", "cmdline"]):
            if procs.name == p.info['name'] or \
                    p.info['exe'] and os.path.basename(p.info['exe']) == procs.name or \
                    p.info['cmdline'] and p.info['cmdline'][0] == procs.name:
                    res.append(p)
                    break
    return res


def main():
    engine = create_engine('sqlite:///db.sqlite3', echo=True)
    with Session(engine) as session:
        all_processes = list(session.scalars(select(Process)))
        for procs in all_processes:
            process_ids[procs.name] = procs.id
        while True:
            closed_list.clear()
            processes = find_procs_by_name(all_processes)
            psutil.wait_procs(processes, callback=process_end_callback, timeout=5)
            if len(closed_list) > 0:
                session.add_all(closed_list)
                session.commit()
main()