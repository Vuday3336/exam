# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Sample questions - in real app, you might load these from a database
QUESTIONS = [
    {
        "id": 1,
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct_answer": "Paris"
    },
    {
        "id": 2,
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": "4"
    },

    
    # Add more questions here
    {
        "id": 3,
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct_answer": "Paris"
    }
]

@app.route('/api/questions', methods=['GET'])
def get_questions():
    return jsonify(QUESTIONS)

@app.route('/api/submit', methods=['POST'])
def submit_exam():
    data = request.json
    student_name = data.get('student_name')
    answers = data.get('answers')
    
    # Calculate score
    score = 0
    results = []
    for q in QUESTIONS:
        student_answer = answers.get(str(q['id']))
        is_correct = student_answer == q['correct_answer']
        if is_correct:
            score += 1
        results.append({
            'question': q['question'],
            'student_answer': student_answer,
            'correct_answer': q['correct_answer'],
            'is_correct': is_correct
        })
    
    # Create results dictionary
    result_data = {
        'student_name': [student_name],
        'score': [score],
        'total_questions': [len(QUESTIONS)],
        'percentage': [round((score/len(QUESTIONS))*100, 2)],
        'date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }
    
    # Save to Excel
    df = pd.DataFrame(result_data)
    excel_file = 'exam_results.xlsx'
    
    if os.path.exists(excel_file):
        existing_df = pd.read_excel(excel_file)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_excel(excel_file, index=False)
    
    return jsonify({
        'score': score,
        'total': len(QUESTIONS),
        'percentage': round((score/len(QUESTIONS))*100, 2),
        'results': results
    })

if __name__ == '__main__':
    app.run(debug=True)