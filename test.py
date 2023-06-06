from database.database import *
import asyncio

async def abc():
    return await MatchingBeansService.match_beans("23234")

asyncio.run(abc())