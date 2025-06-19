from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    max_attempts = 10

    # Initialize the game on first visit
    if 'secret_number' not in session:
        session['secret_number'] = random.randint(1, 100)
        session['attempts'] = 0

    message = ""
    guess = None

    if request.method == 'POST':
        try:
            guess = int(request.form['guess'])
            session['attempts'] += 1

            # Game logic
            if guess < 1 or guess > 100:
                message = "Guess must be between 1 and 100."
            elif guess == session['secret_number']:
                message = f"🎉 Correct! You won in {session['attempts']} attempts."
                session.clear()  # Reset game for the winner
            elif session['attempts'] == max_attempts:
                message = f"😢 Out of attempts! The number was {session['secret_number']}."
                session.clear()
            elif guess < session['secret_number']:
                message = "Too low!"
            elif guess > session['secret_number']:
                message = "Too high!"

        except ValueError:
            message = "Please enter a valid integer between 1 and 100."

    attempts_left = max_attempts - session.get('attempts', 0)
    return render_template('index.html', message=message, attempts_left=attempts_left)
