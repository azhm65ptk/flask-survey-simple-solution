from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSE=[]

@app.route('/')
def main_page():
    """ Start Page of the customer satisfaction survey"""
    return render_template('survey-start.html',survey=survey)


@app.route('/begin')
def start_survey():
    """when user click start from start page, it comes here and 
    redirecting to Quesiton 0"""
    
    return redirect('/question/0')


@app.route('/question/<int:id>')
def question(id):
    if(len(RESPONSE) is None):
        # trying to access question page too soon
        return redirect('/')
    
    if(len(RESPONSE) == len(survey.questions)):
         # They've answered all the questions! Thank them.
        return render_template('completion.html')
        
    if(len(RESPONSE)  != id):
         # Trying to access questions out of order.
        return redirect(f'/question/{len(RESPONSE)}')


    question=survey.questions[id]
    return render_template('question.html',question=question)


@app.route('/answer',methods=['POST'])
def handle_question():

    # get the response choice, from form> input name='answer'
    choice=request.form['answer']

   
    RESPONSE.append(choice)# appending the answer(choice) to the RESPONSE list

    if (len(RESPONSE)== len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect('/completion')
    
    else:
        return redirect(f'/question/{len(RESPONSE)}')

@app.route('/completion')
def completed():
    """Survey complete. Show completion page."""
    return render_template('completion.html')