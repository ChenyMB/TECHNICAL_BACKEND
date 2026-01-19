import httpx

from .models import Person

BASE_URL = "https://randomuser.me/api/"


def _map_user_to_person(user: dict) -> Person:
    full_name = f"{user['name']['first']} {user['name']['last']}"
    gender = user.get("gender", "")

    location_data = user.get("location", {})
    city = location_data.get("city", "")
    state = location_data.get("state", "")
    country = location_data.get("country", "")
    location = ", ".join([x for x in [city, state, country] if x])

    email = user.get("email", "")
    birth_date = user.get("dob", {}).get("date", "")
    picture_url = user.get("picture", {}).get("large", "")

    return Person(
        full_name=full_name,
        gender=gender,
        location=location,
        email=email,
        birth_date=birth_date,
        picture_url=picture_url,
    )


async def get_people(results: int = 10) -> list[Person]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(BASE_URL, params={"results": results})
            response.raise_for_status()
            payload: dict = response.json()
    except httpx.TimeoutException:
        raise RuntimeError("External service timeout")
    except httpx.RequestError as exc:
        raise RuntimeError(f"External service error: {exc}") from exc

    users = payload.get("results", [])
    return [_map_user_to_person(user) for user in users]

