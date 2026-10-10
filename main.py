from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta
from pathlib import Path
import uuid


# ==========================================
# SETTINGS
# ==========================================

INPUT_FILE = "birthdays.txt"
OUTPUT_FILE = "birthdays_and_anniversaries.ics"

# Year used only as the starting year.
# The event repeats every year.
BASE_YEAR = 2026

# Notification time
REMINDER_HOUR = 7
REMINDER_MINUTE = 0


# ==========================================
# CREATE CALENDAR
# ==========================================

cal = Calendar()

cal.add("prodid", "-//Birthday & Anniversary Reminders//EN")
cal.add("version", "2.0")
cal.add("calscale", "GREGORIAN")
cal.add("X-WR-CALNAME", "Birthdays & Anniversaries")


# ==========================================
# HELPER
# ==========================================

def escape(text):
    return (
        text
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


# ==========================================
# READ FILE
# ==========================================

lines = Path(INPUT_FILE).read_text(
    encoding="utf-8"
).splitlines()


event_count = 0


for line_number, line in enumerate(lines, start=1):

    line = line.strip()

    # Ignore empty lines
    if not line:
        continue

    # Ignore comments
    if line.startswith("#"):
        continue


    # ======================================
    # PARSE
    # ======================================

    try:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) != 3:
            raise ValueError(
                "Expected: Name | DD/MM/YYYY | Region"
            )

        name = parts[0]
        date_text = parts[1]
        region = parts[2]

        birthday = datetime.strptime(
            date_text,
            "%d/%m/%Y"
        )

    except ValueError as e:

        print(
            f"⚠️ Skipping line {line_number}: {line}"
        )

        print(f"   Reason: {e}")

        continue


    # ======================================
    # EVENT TYPE
    # ======================================

    if name.lower().startswith("wedding anniversary"):

        event_title = f"💍 {name}"

        event_description = (
            f"Wedding Anniversary\n"
            f"Region: {region}"
        )

    else:

        event_title = f"🎂 {name}'s Birthday"

        event_description = (
            f"Birthday\n"
            f"Region: {region}"
        )


    # ======================================
    # EVENT DATE + TIME
    # ======================================

    # Birthday/anniversary occurs at 7:00 AM
    start = datetime(
        BASE_YEAR,
        birthday.month,
        birthday.day,
        REMINDER_HOUR,
        REMINDER_MINUTE,
        0
    )

    # Event lasts for 30 minutes
    end = start + timedelta(minutes=30)


    # ======================================
    # CREATE EVENT
    # ======================================

    event = Event()

    event.add(
        "uid",
        str(uuid.uuid4()) + "@birthday-reminder"
    )

    event.add(
        "dtstamp",
        datetime.utcnow()
    )

    event.add(
        "summary",
        escape(event_title)
    )

    event.add(
        "description",
        escape(event_description)
    )

    event.add(
        "dtstart",
        start
    )

    event.add(
        "dtend",
        end
    )

    # Repeat every year
    event.add(
        "rrule",
        {"freq": "yearly"}
    )


    # ======================================
    # NOTIFICATION AT 7:00 AM
    # ======================================

    alarm = Alarm()

    alarm.add(
        "action",
        "DISPLAY"
    )

    alarm.add(
        "description",
        escape(
            f"🎉 Today: {event_title}"
        )
    )

    # Notification occurs when the event starts
    alarm.add(
        "trigger",
        timedelta(seconds=0)
    )

    event.add_component(alarm)


    # ======================================
    # ADD EVENT
    # ======================================

    cal.add_component(event)

    event_count += 1

    print(
        f"✅ Added: {event_title} | "
        f"{region} | 7:00 AM"
    )


# ==========================================
# SAVE
# ==========================================

Path(OUTPUT_FILE).write_bytes(
    cal.to_ical()
)


print()
print("=" * 55)
print("DONE!")
print("=" * 55)
print(f"Created: {OUTPUT_FILE}")
print(f"Total events: {event_count}")
print()
print("Every event repeats yearly at 7:00 AM.")
print("The notification triggers at the event start time.")