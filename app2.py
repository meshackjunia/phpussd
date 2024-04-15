from flask import Flask, request
import threading
import time

app = Flask(__name__)

# Sample quiz questions
quiz = [
    {
        'question': 'What is the capital of France?',
        'options': ['1. London', '2. Paris', '3. Berlin', '4. Madrid'],
        'answer': '2'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'options': ['1. Venus', '2. Mars', '3. Jupiter', '4. Saturn'],
        'answer': '2'
    },
    {
        'question': 'Who is the author of "To Kill a Mockingbird"?',
        'options': ['1. Harper Lee', '2. F. Scott Fitzgerald', '3. John Steinbeck', '4. William Faulkner'],
        'answer': '1'
    },
    {
        'question': 'What is the largest ocean on Earth?',
        'options': ['1. Atlantic Ocean', '2. Indian Ocean', '3. Arctic Ocean', '4. Pacific Ocean'],
        'answer': '4'
    },
    {
        'question': 'Which country is famous for the ancient city of Petra?',
        'options': ['1. Egypt', '2. Jordan', '3. Greece', '4. Turkey'],
        'answer': '2'
    }

]

quiz_index = 0
user_answers = []


# Countdown timer function
def countdown(timer):
    while timer:
        mins, secs = divmod(timer, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        timer -= 1
    print('Time is up!')


@app.route('/', methods=['POST'])
def ussd_quiz():
    session_id = request.form.get('sessionId')
    phone_number = request.form.get('phoneNumber')
    text = request.form.get('text')

    response = ""
    global quiz_index
    global user_answers

    if quiz_index < len(quiz):
        current_question = quiz[quiz_index]
        if text == "":
            response = f"CON {current_question['question']}\n{'\n'.join(current_question['options'])}"
            # Start the countdown timer for 30 seconds
            timer = 30
            t = threading.Thread(target=countdown, args=(timer,))
            t.start()
        else:
            user_answers.append(text)
            quiz_index += 1
            if quiz_index < len(quiz):
                next_question = quiz[quiz_index]
                response = f"CON {next_question['question']}\n{'\n'.join(next_question['options'])}"
                # Start the countdown timer for 30 seconds
                timer = 30
                t = threading.Thread(target=countdown, args=(timer,))
                t.start()
            else:
                score = calculate_score()
                response = f"END Quiz completed! Your score is {score}"
    else:
        response = "END Quiz has already been completed. Thank you!"

    return response


def calculate_score():
    score = 0
    for i in range(len(quiz)):
        if user_answers[i] == quiz[i]['answer']:
            score += 1
    return score



if __name__ == '__main__':
    app.run(debug=True)
