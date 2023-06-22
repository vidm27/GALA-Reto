from pathlib import Path
from typing import Dict

import pandas as pd
import pytest

from main import load_data_from, fetch_location_participan, add_location_to_each, RateLimitedException


@pytest.fixture(scope="function")
def data_participant_to_test() -> list[Dict]:
    base_path = Path(__file__).resolve().parent
    current_path = base_path / "data/participante_test.csv"
    data_participant = pd.read_csv(current_path)
    del data_participant['Nombre;GDPR IP']
    return data_participant.to_dict(orient="records")


@pytest.fixture(scope="function")
def data_ip_to_test() -> pd.DataFrame:
    data_ip = pd.read_csv('./data/ip_test.csv')
    return data_ip


def test_load_data_from_path_in_dataframe():
    directory = "data"
    filename = "Listado_de_participantes_reto_1.csv"
    result = load_data_from(filename, directory)
    assert type(result) == pd.DataFrame


@pytest.mark.asyncio
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
async def test_rate_limited_fetch_location_participan(data_ip_to_test):
    with pytest.raises(RateLimitedException) as exc_rt:
        for i, row in data_ip_to_test.iterrows():
            await fetch_location_participan(row["IP"])


@pytest.mark.asyncio
async def test_add_location_to_participan(data_participant_to_test):
    expected = [{"Nombre": "Participante 1", "IP": "170.82.191.157", "Pais": "Chile", "Ciudad": "Melipilla",
                 "Region": "Santiago Metropolitan"},
                {"Nombre": "Participante 2", "IP": "186.154.124.90", "Pais": "Colombia", "Ciudad": "Bogotá",
                 "Region": "Bogota D.C."},
                {"Nombre": "Participante 3", "IP": "186.158.132.184", "Pais": "Argentina",
                 "Ciudad": "Vicente Lopez", "Region": "Buenos Aires"},
                {"Nombre": "Participante 4", "IP": "201.227.20.124", "Pais": "Panama", "Ciudad": "Panama City",
                 "Region": "Provincia de Panama"},
                {"Nombre": "Participante 5", "IP": "201.227.20.124", "Pais": "Panama", "Ciudad": "Panama City",
                 "Region": "Provincia de Panama"}]
    result = await add_location_to_each(data_participant_to_test)
    assert result.to_dict(orient="records") == expected
