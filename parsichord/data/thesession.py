from typing import TypedDict

import requests

tune_type_to_meter = {
    "jig": "6/8",
    "reel": "4/4",
}


class TuneData(TypedDict):
    tune: int
    setting: int
    name: str
    meter: str
    mode: str
    abc: str


def get_session_tune_data(tune_id: int, version: int = 0) -> TuneData:
    response = requests.get(f"https://thesession.org/tunes/{tune_id}?format=json")
    response.raise_for_status()
    tune_json = response.json()

    name = tune_json["name"]
    ref_number = tune_json["id"]
    tune_type = tune_json["type"]
    key = tune_json["settings"][version]["key"]
    abc = tune_json["settings"][version]["abc"]
    setting = tune_json["settings"][version]["id"]

    return {
        "tune": ref_number,
        "setting": setting,
        "name": name,
        "meter": tune_type_to_meter[tune_type],
        "mode": key,
        "abc": abc.replace("!", "\r\n"),
    }
