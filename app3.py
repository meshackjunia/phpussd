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
        return f"CON {current_question['question']}\n{'\n'.join(current_question['options'])}\nTime remaining: {max(0, quiz_duration - (time.time() - quiz_start_time)):.0f} seconds"
    else:
        return f"END Quiz completed! Your score is {user_score}/{len(quiz)}"

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
        correct_answer = quiz[quiz_index]['answer']
        correct_option_index = int(correct_answer) - 1
        print(f"User's input: {text.strip()}")
        print(f"Correct answer: {correct_answer}")
        print(f"Correct option index: {correct_option_index}")
        if text.strip() == correct_answer:
            user_score += 1
            response = "CON Correct!"
        else:
            response = f"CON Incorrect! The correct answer is {quiz[quiz_index]['options'][correct_option_index].split('.')[1]}"
        quiz_index += 1
        response += display_next_question()
        if quiz_index == len(quiz):
            response = f"END Quiz completed! Your score is {user_score}/{len(quiz)}"

    return response


if __name__ == '__main__':
    app.run(debug=True)
