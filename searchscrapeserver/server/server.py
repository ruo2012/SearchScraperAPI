import asyncio

from aiohttp import web

from searchscrapeserver.scraping.google_scraping import google_gather_results
from searchscrapeserver.scraping.bing_scraping import bing_gather_results
from searchscrapeserver.scraping.yandex_scraping import yandex_gather_results
from searchscrapeserver.scraping.duckduckgo_scraping import ddg_gather_results
from searchscrapeserver.schemas.google_schemas import GoogleSingleItem


class SearchScraper:

    def __init__(self, host, port):

        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except ImportError:
            pass
        self.host = host
        self.port = port
        self.loop = asyncio.get_event_loop()
        self.google_schema = GoogleSingleItem()

    async def scrape_google_single_keyword(self, request):
        data = await request.json()
        input_data, errors = self.google_schema.load(data)
        if errors:
            return web.json_response(errors, status=400)
        results = await google_gather_results(input_data)
        if 'error' in results:
            return web.json_response(results, status=400)
        return web.json_response(results, status=200)

    async def scrape_bing_single_keyword(self, request):
        data = await request.json()
        input_data, errors = self.google_schema.load(data)
        if errors:
            return web.json_response(errors, status=400)
        results = await bing_gather_results(input_data)
        if 'error' in results:
            return web.json_response(results, status=400)
        return web.json_response(results, status=200)

    async def scrape_yandex_single_keyword(self, request):
        data = await request.json()
        input_data, errors = self.google_schema.load(data)
        if errors:
            return web.json_response(errors, status=400)
        results = await yandex_gather_results(input_data)
        if 'error' in results:
            return web.json_response(results, status=400)
        return web.json_response(results, status=200)

    async def scrape_ddg_single_keyword(self, request):
        data = await request.json()
        input_data, errors = self.google_schema.load(data)
        if errors:
            return web.json_response(errors, status=400)
        results = await ddg_gather_results(input_data)
        if 'error' in results:
            return web.json_response(results, status=400)
        return web.json_response(results, status=200)

    def run_server(self):
        app = web.Application(loop=self.loop)
        app.router.add_post('/google-scrape', self.scrape_google_single_keyword)
        app.router.add_post('/bing-scrape', self.scrape_bing_single_keyword)
        app.router.add_post('/yandex-scrape', self.scrape_yandex_single_keyword)
        app.router.add_post('/duckduckgo-scrape', self.scrape_ddg_single_keyword)
        web.run_app(app, host=self.host, port=self.port)
