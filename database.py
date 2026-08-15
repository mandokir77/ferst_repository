"""Работа с CSV-базой: показания счётчиков и тарифы."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DATA_DIR = Path(__file__).parent / "data"
READINGS_FILE = DATA_DIR / "readings.csv"
TARIFFS_FILE = DATA_DIR / "tariffs.csv"

READINGS_COLUMNS = ["ХВС", "ГВС", "электричество", "водоотведение", "месяц", "итог"]
TARIFFS_COLUMNS = ["ХВС", "ГВС", "электричество", "водоотведение"]


@dataclass
class Tariffs:
    hvs: float
    gvs: float
    electricity: float
    water_disposal: float


@dataclass
class Reading:
    hvs: float
    gvs: float
    electricity: float
    water_disposal: float | None
    month: str
    total: float | None


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _init_file(path: Path, columns: list[str]) -> None:
    if not path.exists():
        with path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()


def init_database() -> None:
    """Создаёт файлы БД с заголовками, если их ещё нет."""
    _ensure_data_dir()
    _init_file(READINGS_FILE, READINGS_COLUMNS)
    _init_file(TARIFFS_FILE, TARIFFS_COLUMNS)


def _parse_float(value: str, field_name: str) -> float:
    cleaned = value.strip().replace(",", ".")
    try:
        return float(cleaned)
    except ValueError as exc:
        raise ValueError(f"Некорректное число в поле «{field_name}»: {value!r}") from exc


def set_tariffs(raw: str) -> Tariffs:
    """
    Внесение тарифов одной строкой через точку с запятой:
    ХВС;ГВС;электричество;водоотведение
    """
    init_database()
    parts = [part.strip() for part in raw.split(";")]
    if len(parts) != 4:
        raise ValueError(
            "Ожидается 4 значения через точку с запятой: "
            "ХВС;ГВС;электричество;водоотведение"
        )

    tariffs = Tariffs(
        hvs=_parse_float(parts[0], "ХВС"),
        gvs=_parse_float(parts[1], "ГВС"),
        electricity=_parse_float(parts[2], "электричество"),
        water_disposal=_parse_float(parts[3], "водоотведение"),
    )

    with TARIFFS_FILE.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=TARIFFS_COLUMNS)
        writer.writeheader()
        writer.writerow(
            {
                "ХВС": tariffs.hvs,
                "ГВС": tariffs.gvs,
                "электричество": tariffs.electricity,
                "водоотведение": tariffs.water_disposal,
            }
        )

    return tariffs


def get_tariffs() -> Tariffs:
    init_database()
    with TARIFFS_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError("Тарифы не заданы. Сначала внесите тарифы.")

    row = rows[-1]
    return Tariffs(
        hvs=float(row["ХВС"]),
        gvs=float(row["ГВС"]),
        electricity=float(row["электричество"]),
        water_disposal=float(row["водоотведение"]),
    )


def _row_to_reading(row: dict[str, str]) -> Reading:
    total_raw = row.get("итог", "").strip()
    disposal_raw = row.get("водоотведение", "").strip()
    return Reading(
        hvs=float(row["ХВС"]),
        gvs=float(row["ГВС"]),
        electricity=float(row["электричество"]),
        water_disposal=float(disposal_raw) if disposal_raw else None,
        month=row["месяц"],
        total=float(total_raw) if total_raw else None,
    )


def _load_readings() -> list[Reading]:
    init_database()
    with READINGS_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    return [_row_to_reading(row) for row in rows]


def _save_readings(readings: Iterable[Reading]) -> None:
    with READINGS_FILE.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=READINGS_COLUMNS)
        writer.writeheader()
        for reading in readings:
            writer.writerow(
                {
                    "ХВС": reading.hvs,
                    "ГВС": reading.gvs,
                    "электричество": reading.electricity,
                    "водоотведение": "" if reading.water_disposal is None else reading.water_disposal,
                    "месяц": reading.month,
                    "итог": "" if reading.total is None else reading.total,
                }
            )


def add_readings(raw: str) -> Reading:
    """
    Внесение показаний через запятую:
    ХВС, ГВС, электричество, месяц
    """
    parts = [part.strip() for part in raw.split(",")]
    if len(parts) != 4:
        raise ValueError(
            "Ожидается 4 значения через запятую: ХВС, ГВС, электричество, месяц"
        )

    reading = Reading(
        hvs=_parse_float(parts[0], "ХВС"),
        gvs=_parse_float(parts[1], "ГВС"),
        electricity=_parse_float(parts[2], "электричество"),
        water_disposal=None,
        month=parts[3],
        total=None,
    )

    readings = _load_readings()
    if any(item.month == reading.month for item in readings):
        raise ValueError(f"Показания за месяц «{reading.month}» уже существуют.")

    readings.append(reading)
    _save_readings(readings)
    return reading


def calculate_total(month: str | None = None) -> tuple[Reading, float]:
    """
    Рассчитывает и сохраняет водоотведение и итог для указанного месяца
    или для последней записи без итога.
    """
    readings = _load_readings()
    if not readings:
        raise ValueError("Нет показаний для расчёта.")

    tariffs = get_tariffs()

    if month is None:
        target_index = None
        for index in range(len(readings) - 1, -1, -1):
            if readings[index].total is None:
                target_index = index
                break
        if target_index is None:
            target_index = len(readings) - 1
    else:
        target_index = next(
            (index for index, item in enumerate(readings) if item.month == month),
            None,
        )
        if target_index is None:
            raise ValueError(f"Месяц «{month}» не найден в показаниях.")

    if target_index == 0:
        raise ValueError(
            "Для расчёта нужны показания предыдущего месяца. "
            "Это первая запись в базе."
        )

    current = readings[target_index]
    previous = readings[target_index - 1]

    hvs_diff = current.hvs - previous.hvs
    gvs_diff = current.gvs - previous.gvs
    electricity_diff = current.electricity - previous.electricity

    if hvs_diff < 0 or gvs_diff < 0 or electricity_diff < 0:
        raise ValueError(
            "Текущие показания меньше предыдущих. Проверьте введённые значения."
        )

    hvs_cost = hvs_diff * tariffs.hvs
    gvs_cost = gvs_diff * tariffs.gvs
    disposal_volume = hvs_diff + gvs_diff
    disposal_cost = disposal_volume * tariffs.water_disposal
    electricity_cost = electricity_diff * tariffs.electricity

    total = hvs_cost + gvs_cost + disposal_cost + electricity_cost

    current.water_disposal = round(disposal_volume, 3)
    current.total = round(total, 2)

    readings[target_index] = current
    _save_readings(readings)

    return current, total


def format_readings_table() -> str:
    """Форматирует таблицу показаний для вывода на экран."""
    readings = _load_readings()
    if not readings:
        return "Таблица «показания» пуста."

    headers = READINGS_COLUMNS
    rows: list[list[str]] = []
    for reading in readings:
        rows.append(
            [
                f"{reading.hvs:g}",
                f"{reading.gvs:g}",
                f"{reading.electricity:g}",
                "" if reading.water_disposal is None else f"{reading.water_disposal:g}",
                reading.month,
                "" if reading.total is None else f"{reading.total:.2f}",
            ]
        )

    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def format_row(values: list[str]) -> str:
        return " | ".join(value.ljust(widths[index]) for index, value in enumerate(values))

    separator = "-+-".join("-" * width for width in widths)
    lines = [format_row(headers), separator]
    lines.extend(format_row(row) for row in rows)
    return "\n".join(lines)
