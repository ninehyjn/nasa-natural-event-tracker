# NASA Natural Events Tracker

NASA Natural Events Tracker is a Flask web application that uses NASA's EONET API to display real-world natural events. Users can browse live events, filter them by status, category, and number of days, vies detailed event information, and save selected events to a personal watch list stored in SQLite.

## Features

- Browse live natural events from the NASA EONET API
- Filter events by status, category, and number of days
- Views detailed information about an event
- Add events to a watch list
- Remove events from the watch list
- Add and edit personal notes
- Flash messages for user actions

## Setup and Run

1. Create a virtual environment:
   python -m venv .venv

2. Activate the virtual environment.
   On macOS/Linux:
   source .venv/bin/activate

3. Install the required packages:
   pip install -r requirments.txt

4. Run the Flask application:
   flask run

5. Open the application in a browser:
   http://127.0.0.1:5000

## Requirements

The required Python packages are listed in 'requirments.txt'.

Main dependencies:
- Flask
- requests

## OOP Design

The project uses three main classes in 'models.py'

- NaturlalEvent represents an event received from the NASA EONET API. It stores information such as the evnet ID, title, category, status, coordinates, date, magnitude, and source URL.
- WatchedEvent inherits from 'NaturalEvent' and adds a personal note and an alert status.
- EventFetcher handles requests to the NASA EONET API and converts API response data into 'NaturalEvent' objects.

The 'eonet_id' attribute in 'NaturalEvent' uses encapsulation with a private attribute and a property.

## Known Limitations

- Some optional features from Groups C, D and E were not fully implemented because they were excluded from the revised required scope.
- The application depends on the NASA EONET API being available.
- Some EONET events may not provide magnitude information.

## AI Usage

AI tools were used as a development aid for explanations, debugging, and guidance during this project. I reviewed and tested the code and can explain the implementation used in the submission.
