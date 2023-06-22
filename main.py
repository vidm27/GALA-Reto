import asyncio
from pathlib import Path
from typing import Dict, Any

import aiohttp
import pandas as pd
from loguru import logger


class RateLimitedException(Exception):
    """Rate api limited exception"""


def load_data_from(filename: str, path: str) -> pd.DataFrame:
    base_path = Path(__file__).resolve().parent
    directory = base_path / path
    current_path = directory / filename
    data_file = pd.read_csv(current_path)
    return data_file


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    df_copy = data.copy()
    df_copy[["Participante", "IP"]] = df_copy["Nombre;GDPR IP"].str.split(
        ";", expand=True
    )
    return df_copy


async def fetch_location_participan(ip: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://ip-api.com/json/{ip}") as response:
            logger.debug(f"Status: {response.status}")
            if response.status == 429:
                raise RateLimitedException(f"Could not fetch location this ip: {ip}")

            location = await response.json()
            return location


async def add_location_to_each(records_session: list[Dict]) -> pd.DataFrame:
    waiting_time_request = 20  # seconds
    new_dataframe = pd.DataFrame(columns=["Nombre", "IP", "Pais", "Ciudad", "Region"])
    count = 0
    total_len = len(records_session)
    while len(records_session) > 0:
        ip = records_session[0]["IP"]
        name = records_session[0]["Participante"]
        try:
            location = await fetch_location_participan(ip)
            logger.info(f"Name: {name}, Index:{count} - {location}")
            new_row = {
                "Nombre": name,
                "IP": ip,
                "Pais": location["country"],
                "Ciudad": location["city"],
                "Region": location["regionName"]
            }
            new_dataframe.loc[len(new_dataframe)] = new_row
            count += 1
            records_session.pop(0)  # remove first item
        except RateLimitedException as rt:
            logger.error(rt)
            await asyncio.sleep(waiting_time_request)

        logger.debug(f"Initial len: {total_len}, Current len: {count},  Len DataFrame: {new_dataframe.shape}")
    return new_dataframe


async def main():
    data_virtual_session = load_data_from("Listado_de_participantes_reto_1.csv", 'data')
    data_virtual_session = clean_data(data_virtual_session)
    records_session = data_virtual_session.to_dict(orient="records")
    new_dataframe = await add_location_to_each(records_session)
    new_dataframe.to_excel("./data/output.xlsx", index=False)


if __name__ == "__main__":
    asyncio.run(main())
