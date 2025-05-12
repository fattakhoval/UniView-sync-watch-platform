import asyncio
import logging.config
from enum import Enum
from pathlib import Path
from urllib.parse import urlparse

from src.logger.logging_congig import logger_config

from undetected_playwright.tarnished import Malenia
from playwright.async_api import async_playwright, Route, TimeoutError as PlaywrightTimeoutError


logging.config.dictConfig(logger_config)


class ViewMode(str, Enum):
    new = "new"
    headless = "headless"
    headful = "headful"


class Parser:

    class NotFoundVideo(Exception):
        pass

    def __init__(self, search_id, name='WithoutProxy', proxy=None):
        self.playwright = None
        self.browser = None
        self.page = None
        self.context = None
        self.proxy = proxy
        self.start_url = 'about:blank'
        self.timeout = 30000
        self.name = name
        self.logger = logging.getLogger(name=self.name)

        self.search_id = search_id
        self.base_rutube_url = 'https://rutube.ru/video'
        self.master_playlist_url = ''

        self.video_dir = Path('/home/letquare/Work/Individual-project/src/media/download_video')

        self.logger.info(f'Init Parser with name: {self.name}')

    async def launch_browser(self, view_mode: ViewMode = ViewMode.headless):
        import sys
        import asyncio

        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        self.playwright = await async_playwright().start()
        await self._start_browser(view_mode=view_mode)

    async def _hijacker(self, route: Route):
        resource_type = route.request.resource_type
        url = route.request.url

        if resource_type in [ 'images', 'font', 'image']:
            await route.abort()
            return

        if resource_type == 'xhr':
            self.logger.info(f"{route.request.method} - {resource_type} - {url}")
            url_parse = urlparse(url)
            if len(url_parse.query.split('&')) == 5 and self.search_id in url_parse.path:
                self.master_playlist_url = url
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

        if self.proxy:
            launch_args['proxy'] = {**self.proxy}

        self.browser = await self.playwright.firefox.launch(**launch_args)


    async def close_browser(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


    async def worker(self):
        self.logger.info(f"Worker starting")

        await self.page.goto(f"{self.base_rutube_url}/{self.search_id}", timeout=self.timeout)

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

async def main():
    new_parser = Parser('160e059bfada7d99b5fe58ab2db69d65')
    await new_parser.launch_browser(view_mode=ViewMode.headful)
    master_url = (await new_parser.run())

    print(master_url)


if __name__ == '__main__':

    asyncio.run(main())