
# Brock University Course Scraper

This Selenium-powered web scraper extracts course information from the Brock University Timetables website ([https://brocku.ca/guides-and-timetables/timetables](https://brocku.ca/guides-and-timetables/timetables)) and stores the data in a structured SQLite3 database.

## Features

- **Automated Data Collection:**  Scrapes course details (titles, codes, descriptions, schedules, etc.) directly from the official timetable source.
- **SQLite3 Database:**  Organizes the scraped information in a relational database for efficient querying and analysis.
- **Customizable:**  Easily adapt the scraper to target specific terms, faculties, or course types.
- **Up-to-Date:**  Ensures you have access to the latest course information.
- **Command Line Arguments:** Fine-tune scraping with options like starting department index.

## Installation

1. **Prerequisites:**
   - Python 3.x
   - Selenium WebDriver
   - SQLite3

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/condyl/brock-schedule-web-scraper.git
   ```

3. **Install Dependencies:**
   ```bash
   cd brock-schedule-web-scraper
   pip install selenium
   pip install sqlite3
   ```

4. **Configure:**
    - Optionally modify scraping filters in `scraper.py`.

## Usage

```bash
# Basic Usage: Scrapes all departments starting from the first
python tt-scraper.py 

# Scrape from a specific department index onwards:
python tt-scraper.py 5  # Start from index 5 (0-based)
```

### Available Command Line Arguments:

| Argument        | Description                                                    | Default        |
| --------------- | -------------------------------------------------------------- | ------------- |
| start index | Index of the department to start scraping from.                 | 0             |

## Database Schema

The SQLite3 database includes the following tables (example):

| Table Name     | Columns                                                  | Description                                       |
| -------------- | --------------------------------------------------------- | ------------------------------------------------- |
| course_times        | id, course_code, course_name, course_type, course_days, course_start_time, course_end_time, course_start_date, course_end_date, course_instructor            | Stores basic course information                    |
