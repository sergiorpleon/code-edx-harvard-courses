from flask import redirect, render_template, url_for, flash
from functools import wraps
from app.models import User
from flask_login import current_user

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

"""
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
"""


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user:
                return redirect(url_for('user.login'))  
              
            user = User.query.get(current_user.id)
            if not user.allowed(access_level):
                flash('You do not have access to that page. Sorry!', 'success')
                return redirect(url_for('event.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator



def make_login(self, user, password):
    """
    Call login user. Used in test_auth

    """

    response = self.client.get(url_for('user.login'))
    csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
            
    response = self.client.post('/login', data={
        'csrf_token': csrf_token,
        'name': user,
        'password': password
    }, follow_redirects=True)

    return response
