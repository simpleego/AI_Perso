"""3-3. 커스텀 도구: API 키 없는 Open-Meteo 날씨 도구 제작."""

from __future__ import annotations

import requests
from langchain.agents import create_agent
from langchain.tools import tool

from common import get_model, print_final_answer


@tool("current_weather")
def get_current_weather(city: str) -> dict:
    """도시 이름을 받아 현재 기온, 습도, 강수량, 풍속을 조회합니다.

    Args:
        city: 조회할 도시 이름. 예: Seoul, Busan, Daejeon
    """
    city = city.strip()
    if not city:
        return {"error": "도시 이름이 비어 있습니다."}

    try:
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "language": "ko",
                "format": "json",
            },
            timeout=10,
        )
        geo_response.raise_for_status()
        candidates = geo_response.json().get("results", [])
        if not candidates:
            return {"error": f"'{city}'의 위치를 찾지 못했습니다."}

        place = candidates[0]
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "precipitation,wind_speed_10m"
                ),
                "timezone": "auto",
            },
            timeout=10,
        )
        weather_response.raise_for_status()
        current = weather_response.json()["current"]

        return {
            "city": place["name"],
            "country": place.get("country", ""),
            "observed_at": current["time"],
            "temperature_c": current["temperature_2m"],
            "humidity_percent": current["relative_humidity_2m"],
            "precipitation_mm": current["precipitation"],
            "wind_speed_kmh": current["wind_speed_10m"],
        }
    except requests.RequestException as exc:
        return {"error": f"날씨 서버 요청 실패: {exc}"}
    except (KeyError, TypeError, ValueError) as exc:
        return {"error": f"날씨 데이터 처리 실패: {exc}"}


@tool
def recommend_activity(
    temperature_c: float,
    precipitation_mm: float,
    wind_speed_kmh: float,
) -> str:
    """날씨 수치를 바탕으로 간단한 야외 활동 여부를 판단합니다."""
    if precipitation_mm > 0:
        return "비가 오므로 실내 활동을 권장합니다."
    if wind_speed_kmh >= 30:
        return "바람이 강하므로 야외 활동에 주의하세요."
    if 10 <= temperature_c <= 28:
        return "비가 없고 기온이 적당하여 야외 활동에 좋습니다."
    return "기온이 쾌적 범위를 벗어나므로 복장을 조절하세요."


def main() -> None:
    agent = create_agent(
        model=get_model(),
        tools=[get_current_weather, recommend_activity],
        system_prompt=(
            "당신은 날씨 활동 도우미입니다. 먼저 current_weather로 "
            "현재 날씨를 조회하고, 반환된 수치를 recommend_activity에 "
            "전달하세요. 도구를 사용하지 않고 날씨를 추측하면 안 됩니다."
        ),
    )

    city = input("날씨를 조회할 도시(기본값: Seoul): ").strip() or "Seoul"
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"{city}의 현재 날씨와 야외 활동 가능 여부를 알려줘.",
                }
            ]
        }
    )
    print_final_answer(result)


if __name__ == "__main__":
    main()

