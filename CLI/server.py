from aiohttp import web

app = web.Application()
routes = web.RouteTableDef()

@routes.get('/')
async def check_connect_handler(request):
    print(request.match_info)
    return web.Response(text=request.match_info['key'])

app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app)