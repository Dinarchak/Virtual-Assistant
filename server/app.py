from sqlalchemy import create_engine
from aiohttp import web
import aiohttp_cors
from settings import config
from schemas import TabInfoSchema
from datetime import datetime
from db import Repository
from db.models import LifePeriod
import typing as tp

async def on_startup(app):
    app['tabs'] = []
    app['repo'] = Repository(create_engine(config['db_url']))

app = web.Application()
routes = web.RouteTableDef()

app.on_startup.append(on_startup)

@routes.post('/upd_stat')
async def update_stat(request):
    data = await request.json()
    tabs_info = [TabInfoSchema(
            url=i,
            time=datetime.strptime(
                data['time'],
                config['datetime_str_format_js'])
            ) for i in data['tabs']]
    
    closed_list = []

    all_sites = app['repo'].get_all_sites()
    sites_ids: tp.Dict[str, int] = {}
    sites_pattern = {}

    for procs in all_sites:
        sites_ids[procs.name] = procs.id

    for i in tabs_info:
        for url_pattern in sites_ids.keys():
            if url_pattern in i.url:
                sites_pattern[i.url] = url_pattern
                break
    to_remove = []
    for i in app['tabs']:
        corresponding_pattern = None
        for pattern in sites_ids:
            if pattern in i.url:
                corresponding_pattern = pattern
                break
        
        if corresponding_pattern is not None and i not in tabs_info:
            print(f'сайт {i.url} закрыт.')
            closed_list.append(LifePeriod(
                start=i.time,
                end=datetime.strptime(
                    data['time'],
                    config['datetime_str_format_js']),
                process_id=sites_ids[corresponding_pattern]
                ))
            to_remove.append(i)
    for i in to_remove:
        app['tabs'].remove(i)
    
    if len(closed_list) > 0:
        app['repo'].record_app_life_periods(closed_list)
            
    for i in tabs_info:
        if i not in app['tabs']:
            app['tabs'].append(i)

    return web.Response(text='ok')

app.add_routes(routes)

cors = aiohttp_cors.setup(app, defaults={
    "*":  aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers="*",
        expose_headers="*",
    )
})

for route in list(app.router.routes()):
    cors.add(route)

if __name__ == '__main__':
    web.run_app(app, port=config['port'])