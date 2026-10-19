"""Handles saving and loading quiz history."""

import json
import os
from datetime import datetime

HISTORY_FILE = "quiz_history.json"

def save_result(score, total):
    """Append a quiz result to the history file."""

    history = load_history()
    percentage = round((score / total) * 100, 2)

    history.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "total": total,
        "percentage": percentage
    })

    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
        print(f"\nResults saved to {HISTORY_FILE}")
    except OSError as e:
        print(f"\nCould not save results: {e}")

    return percentage

def load_history():
    """Return list of past quiz results."""

    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return []

def print_history():
    """Print the last 5 quiz results."""

    history = load_history()

    if not history:
        print("\nNo quiz history found. Play the quiz first.")
        return

    print("\n" + "=" * 60)
    print("QUIZ HISTORY (last 5)")
    print("=" * 60)

    for entry in history[-5:]:
        print(f" {entry['date']} | {entry['score'] / entry['total']} "
              f"{entry['percentage']}%")

    avg = sum(e['percentage'] for e in history) / len(history)

    print(f"\nAttempts: {len(history)} | Average score: {avg:.2f}%")