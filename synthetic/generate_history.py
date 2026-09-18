import datetime
import json
import random
from pathlib import Path

import holidays


SEED = 42
OBSERVATION_COUNT = 8
STAY_DATE_DAYS = 60

PREMIUM_CASH_ADJUSTMENT = 0.25
WEEKEND_CASH_ADJUSTMENT = 0.25
HIGH_DEMAND_CASH_ADJUSTMENT = 0.25
HOLIDAY_CASH_ADJUSTMENT = 0.25

US_HOLIDAYS = holidays.US()


HOTELS = [
    {
        "hotel_id": "SYN001",
        "hotel_name": "Synthetic Regency Chicago",
        "category": 4,
        "base_cash_price": 250,
    },
    {
        "hotel_id": "SYN002",
        "hotel_name": "Synthetic Grand Chicago",
        "category": 6,
        "base_cash_price": 500,
    },
    {
        "hotel_id": "SYN003",
        "hotel_name": "Synthetic Park Chicago",
        "category": 8,
        "base_cash_price": 800,
    },
]


ROOMS = [
    {
        "room_type_id": "STD_KING",
        "room_name": "Standard King",
        "room_class": "standard",
    },
    {
        "room_type_id": "STD_TWO_QUEENS",
        "room_name": "Standard Two Queens",
        "room_class": "standard",
    },
    {
        "room_type_id": "PREMIUM",
        "room_name": "Premium Room",
        "room_class": "premium",
    },
]


POINTS_TIERS = {
    4: {
        "standard": {
            "low": 12000,
            "standard": 18000,
            "high": 24000,
        },
        "premium": {
            "low": 18000,
            "standard": 24000,
            "high": 30000,
        },
    },
    6: {
        "standard": {
            "low": 20000,
            "standard": 30000,
            "high": 40000,
        },
        "premium": {
            "low": 40000,
            "standard": 50000,
            "high": 60000,
        },
    },
    8: {
        "standard": {
            "low": 35000,
            "standard": 55000,
            "high": 75000,
        },
        "premium": {
            "low": 70000,
            "standard": 90000,
            "high": 110000,
        },
    },
}


def generate_observation_dates(reference_date: datetime.date) -> list:
    observation_dates = []

    for week in range(OBSERVATION_COUNT):
        new_date = reference_date - datetime.timedelta(
            weeks=OBSERVATION_COUNT - 1 - week
        )
        observation_dates.append(new_date)

    return observation_dates


def generate_stay_dates(reference_date: datetime.date) -> list:
    stay_dates = []

    for num_day in range(STAY_DATE_DAYS):
        stay_date = reference_date + datetime.timedelta(days=num_day + 1)
        stay_dates.append(stay_date)

    return stay_dates


def determine_demand(stay_date: datetime.date, us_holidays) -> str:
    if stay_date in us_holidays:
        return "high"

    num = random.random()

    if stay_date.weekday() >= 5 and num < 0.5:
        return "high"

    if stay_date.weekday() < 5 and num < 0.1:
        return "high"

    return "normal"


def initial_award_availability(demand: str) -> bool:
    num = random.random()

    if demand == "high":
        return num < 0.25

    if demand == "normal":
        return num < 0.80

    raise ValueError(f"Invalid demand value: {demand}")


def transition_award_availability(
    demand: str,
    previous_availability: bool,
) -> bool:
    num = random.random()

    if demand == "normal":
        if previous_availability:
            return num < 0.85
        return num < 0.50

    if demand == "high":
        if previous_availability:
            return num < 0.40
        return num < 0.15

    raise ValueError(f"Invalid demand value: {demand}")


def generate_point_price(
    category: int,
    room_class: str,
    demand: str,
    award_available: bool,
) -> int | None:
    if not award_available:
        return None

    points_tiers = POINTS_TIERS[category][room_class]
    num = random.random()

    if demand == "normal":
        if num < 0.10:
            return points_tiers["high"]
        if num < 0.60:
            return points_tiers["standard"]
        return points_tiers["low"]

    if demand == "high":
        if num < 0.10:
            return points_tiers["low"]
        if num < 0.50:
            return points_tiers["standard"]
        return points_tiers["high"]

    raise ValueError(f"Invalid demand value: {demand}")


def generate_cash_price(
    base_cash_price: int,
    room_class: str,
    stay_date: datetime.date,
    demand: str,
    us_holidays,
) -> float:
    adjustment = 0

    if room_class == "premium":
        adjustment += PREMIUM_CASH_ADJUSTMENT

    if stay_date.weekday() >= 5:
        adjustment += WEEKEND_CASH_ADJUSTMENT

    if demand == "high":
        adjustment += HIGH_DEMAND_CASH_ADJUSTMENT

    if stay_date in us_holidays:
        adjustment += HOLIDAY_CASH_ADJUSTMENT

    structured_price = base_cash_price * (1 + adjustment)
    variation = random.uniform(-0.05, 0.05)
    final_price = round(structured_price * (1 + variation), 2)

    return final_price


def main():
    random.seed(SEED)

    reference_date = datetime.date(2026, 9, 18)
    observation_dates = generate_observation_dates(reference_date)
    stay_dates = generate_stay_dates(reference_date)

    records = []

    for hotel in HOTELS:
        for stay_date in stay_dates:
            demand = determine_demand(stay_date, US_HOLIDAYS)

            for room in ROOMS:
                previous_availability = None

                for observation_date in observation_dates:
                    if previous_availability is None:
                        award_available = initial_award_availability(demand)
                    else:
                        award_available = transition_award_availability(
                            demand,
                            previous_availability,
                        )

                    points_price = generate_point_price(
                        hotel["category"],
                        room["room_class"],
                        demand,
                        award_available,
                    )

                    cash_price = generate_cash_price(
                        hotel["base_cash_price"],
                        room["room_class"],
                        stay_date,
                        demand,
                        US_HOLIDAYS,
                    )

                    record = {
                        "hotel_id": hotel["hotel_id"],
                        "hotel_name": hotel["hotel_name"],
                        "category": hotel["category"],
                        "room_type_id": room["room_type_id"],
                        "room_name": room["room_name"],
                        "room_class": room["room_class"],
                        "stay_date": stay_date.isoformat(),
                        "observed_at": observation_date.isoformat(),
                        "demand": demand,
                        "award_available": award_available,
                        "points_price": points_price,
                        "cash_price": cash_price,
                        "currency": "USD",
                        "synthetic": True,
                    }

                    records.append(record)
                    previous_availability = award_available

    return records


if __name__ == "__main__":
    records = main()

    output_path = Path("data/synthetic/synthetic_history.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)
