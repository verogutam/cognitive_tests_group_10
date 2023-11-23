import matplotlib.pyplot as plt
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import time
import ipywidgets as widgets
import pandas as pd
import random
from IPython.display import display, Image, clear_output, HTML
from jupyter_ui_poll import ui_events
from PIL import Image as IM
from IPython.display import clear_output

# Function that send the answer dictionary to google form
def send_to_google_form(data_dict, form_url):
    ''' Helper function to upload information to a corresponding google form
        You are not expected to follow the code within this function!
    '''
    form_id = form_url[34:90]
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}

    loaded_all = True
    for item in result:
        if item[1] not in data_dict:
            print(f"Form item {item[1]} not found. Data not uploaded.")
            loaded_all = False
            return False
        form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]

    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok

# function for run ANS test
def test1():
    # function for waiting
    event_info = {
        'type': '',
        'description': '',
        'time': -1
    }

    def wait_for_event(timeout=-1, interval=0.001, max_rate=20, allow_interupt=True):
        start_wait = time.time()
        event_info['type'] = ""
        event_info['description'] = ""
        event_info['time'] = -1

        n_proc = int(max_rate * interval) + 1

        with ui_events() as ui_poll:
            keep_looping = True
            while keep_looping == True:
                ui_poll(n_proc)

                if (timeout != -1) and (time.time() > start_wait + timeout):
                    keep_looping = False

                if allow_interupt == True and event_info['description'] != "":
                    keep_looping = False

                time.sleep(interval)
        return event_info

    # function for bottons
    def register_event(btn):
        event_info['type'] = "click"
        event_info['description'] = btn.description
        event_info['time'] = time.time()
        return

    # function for displaying image
    def display_img(img_file):
        style_str = f'width: 500px'
        html_out = HTML(f"<img style='{style_str}' src={img_file}></img>")
        display(html_out)

    # function for running the test and compare results with correct answer
    def which_more(img_file, right_answer):
        time.sleep(1.5)
        display_img(img_file)
        time.sleep(0.75)
        clear_output(wait=False)
        # buttons
        btn1 = widgets.Button(description="Left")
        btn2 = widgets.Button(description="Right")
        btn1.on_click(register_event)
        btn2.on_click(register_event)
        myhtml1 = HTML("<h1>You have 3 seconds to answer</h1>")
        display(myhtml1)

        panel = widgets.HBox([btn1, btn2])
        display(panel)
        result = wait_for_event(timeout=3)
        clear_output()

        if result['description'] != "":
            print(f"User clicked: {result['description']}")
        else:
            print("User did not click in time")

        score = 0

        if event_info['description'] == right_answer:
            print("Well done!")
            score = 1
        else:
            print(f"Sorry the answer was {right_answer}")

        return score

    # define the correct answer
    files = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png", "10.png", "11.png",
             "12.png", "13.png", "14.png", "15.png", "16.png", "17.png", "18.png", "19.png", "20.png", "21.png",
             "22.png", "23.png", "24.png", "25.png", "26.png", "27.png", "28.png", "29.png", "30.png", "31.png",
             "32.png", "33.png", "34.png", "35.png", "36.png", "37.png", "38.png", "39.png", "40.png", "41.png",
             "42.png", "43.png", "44.png", "45.png", "46.png", "47.png", "48.png", "49.png", "50.png", "51.png",
             "52.png", "53.png", "54.png", "55.png", "56.png", "57.png", "58.png", "59.png", "60.png", "61.png",
             "62.png", "63.png", "64.png"]
    answers = ["Right", "Right", "Left", "Left", "Right", "Right", "Left", "Right", "Left", "Left", "Left", "Left",
               "Right", "Left", "Right", "Right", "Left", "Right", "Left", "Right", "Right", "Right", "Right", "Right",
               "Right", "Left", "Right", "Right", "Right", "Right", "Right", "Left", "Right", "Right", "Right", "Left",
               "Right", "left", "Left", "Left", "Left", "Left", "Right", "Left", "Right", "Left", "Right", "Left",
               "Right", "Left", "Left", "Left", "Right", "Right", "Left", "Left", "Left", "Left", "Right", "Left",
               "Right", "Right", "Right", "Left", "Left", "Right", "Right"]
    print("Welcome to the ANS testing")

    time.sleep(1)
    print(
        "From the following test you are expecting to estimate which circle contains more small circles within,please choose left or right:")
    time.sleep(3)
    print(
        "You have 3 seconds to answer each question, the whole test have 64 questions taking about 3 and a half minutes")
    time.sleep(3)
    total = 0
    n_correct = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    start_time = time.time()

    # get output for time taken, total score, and score for individual questions
    for i in range(len(files)):
        image = f"dots/{files[i]}"
        score = which_more(image, answers[i])
        total += score
        n_correct[i] += score
        end_time = time.time()
        time_taken = round(end_time - start_time)

    return (time_taken, total, n_correct)

# Function that displays each part of the question separately (for 1.3 seconds)
def display_question_parts(question):
    parts = question.split()
    for i, part in enumerate(parts):
        clear_output(wait=True)
        display(HTML(f"<p style='font-size: 30px; color: black;'>{part}</p>"))
        if i == 1:
            time.sleep(1.3)  # flash each part of the question onscreen for 1.3 seconds
        else:
            time.sleep(1.3)
            clear_output(wait=True)
            time.sleep(0.3)  # brief pause before next part (0.3 seconds duration)
# Function that generates questions of different difficulty levels
def generate_question(difficulty):
    if difficulty == 1:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
    elif difficulty == 2:
        num1 = random.randint(10, 20)
        num2 = random.randint(1, 10)
    else:
        num1 = random.randint(10, 20)
        num2 = random.randint(10, 20)

    operator = random.choice(['+', '-', '*'])
    question = f"{num1} {operator} {num2}"

    return question, eval(question)
# Function for running the entire quiz, using the functions above
def run_quiz():
    random.seed(42)  # Setting a random seed for reproducibility

    results = {'score': 0, 'total_time': 0, 'avg_time': 0, 'raw_results': []}

    total_score = 0
    total_time = 0
    difficulty = 1
    question_duration = 1.3  # in seconds
    quiz_duration = 180  # in seconds

    start_time = time.time()

    while time.time() - start_time < quiz_duration:
        question, answer = generate_question(difficulty)

        clear_output(wait=True)
        display_question_parts(question)

        start_question_time = time.time()
        user_answer = input("Your answer: ")
        end_question_time = time.time()

        try:
            user_answer = float(user_answer)
        except ValueError:
            user_answer = None

        results['raw_results'].append(user_answer)  # Saving raw user inputs

        if user_answer == answer:
            total_score += 1
            total_time += end_question_time - start_question_time

        time.sleep(question_duration)

        difficulty += 1

    results['score'] = total_score
    results['total_questions'] = difficulty - 1
    if total_score > 0:
        results['avg_time'] = total_time / total_score
    else:
        results['avg_time'] = None
    results['total_time'] = total_time

    return results, total_score, results['avg_time']

# Function to run the memory_test
def memory_test():
    grid_easy = Image("Grid/grideasy.png", width=500)
    grid_medium = Image("Grid/gridmedium.png", width=500)
    grid_hard = Image("Grid/gridhard.png", width=500)
    indicated_position = Image("Grid/indicatedposition.png", width=500)
    positions = Image("Grid/positions.png", width=500)

    text1 = f"Welcome to part C - the memory test!"
    text2 = "You need to answer a series of questions about the displayed grids (with varying levels of difficulty) to complete this part, good luck!"
    style1 = "color: black; font-size: 30px;"
    style2 = "color: black; font-size: 20px;"
    html_out1 = HTML(f"<span style = '{style1}'>{text1}</span>")
    html_out2 = HTML(f"<span style = '{style2}'>{text2}</span>")

    display(html_out1, html_out2)
    time.sleep(2.5)
    clear_output(wait=False)

    text3 = "Part C.1 - difficulty level: easy"
    style3 = "color: black; font-size: 30px;"
    html_out3 = HTML(f"<span style = '{style3}'>{text3}</span>")
    display(html_out3)

    start_time = time.time()

    display(grid_easy)
    time.sleep(5)
    clear_output(wait=False)

    q1_1 = input("What colour was the triangle?")
    q1_2 = input("Which shape was to the right of the star?")
    q1_3 = input("Which primary colour was missing from the grid? (hint: blue, red, and yellow are primary colours)")

    time.sleep(2)
    clear_output(wait=False)

    text4 = "Part C.2 - difficulty level: medium"
    style4 = "color: black; font-size: 30px;"
    html_out4 = HTML(f"<span style = '{style4}'>{text4}</span>")
    display(html_out4)

    display(grid_medium)
    time.sleep(7.5)
    clear_output(wait=False)

    q2_1 = input("What colour was the square?")
    q2_2 = input("What shape was above the pentagon?")
    display(indicated_position)
    q2_3 = input("""Was the shape in the indicated position a regular polygon? Answer with yes or no.
    (Hint: a regular polygon is an n-sided polygon in which the sides are all the same length and are symmetrically placed about a common centre, i.e., the polygon is both equiangular and equilateral)""")

    time.sleep(2)
    clear_output(wait=False)

    text5 = "Part C.3 - difficulty level: hard"
    style5 = "color: black; font-size: 30px;"
    text6 = """Give your answers to this section in a Pn format (e.g., P1).
    If there is more than one answer to a question use a comma to separate them (e.g., P1, P2 - DO NOT PUT A SPACE BEFORE THE COMMA, JUST ONE AFTER).
    Give answers in chronological order (i.e., P7, P8 and NOT P8, P7)."""
    style6 = "color: black; font-size: 20px;"
    html_out5 = HTML(f"<span style = '{style5}'>{text5}</span>")
    html_out6 = HTML(f"<span style = '{style6}'>{text6}</span>")
    display(html_out5, html_out6)

    display(grid_hard)
    time.sleep(12.5)
    clear_output(wait=False)

    display(positions)
    q3_1 = input("Shapes in which position(s) had a black inner shape?")
    q3_2 = input("Shapes in which positions looked identical?")
    q3_3 = input("What colour was position 2's inner triangle?")

    time.sleep(2)
    clear_output(wait=False)

    end_time = time.time()
    time_taken = round(end_time - start_time)

    result_list = []
    raw_data = [q1_1, q1_2, q1_3, q2_1, q2_2, q2_3, q3_1, q3_2, q3_3]
    total_score = 0
    answer_dict = {q1_1: "green", q1_2: "circle", q1_3: "blue", q2_1: "purple", q2_2: "star", q2_3: "no",
                   q3_1: "p3, p5", q3_2: "p4, p6", q3_3: "yellow"}

    if q1_1.lower() == answer_dict[q1_1]:
        result_list.append("correct")
        total_score = total_score + 1
    else:
        result_list.append("wrong")

    if q1_2.lower() == answer_dict[q1_2]:
        result_list.append("correct")
        total_score = total_score + 1
    else:
        result_list.append("wrong")

    if q1_3.lower() == answer_dict[q1_3]:
        result_list.append("correct")
        total_score = total_score + 1
    else:
        result_list.append("wrong")

    if q2_1.lower() == answer_dict[q2_1]:
        result_list.append("correct")
        total_score = total_score + 1
    else:
        result_list.append("wrong")

    if q2_2.lower() == answer_dict[q2_2]:
        result_list.append("correct")
        total_score = total_score + 1
    else:
        result_list.append("correct")

    if q2_3.lower() == answer_dict[q2_3]:
        result_list.append("correct")
        total_score = total_score + 1
    else:
        result_list.append("wrong")

    if q3_1.lower() == answer_dict[q3_1]:
        result_list.append("correct")
        total_score = total_score + 1
    else:
        result_list.append("wrong")

    if q3_2.lower() == answer_dict[q3_2]:
        result_list.append("correct")
        total_score = total_score + 1
    else:
        result_list.append("wrong")

    if q3_3.lower() == answer_dict[q3_3]:
        result_list.append("correct")
        total_score = total_score + 1
    else:
        result_list.append("wrong")

    results = f"It took you {time_taken} seconds to complete this part of the test, well done!"
    r_style = "color: black; font-size: 20px;"
    r_html_out = HTML(f"<span style = '{r_style}'>{results}</span>")
    return time_taken, total_score, result_list, raw_data

# Function to run the spatial_reasoning test
def spatial_reasoning_test():
    # This will first defined a general pool of image
    # Then we randomly shuffle it and take out five to do the test
    result_list = []
    row_result_list = []

    # Set up a dictionary to verify the answer
    answer_dict = {0: "a", 1: "d", 2: "c", 3: "b", 4: "a", 5: "c"}

    print("This is the Spatial Reasoning Test")
    time.sleep(1)
    print("You will be shown a 3-d cubes image and four 2-d cube choices for each question")
    time.sleep(1)
    print("Please type in the image that can not be made by rotating the cube arrangement shown")
    time.sleep(3)

    print("You will only have one chance to answer each question, and we are measuring the number of correct answers")
    time.sleep(2)

    start = input("When you are ready to start the test enter S here: ")

    clear_output(wait=False)

    total_time = 0

    # Set up the images for the test
    for i in range(0, 6):
        # Creating the plot to hold the images
        fig = plt.figure(figsize=(10, 8))

        # Displaying question image
        ax1 = fig.add_subplot(2, 2, (1, 2))
        ax1.imshow(IM.open(f"Image/{i}.png"))
        ax1.set_title('Question')
        ax1.axis('off')  # Hide the axes

        # Displaying choices subplots
        label_list = ["A", "B", "C", "D"]
        for idx, label in enumerate(label_list):
            ax = fig.add_subplot(2, 4, idx + 5)  # Positions 5-8 are for the second row in a 2x4 grid
            ax.imshow(IM.open(f"Image/{i}_{label.lower()}.png"))
            ax.set_title(label)
            ax.axis('off')  # Hide the axes

        plt.tight_layout()
        plt.show(block=False)
        plt.pause(1)

        start_time = time.time()  # Starting counting the time

        # The part for gathering user input and save them to the two lists created
        answer = input("Please type your answer here: ")
        if answer.lower() == answer_dict[i]:
            result_list.append(1)
        else:
            result_list.append(0)

        row_result_list.append(answer)

        clear_output(wait=False)

        end_time = time.time()
        time_taken = end_time - start_time

        total_time += time_taken

    print("You have completed the test! Well done!")

    return (total_time, result_list, row_result_list)


def all_tests():
    data_consent_info = """DATA CONSENT INFORMATION:

    Please read:

    we wish to record your response data
    to an anonymised public data repository. 
    Your data will be used for educational teaching purposes
    practising data analysis and visualisation.

    Please type   yes   in the box below if you consent to the upload."""

    print(data_consent_info)
    result = input("> ")

    if result == "yes":
        clear_output(wait=False)
        print("Thanks for your participation.")
        print("Please contact philip.lewis@ucl.ac.uk")
        print("If you have any questions or concerns")
        print("regarding the stored results.")


    else:
        # end code execution by raising an exception
        raise (Exception("User did not consent to continue test."))
        
    name = input("Please type your name here ")
    age = input("Please type your age here: ")
    gender = input("Please type your gender here: ")
    id_instructions = """

    Enter your anonymised ID

    To generate an anonymous 4-letter unique user identifier please enter:
    - two letters based on the initials (first and last name) of a childhood friend
    - two letters based on the initials (first and last name) of a favourite actor / actress

    e.g. if your friend was called Charlie Brown and film star was Tom Cruise
         then your unique identifer would be CBTC
    """

    print(id_instructions)
    user_id = input("> ")

    print("User entered id:", user_id)

    time.sleep(1)
    clear_output(wait=False)

    time.sleep(2)
    print("Welcome to the Math ability test!")
    time.sleep(2)
    aver_time_B, results_B, raw_results_B = run_quiz()

    time.sleep(2)
    total_time_C, total_score_C, results_C, raw_results_C = memory_test()

    time.sleep(2)
    total_time_D, results_D, raw_results_D = spatial_reasoning_test()

    time.sleep(2)
    total_time_A, results_A, raw_results_A = test1()

    answer_to_upload_dict = {
        "User ID": user_id,
        "Name": name,
        "Age": age,
        "Male or Female": gender,
        "Total Time - Part A (in seconds)": total_time_A,
        "Results - Part A": results_A,
        "Raw Results - Part A": raw_results_A,
        "Average Time - Part B (in seconds)": aver_time_B,
        "Results - Part B": results_B,
        "Raw Results - Part B": raw_results_B,
        "Total Time - Part C (in seconds)": total_time_C,
        "Results - Part C": results_C,
        "Raw Results - Part C": raw_results_C,
        "Total Time - Part D (in seconds)": total_time_D,
        "Results - Part D": results_D,
        "Raw Result - Part D": raw_results_D
    }

    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSd6vTK6IISyfvZwSszk1tAFHzUJcXC9H-tQymO-dHNHMw9JoQ/viewform?usp=sf_link"
    send_to_google_form(answer_to_upload_dict, form_url)








