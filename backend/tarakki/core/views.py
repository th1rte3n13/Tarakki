import random
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from .forms import SignInForm, SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User, StudentProfile
import os
import csv
import logging
logger = logging.getLogger(__name__)

import plotly.express as px
from datetime import datetime, timedelta
# Create your views here.
def home(request):
    return render(request,"landing/home.html")


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'landing/signin.html', {'error': 'Invalid email format'})
        
        # Check if user exists
        if not User.objects.filter(email=email).exists():
            return render(request, 'landing/signin.html', {'error': 'No account found with this email'})
        
        # Attempt authentication
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dash')  # Redirect to a home or dashboard page
        else:
            # At this point, the user exists but the password is wrong
            return render(request, 'landing/signin.html', {'error': 'Incorrect password'})
    
    return render(request, 'landing/signin.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()
            # Optionally, create a student profile with additional data
            StudentProfile.objects.create(user=user)
            # Log the user in
            login(request, user)
            return redirect('home')  # Redirect to a home or dashboard page
        else:
            print("Form errors:", form.errors)  # Print form errors for debugging
    else:
        form = SignUpForm()
    return render(request, 'landing/signup.html', {'form': form})

# @login_required(login_url='/signin')
def dashboard_home(request):
    # Generate random data using plain Python
    days = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(30)]
    temperatures = [random.randint(20, 35) for _ in range(30)]

# Create the line chart
    fig = px.line(
        x=days,
        y=temperatures,
        title="Random Temperature Data over 30 Days",
        labels={"x": "Date", "y": "Temperature (°C)"}
    )
    chart = fig.to_html(full_html=False, default_height=500, default_width=700)
    context = {'chart': chart}
    return render(request, 'dashboard/dash-home.html',context)

def dashboard_roadmap(request):
    context = {'items':[
    {
        'title': 'Alpha Corp',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla fermentum, turpis ac vestibulum aliquam, lacus felis.'
    },
    {
        'title': 'Beta LLC',
        'description': 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip.'
    },
    {
        'title': 'Gamma Inc',
        'description': 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident.'
    },
    {
        'title': 'Gamma Inc',
        'description': 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident.'
    },
    {
        'title': 'Gamma Inc',
        'description': 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident.'
    }
]
}
    return render(request, 'dashboard/dash-roadmap.html',context)

def dashboard_settings(request):
    return render(request, 'dashboard/settings.html')


# def dashboard_test(request):
#     context = {'greeting':'Hello, World!'}
#     return render(request, 'dashboard/dash-test.html',context)













def load_questions():
    # Dictionary to store questions by parameter
    questions_by_param = {}

    # Path to the CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), 'your_data_2.csv')  # Adjust path if needed
    
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            param = row['parameter']
            if param not in questions_by_param:
                questions_by_param[param] = []
            questions_by_param[param].append({
                'parameter': param,
                'question_text': row['question_text'],
                'option_a': row['A'],
                'option_b': row['B'],
                'option_c': row['C'],
                'option_d': row['D'],
                'correct_option': row['correct_option']
            })

    # Select 10 random questions for each parameter
    selected_questions = []
    for param, questions in questions_by_param.items():
        selected_questions.extend(random.sample(questions, min(10, len(questions))))

    return selected_questions

def calculate_score(answers, correct_options, options):
    logger.info(f'Answers: {answers}, Correct Options: {correct_options}, Options: {options}')
    
    if any(not validate_option(answer) for answer in answers) or not validate_option(correct_options[0]):
        logger.error(f'Invalid option detected - Answers: {answers}, Correct Options: {correct_options}')
        raise ValidationError('Invalid answer or correct option')

    total_score = 0
    if options == ["Strongly Disagree", "Disagree", "Agree", "Strongly Agree"]:
        score_map = {
            "A": {"A": 1, "B": 0.75, "C": 0.5, "D": 0.25},
            "B": {"A": 0.25, "B": 1, "C": 0.75, "D": 0.5},
            "C": {"A": 0.25, "B": 0.5, "C": 1, "D": 0.75},
            "D": {"A": 0.25, "B": 0.5, "C": 0.75, "D": 1}
        }
        for answer, correct_option in zip(answers, correct_options):
            total_score += score_map.get(correct_option, {}).get(answer, 0)
    else:
        total_score = sum(1 for answer, correct_option in zip(answers, correct_options) if answer == correct_option)
    
    return total_score

def validate_option(option):
    # Add your own validation logic for options
    valid_options = ["A", "B", "C", "D"]
    if option not in valid_options:
        return False
    return True

# The test view logic
def dashboard_test(request):
    if request.method == 'POST':
        # Process the submitted answers
        answers = []
        correct_options = []
        questions = load_questions()
        for i, question in enumerate(questions):
            user_answer = request.POST.get(f'question_{i}')
            answers.append(user_answer)
            correct_options.append(question['correct_option'])
        
        # Calculate score
        total_score = calculate_score(answers, correct_options, ["A", "B", "C", "D"])  # Pass the options list
        return render(request, 'dashboard/dash-test.html', {'score': total_score, 'questions': questions})
    
    else:
        # Load questions for a new test
        questions = load_questions()
        return render(request, 'dashboard/dash-test.html', {'questions': questions})