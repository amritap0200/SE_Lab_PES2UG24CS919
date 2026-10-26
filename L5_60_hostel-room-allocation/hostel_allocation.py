"""Hostel room allocation with a small Flask room lookup portal."""
import os
import secrets
import yaml
from flask import Flask, request
from markupsafe import escape

# Global hostel state
rooms = {}
allocations = {}
waitlist = []
app = Flask(__name__)
_RNG = secrets.SystemRandom()

CONFIG = """
blocks:
  A: {gender: M, rooms: 3, capacity: 2, fee: 4000}
  B: {gender: F, rooms: 2, capacity: 3, fee: 3500}
"""


def load_config(text=CONFIG):
    """Parse the YAML block config and create the rooms."""
    config = yaml.safe_load(text)
    for block, info in config["blocks"].items():
        for n in range(1, info["rooms"] + 1):
            rooms[block + str(n)] = {
                "gender": info["gender"],
                "capacity": info["capacity"],
                "fee": info["fee"],
                "occupants": [],
            }
    return config


def allocate_room(student_id, name, gender, year, preferred=None):
    """Give a student a free room in a matching gender block.

    Returns the room number, or None if the year is invalid or the
    student had to go on the waitlist.
    """
    if not isinstance(year, int):
        return None
    if student_id in allocations:
        return allocations[student_id]["room"]
    candidates = [r for r in (preferred or []) if r in rooms] + list(rooms)
    for room_no in candidates:
        room = rooms[room_no]
        if room["gender"] != gender:
            continue
        if len(room["occupants"]) >= room["capacity"]:
            continue
        room["occupants"].append(student_id)
        allocations[student_id] = {"name": name, "room": room_no, "year": year}
        return room_no
    waitlist.append(student_id)
    return None


def vacate_room(student_id):
    """Remove a student from their room and from the allocations."""
    record = allocations.pop(student_id, None)
    if record is not None:
        rooms[record["room"]]["occupants"].remove(student_id)


def monthly_fee(student_id, days_stayed):
    """Return the fee for the full months a student has stayed."""
    room = rooms[allocations[student_id]["room"]]
    months = days_stayed // 30
    return months * room["fee"]


def priority_order(students):
    """Sort students so the most senior year comes first."""
    return sorted(students, key=lambda s: s["year"], reverse=True)


def room_lottery(student_ids):
    """Return the student ids in a random order."""
    return _RNG.sample(student_ids, len(student_ids))


def vacant_beds():
    """Count every free bed across all rooms."""
    total = 0
    for room in rooms.values():
        total += room["capacity"] - len(room["occupants"])
    return total


def connect_warden_db():
    """Open the warden database using a password from the environment."""
    password = os.environ.get("WARDEN_DB_PASSWORD", "")
    return sqlite_connect(host="localhost", user="warden", password=password)


def sqlite_connect(host, user, password):
    """Return a stub connection record for the warden database."""
    return {"host": host, "user": user, "connected": len(password) > 0}


@app.route("/room")
def room_lookup():
    """Show the room for the student id given in the query string."""
    student_id = request.args.get("id", "")
    room = escape(str(allocations.get(student_id)))
    return f"<h1>Room for {escape(student_id)}: {room}</h1>"


def run_portal():
    """Start the Flask portal with the debugger switched off."""
    app.run(debug=False)


def main():
    """Run a small demo of the allocation system."""
    load_config()
    print("Rooms:", list(rooms.keys()))
    print("S1 ->", allocate_room("S1", "Arjun", "M", 1))
    print("S2 ->", allocate_room("S2", "Kabir", "M", 2))
    print("S3 ->", allocate_room("S3", "Rohan", "M", 3))
    print("S4 (female) ->", allocate_room("S4", "Diya", "F", 1))
    print("S1 again ->", allocate_room("S1", "Arjun", "M", 1))
    print("S5 year '2' ->", allocate_room("S5", "Vikram", "M", "2"))
    print("Occupants of A1:", rooms["A1"]["occupants"])
    vacate_room("S2")
    print("Occupants of A1 after S2 left:", rooms["A1"]["occupants"])
    print("Fee for S1, 45 days:", monthly_fee("S1", 45))
    seniors_first = priority_order([{"year": 1}, {"year": 4}, {"year": 2}])
    print("Priority (seniors first):", [s["year"] for s in seniors_first])
    print("Lottery:", room_lottery(["S6", "S7", "S8"]))
    print("Vacant beds:", vacant_beds())
    print("Warden DB:", connect_warden_db())
    print("Waitlist:", waitlist)


if __name__ == "__main__":
    main()
