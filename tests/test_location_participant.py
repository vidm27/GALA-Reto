import pandas as pd
import pytest

from main import load_data_from, fetch_location_participan, RateLimitedException


def test_load_data_from_path_in_dataframe():
    directory = "data"
    filename = "Listado_de_participantes_reto_1.csv"
    result = load_data_from(filename, directory)
    assert type(result) == pd.DataFrame


@pytest.mark.asyncion
async def test_success_fetch_location_participan():
    ip = "186.104.222.19"
    response_expected = {
        "status": "success",
        "country": "Chile",
        "countryCode": "CL",
        "region": "RM",
        "regionName": "Santiago Metropolitan",
        "city": "Santiago",
        "zip": "34033",
        "lat": -33.4521,
        "lon": -70.6536,
        "timezone": "America/Santiago",
        "isp": "TELEFÓNICA CHILE S.A.",
        "org": "Movistar Fibra",
        "as": "AS7418 TELEFÓNICA CHILE S.A.",
        "query": "186.104.222.19"
    }
    result = await fetch_location_participan(ip)
    assert result == response_expected


@pytest.mark.asyncio
async def test_rate_limited_fetch_location_participan():
    ip = "186.104.222.19"
    with pytest.raises(RateLimitedException) as exc_rt:
        for i in range(100):
            await fetch_location_participan(ip)
