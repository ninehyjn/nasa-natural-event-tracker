

import sqlite3

from flask import Flask, render_template, request, redirect, flash
from models import NaturalEvent, EventFetcher

app = Flask(__name__)
app.secret_key = "secret-key"

fetcher = EventFetcher()

def init_db():
    connection = sqlite3.connect("events.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watched_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        eonet_id TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        category TEXT,
        status TEXT,
        latitude REAL,
        longitude REAL,
        event_date TEXT,
        magnitude REAL,
        mag_unit TEXT,
        source_url TEXT,
        note TEXT DEFAULT '',
        alert_active INTEGER DEFAULT 0,
        saved_at TEXT DEFAULT (datetime('now'))
    )    
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT NOT NULL UNIQUE,
        label TEXT NOT NULL
    )
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS search_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_text TEXT,
        searched_at TEXT DEFAULT (datetime('now'))
    )
""")
    
    categories = fetcher.fetch_categories()

    for category in categories:
        cursor.execute("""
        INSERT OR IGNORE INTO categories (
            slug,
            label
    )
    VALUES (?, ?)
""", (
    category["id"],
    category["title"]
))


    connection.commit()
    connection.close()




@app.route("/")
def home():
    return render_template(
        "index.html",
        title = "NASA Natural Events Tracker"
    )

@app.route("/browse")
def browse():
    status = request.args.get("status", "open")
    category = request.args.get("category")
    days = int(request.args.get("days", 30))

    events = fetcher.fetch_events(
        status = status,
        category = category,
        days = days
        )

    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT slug, label
    FROM categories
    """)

    categories = cursor.fetchall()

    cursor.execute("""
    SELECT eonet_id
    FROM watched_events
""")

    watched_ids = [row[0] for row in cursor.fetchall()]

    connection.close()

    return render_template(
        "browse.html",
        events = events,
        categories = categories,
        watched_ids = watched_ids
    )

@app.route("/event/<eonet_id>")
def event_detail(eonet_id):
    event = fetcher.fetch_event(eonet_id)

    return render_template(
        "event_detail.html",
        event = event
    )

@app.route("/watch/add/<eonet_id>", methods=["POST"])
def add_watch(eonet_id):
    event = fetcher.fetch_event(eonet_id)

    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO watched_events (
        eonet_id,
        title,
        category,
        status,
        latitude,
        longitude,
        event_date,
        magnitude,
        mag_unit,
        source_url
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event.eonet_id,
        event.title,
        event.category,
        event.status,
        event.latitude,
        event.longitude,
        event.event_date,
        event.magnitude,
        event.mag_unit,
        event.source_url
    ))

    connection.commit()
    connection.close()

    flash("Event added to watch list!")
    return redirect("/browse")

@app.route("/watchlist")
def watchlist():
    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, title, category, status, event_date, note
    FROM watched_events
""")

    watched_events = cursor.fetchall()
    connection.close()

    return render_template(
        "watchlist.html",
        watched_events = watched_events
    )

@app.route("/watch/remove/<int:id>", methods=["POST"])
def remove_watch(id):
    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM watched_events
    WHERE id = ?
""", (id,))

    connection.commit()
    connection.close()

    flash("Event removed from watch list!")
    return redirect("/watchlist")

@app.route("/watch/note/<int:id>", methods=["GET", "POST"])
def edit_note(id):

    if request.method == "POST":
        note = request.form.get("note", "")

        connection = sqlite3.connect("events.db")
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE watched_events
        SET note = ?
        WHERE id = ?
    """, (note, id))

        connection.commit()
        connection.close()

        flash("Note saved!")
        return redirect("/watchlist")

    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, title, note
    FROM watched_events
    WHERE id = ?
""", (id,))

    event = cursor.fetchone()
    connection.close()

    return render_template(
        "edit_note.html",
        event = event
    )


init_db()

if __name__ =="__main__":
    app.run(debug = True, port = 5001)