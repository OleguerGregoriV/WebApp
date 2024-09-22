
from flask import redirect, render_template, session
from functools import wraps


def error_message(message):
    """Render message as an apology to user."""

    return render_template("error.html", message=message)



