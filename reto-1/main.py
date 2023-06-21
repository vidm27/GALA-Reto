import asyncio
from pathlib import Path
from typing import Dict, Any

import aiohttp
import pandas as pd
from loguru import logger


class RateLimitedException(Exception):
    """Rate api limited exception"""


def load_data_from(filename: str) -> pd.DataFrame:
    current_path = Path('./data') / filename
    data_file = pd.read_csv(current_path)
    return data_file


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    df_copy = data.copy()
    df_copy[['Participante', 'IP']] = df_copy["Nombre;GDPR IP"].str.split(";", expand=True)
    return df_copy


async def fetch_location_participan(ip: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://ip-api.com/json/{ip}') as response:
            logger.debug(f"Status: {response.status}")
            if response.status == 429:
                raise RateLimitedException("Could not fetch location this ip: {ip}")

            location = await response.json()
            return location



if __name__ == '__main__':
    asyncio.run(main())
