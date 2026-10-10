# Birthday & Anniversary Calendar Adder

Generate an `.ics` calendar file with yearly birthday and wedding-anniversary reminders.

This project was made a few months ago with AI doing most of the building, plus a few brain cells of mine providing the ideas and direction.

## What it does

- Reads birthdays and wedding anniversaries from `birthdays.txt`.
- Creates yearly recurring calendar events at 7:00 AM.
- Adds a notification at the start of each event.
- Writes the calendar to `birthdays_and_anniversaries.ics`.
- Skips blank lines and lines beginning with `#`; reports and skips entries that do not match the expected format.

## Requirements

- Python 3
- The `icalendar` package

Install the dependency from the project folder:

```bash
python -m pip install -r requirements.txt
```

## Add your dates

Open `birthdays.txt` and add one entry per line in this format:

```text
Name | DD/MM/YYYY | Region
```

For example:

```text
Alex | 14/02/1995 | California
Wedding Anniversary - Sam and Lee | 20/08/2018 | Ontario
```

The date is used to determine the month and day of the yearly event. The year in the input is not used for recurrence. Entries whose names start with `Wedding Anniversary` (case-insensitive) are treated as anniversaries; other entries are treated as birthdays.

## Generate the calendar

Run the script from the project folder:

```bash
python main.py
```

The script creates `birthdays_and_anniversaries.ics` in the same folder. Import that file into a calendar app that supports `.ics` files. If you change the input data and run the script again, import the newly generated file.

## Settings

You can adjust the starting year, reminder time, and input/output filenames near the top of `main.py`:

- `BASE_YEAR`
- `REMINDER_HOUR`
- `REMINDER_MINUTE`
- `INPUT_FILE`
- `OUTPUT_FILE`

The reminder uses the calendar application's local time zone for the event time.

---

This README was written by AI.

--- 
This is being or was used to help my dad who want a small help in remembering birthdays so i thought of using ai thats why 

its fully ai gen but this msg is not but like i am lazy af so you know the drill.

Next time i will do all by hand other than the publishing to the github bc i am lazy af
