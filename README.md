# TimeTracker

This TimeTracker is a straightforward terminal-based time tracking tool designed for both personal and professional use. It provides essential features to help you keep track of your activities efficiently.

## Features

### 1. Start/Stop Timer
Initiate a timer to track the duration of your current activity. Stop the timer when you're done.

### 2. Add Entry Manually
Manually log entries by providing details such as name, start time, and elapsed time. This is useful for recording activities not tracked in real-time.

### 3. Timer Names
TimeTracker allows you to assign names to your timers, making it easier to identify and categorize your activities. When starting a timer or adding a manual entry, you can choose from previously stored names or add a new one.

### 4. Browse Entries
View a chronological list of your recorded entries. Each entry displays essential information, including ID, name, start time, and elapsed time.

### 5. Edit Entries
Modify existing entries by updating details such as name, start time, end time, and notes. This feature allows you to refine your recorded data.

### 6. Save in SQLite Using SQLAlchemy
TimeTracker leverages the SQLAlchemy library to store data in an SQLite database, ensuring data integrity and easy retrieval.

## Installation

### Prerequisites
- Python installed on your system
- Pip (Python package installer)
- Install SQLAlchemy:
   ```bash
   python timetracker.py
   ```

## Usage

1. Run the script:
   ```bash
   pip install sqlalchemy
   ```
2. Select options based on your needs:
- Start timer (1)
- Stop timer (2)
- Add entry (3)
- Browse entries (4)
- Edit entry (5)
- Exit (6)
