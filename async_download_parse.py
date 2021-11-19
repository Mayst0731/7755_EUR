import aiohttp
import asyncio

import bs4


async def fetch(session, url):
    async with session.get(url) as response:
        source = await response.content
        page = bs4.BeautifulSoup(source, 'html.parser')
        return page


async def fetch_all(session, courses, loop):
    results = await asyncio.gather(
        *[fetch(session, course['url']) for course in courses],
        return_exceptions=True  # default is false, that would raise
    )
    # for testing purposes only
    # gather returns results in the order of coros
    for idx, course in enumerate(courses):
        print('{}: {}'.format(course["name"], 'ERR' if isinstance(results[idx], Exception) else 'OK'))
    return results


