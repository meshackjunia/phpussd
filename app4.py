from flask import Flask, request
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
        'question': 'Who wrote the novel "To Kill a Mockingbird"?',
        'options': ['1. Harper Lee', '2. Ernest Hemingway', '3. Jane Austen', '4. Mark Twain'],
        'answer': '1'
    },
    {
        'question': 'What is the largest ocean on Earth?',
        'options': ['1. Atlantic Ocean', '2. Indian Ocean', '3. Arctic Ocean', '4. Pacific Ocean'],
        'answer': '4'
    },
    {
        'question': 'What is the chemical symbol for gold?',
        'options': ['1. Au', '2. Ag', '3. Cu', '4. Pb'],
        'answer': '1'
    }
]

quiz_index = 0
user_score = 0
quiz_start_time = None
quiz_duration = 60  # 60 seconds

def display_next_question():
    global quiz_index
    if quiz_index < len(quiz):
        current_question = quiz[quiz_index]
        options_text = "\n".join(current_question['options'])
        return f"CON {current_question['question']}\n{options_text}\nTime remaining: {max(0, quiz_duration - (time.time() - quiz_start_time)):.0f} seconds"
    else:
        return f"END Quiz completed! Your final score is {user_score}/{len(quiz)}"

def handle_quiz_response(text):
    global user_score
    global quiz_index

    if text.isdigit() and 1 <= int(text) <= len(quiz[quiz_index]['options']):
        # User answered a question
        correct_answer = quiz[quiz_index]['answer']
        user_option = int(text)

        if str(user_option) == correct_answer:
            user_score += 1
            return "CON Correct!"
        else:
            return f"CON Incorrect! The correct answer is {quiz[quiz_index]['options'][int(correct_answer) - 1].split('.')[1]}"
    else:
        # User input is not a valid option
        return "CON Invalid option. Please enter a number between 1 and the number of options."

@app.route('/', methods=['POST'])
def ussd_quiz():
    global quiz_index
    global user_score
    global quiz_start_time

    session_id = request.form.get('sessionId')
    phone_number = request.form.get('phoneNumber')
    text = request.form.get('text')

    response = ""

    if text == "":
        # Start the quiz
        quiz_start_time = time.time()
        response = "CON Start the quiz?\n1. Yes\n2. No"
    elif text == "1":
        # Start quiz
        response = display_next_question()
    elif text == "2":
        # Leave
        response = "END Thank you for using the USSD quiz app."
    else:
        # User answered a question
        response = handle_quiz_response(text)

    return response

if __name__ == '__main__':
    app.run(debug=True)