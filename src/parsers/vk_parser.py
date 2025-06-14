import asyncio
import logging.config
from enum import Enum
from pprint import pprint
from urllib.parse import urlparse

from src.logger.logging_congig import logger_config

from undetected_playwright.tarnished import Malenia
from playwright.async_api import async_playwright, Route
from aiohttp import ClientSession

logging.config.dictConfig(logger_config)


class ViewMode(str, Enum):
    new = "new"
    headless = "headless"
    headful = "headful"


class ParserVK:

    class NotFoundVideo(Exception):
        pass

    def __init__(self, link, name='ParserVK'):
        self.playwright = None
        self.browser = None
        self.page = None
        self.context = None
        self.start_url = 'about:blank'
        self.timeout = 30000
        self.name = name
        self.logger = logging.getLogger(name=self.name)

        self.link = link
        self.master_playlist_url = ''
        self.cookies = ''

        self.logger.info(f'Init Parser {self.name}')

    async def launch_browser(self, view_mode: ViewMode = ViewMode.headless):
        import sys
        import asyncio

        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        self.playwright = await async_playwright().start()
        await self._start_browser(view_mode=view_mode)

    async def extract_cookies(self):
        cookies_list = await self.context.cookies()
        self.cookies = "; ".join(f"{c['name']}={c['value']}" for c in cookies_list)

    async def _hijacker(self, route: Route):
        resource_type = route.request.resource_type
        url = route.request.url
        if resource_type in [ 'images', 'font', 'image', 'stylesheet']:
            await route.abort()
            return

        if resource_type == 'fetch':
            self.logger.info(f"{route.request.method} - {resource_type} - {url}")
            url_parse = urlparse(url)

            if url_parse.path == '/method/video.getVideoDiscover':
                headers = dict(route.request.headers)
                print(headers)
                method = route.request.method
                post_data = route.request.post_data
                async with ClientSession(headers=headers) as session:
                    async with session.request(
                            method=method,
                            url=url,
                            data=post_data
                    ) as response:

                        json_data = await response.json()
                        files = json_data.get('response').get('current_video').get('files')
                        print("Ответ от video.getVideoDiscover:")
                        self.master_playlist_url = files.get('hls')
                        print(self.master_playlist_url)
                        await route.abort()
                        return

        await route.continue_()

    async def _start_browser(self, view_mode: ViewMode = ViewMode.headless):
        match view_mode:
            case ViewMode.new:
                launch_args = {
                    'args': ["--headless=new", "--dump-dom"]
                }
            case ViewMode.headless:
                launch_args = {
                    'headless': True
                }
            case _:
                launch_args = {
                    'headless': False
                }

        self.browser = await self.playwright.firefox.launch(**launch_args)


    async def close_browser(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def worker(self):
        self.logger.info(f"Worker starting")

        await self.page.goto(self.link, timeout=self.timeout)

        for _ in range(25):
            if self.master_playlist_url:
                return self.master_playlist_url

            await asyncio.sleep(1)

        raise self.NotFoundVideo()

    async def run(self):

        self.context = await self.browser.new_context(locale="en-US")
        await Malenia.apply_stealth(self.context)
        await self.context.route("**/*", self._hijacker)

        self.page = await self.context.new_page()
        try:
            res = await self.worker()

        except self.NotFoundVideo:
            return ''
        else:
            return res
        finally:
            await self.close_browser()
