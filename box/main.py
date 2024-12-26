#!/usr/bin/env python3

import sqlite3

from loguru import logger


def main() -> None:
    data = {"drone_id": "drone_01", "battery_level": 75, "status": "ready"}

    connection = sqlite3.connect("journal.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drones (
        id TEXT PRIMARY KEY,
        battery_level INTEGER
    )
    """)

    cursor.execute(
        """INSERT INTO devices (id, battery_level) VALUES (?, ?)""",
        (data["drone_id"], data["battery_level"]),
    )

    connection.commit()
    connection.close()

    logger.info(f"Battery level {data["battery_level"]}")
    if data["battery_level"] < 50:
        logger.warning("Charging is required")
    else:
        logger.success("Battery can be used!")


if __name__ == "__main__":
    main()
