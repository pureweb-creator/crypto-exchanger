import logging
import asyncio
import json
from redis.asyncio import Redis

from bot.utils.load_json import load_json

async def udpate_data(r: Redis):
    while True:
        try:
            currencies = await load_json('currencies.json')
            pairs = await load_json('pairs.json')
            # rates = await load_json('rates.json')



            await r.set('exchange:currencies', json.dumps(currencies))
            await r.set('exchange:pairs', json.dumps(pairs))
            # await r.set('exchange:rates', json.dumps(rates))

            logging.info(f"Data sucessfully refreshed")

        except Exception as e:
            logging.info(f"Failed to refresh data {e}")

        await asyncio.sleep(60*10)
