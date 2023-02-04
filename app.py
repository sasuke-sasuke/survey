from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chickens'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def index():
    return render_template('index.html', survey=satisfaction_survey)

@app.route('/start', methods=["POST"])
def start_question():
    return redirect('/questions/0')

@app.route('/questions/<int:idx>')
def get_question(idx):
    if len(responses) != idx:
        flash('Cannot access invalid question...')
        return redirect(f'/questions/{len(responses)}')
    question = satisfaction_survey.questions[idx]
    return render_template('questions.html', idx=idx, question=question)

@app.route('/answers', methods=['POST'])
def store_answers():
    responses.append(request.form['answers'])
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thanks')
    return redirect(f'/questions/{len(responses)}')

@app.route('/thanks')
def thank_you():
    return render_template('thanks.html')