from tkinter import *
from tkinter import messagebox
import random

# Define quiz questions with options and correct answers
questions = [
    {"question": "What is the capital of India?", "options": ["Amaravati", "New Delhi", "AP", "Chennai"],
     "correct_answer": "New Delhi"},
    {"question": "What is the first film of RGV?", "options": ["Rangeela", "Kshana Kshanam", "Siva", "Company"],
     "correct_answer": "Siva"},
    {"question": "In which state is Kedarnath located?", "options": ["Haryana", "Uttarakhand", "Delhi", "AP"],
     "correct_answer": "Uttarakhand"},
    {"question": "In which state is Rishikesh located?", "options": ["Haryana", "AP", "Delhi", "Uttarakhand"],
     "correct_answer": "Uttarakhand"},
    {"question": "What is the first film of Director Puri Jagannadh?",
     "options": ["Idiot", "Businessman", "Badri", "Bujjigadu"], "correct_answer": "Badri"},
    {"question": "Which character appears in both Ramayana and Mahabharata?",
     "options": ["Rama", "Hanuman", "Sita", "Ravana"], "correct_answer": "Hanuman"},
    {"question": "In which state is Puri Jagannatha Temple located?",
     "options": ["TamilNadu", "AP", "Odisha", "Kerala"], "correct_answer": "Odisha"},
    {"question": "In which state is Sree Padmanabhaswamy Temple located?",
     "options": ["TamilNadu", "AP", "Odisha", "Kerala"], "correct_answer": "Kerala"},
    {"question": "What is the first film of Sushant Singh Rajput?",
     "options": ["Raabta", "Kai Po Che", "Dil Bechara", "Chhichhore"], "correct_answer": "Kai Po Che"},
    {"question": "In which state is Ladakh located?",
     "options": ["Himachal Pradesh", "Kashmir", "Delhi", "None of the above"], "correct_answer": "None of the above"},
    {"question": "Who is the CEO of Tesla?",
     "options": ["Marc Tarpenning", "Jeff Bezos", "Elon Musk", "Mark Zuckerberg"], "correct_answer": "Elon Musk"}
]

# Initialize variables for quiz state
current_question, score, msg = 0, 0, ""
random_numbers = random.sample(range(11), 5)


# Function to handle radiobutton click
def on_radiobutton_click():
    next_button.config(bg="green", fg="white")


# Function to show warning if no option is selected
def did_not_attempt():
    messagebox.showwarning("Selected Nothing", "You have to attempt the question")


# Function to exit the application
def on_exit_click():
    window.destroy()


# Function to reset and retry the quiz
def on_retry_click():
    global random_numbers, current_question, score
    current_question = score = 0
    scale.config(state=NORMAL)
    scale.set(1)
    scale.config(state=DISABLED)
    check_button.config(text="Check", command=check_answer, bg="blue", fg="white")
    next_button.config(text="Next", command=on_next_click, bg="orange", fg="black")
    random_numbers = random.sample(range(11), 5)

    # Enable all options for the next attempt
    for option in options:
        option.config(state=NORMAL)

    display_question()


# Function to show warning when skipping questions
def on_scale_click(event):
    messagebox.showwarning("NO SKIP", "Go in a serial order!")


# Function to display the current question
def display_question():
    if current_question < 5:
        question_data = questions[random_numbers[current_question]]
        question_label.config(text=question_data["question"])

        for i in range(4):
            options[i].config(
                text=question_data["options"][i],
                value=question_data["options"][i]
            )

        radio_var.set("None")
        window.after(500, lambda: window.configure(bg="lightgrey"))
        # Adding fade-in effect
        window.attributes("-alpha", 0.1)
        window.deiconify()
        for alpha in range(1, 11):
            window.after(alpha * 50, lambda a=alpha / 10: window.attributes("-alpha", a))
    else:
        messagebox.showinfo("Quiz Completed", f"Your score: {score}/5")
        check_button.config(text="Retry", command=on_retry_click, bg="orange", fg="black")
        next_button.config(text="Exit", command=on_exit_click, bg="red", fg="white")

        # Disable all options after quiz completion
        for option in options:
            option.config(state=DISABLED)


# Function to check the selected answer
def check_answer():
    global current_question, msg
    if radio_var.get() == "None":
        did_not_attempt()
        return
    if radio_var.get() == questions[random_numbers[current_question]]["correct_answer"]:
        result_label.config(text="Correct!", fg="green")
    else:
        result_label.config(
            text=f"Incorrect! Correct answer is {questions[random_numbers[current_question]]['correct_answer']}",
            fg="red", padx=20)
    result_label.grid(row=11, column=0, columnspan=2, pady=20)


# Function to handle next/exit button click
def on_next_click():
    global current_question, score
    result_label.grid_forget()
    if radio_var.get() == "None":
        did_not_attempt()
        return
    if radio_var.get() == questions[random_numbers[current_question]]["correct_answer"]:
        score += 1
    current_question += 1
    scale.config(state=NORMAL)
    scale.set(current_question + 1)
    scale.config(state=DISABLED)
    display_question()
    if current_question < 5:
        next_button.config(command=on_next_click, bg="orange", fg="black")
    else:
        next_button.config(bg="red", fg="white")

    # Create the main Tkinter window


window = Tk()
window.title("QUIZ GAME")
window.geometry("650x550")
window.minsize(650, 550)
window.maxsize(660, 560)
window.wm_iconbitmap("quiz_favicon.ico")

# Create and configure the scale widget
scale = Scale(window, from_=1, to=5, orient=HORIZONTAL, tickinterval=1, sliderlength=15, width=15, troughcolor="black",
              state=DISABLED, bg="lightgrey", bd=0, highlightthickness=0)
scale.grid(row=3, columnspan=2, pady=10)
scale.bind("<Button-1>", on_scale_click)

# Create and configure the question label
question_label = Label(window, text="", font=("Arial", 14, "bold"), bg="lightgrey")
question_label.grid(row=5, columnspan=2, pady=30, padx=5)

# Create variables for radio buttons
radio_var = StringVar()

# Create and configure radio buttons for options
options = []
for i in range(4):
    option = Radiobutton(window, text="", variable=radio_var, value="", font=("Arial", 12, "bold"),
                         command=on_radiobutton_click, bg="lightgrey")
    option.grid(row=6 + i, column=0, sticky=W, padx=10)
    options.append(option)

# Display the initial question
display_question()

# Create and configure the "Check" button
check_button = Button(window, text="Check", command=check_answer, bg="blue", fg="white", font="Arial 12 bold")
check_button.grid(row=10, column=0, padx=100, pady=50)

# Create and configure the "Next" button
next_button = Button(window, text="Next", command=on_next_click, bg="orange", fg="black", font="Arial 12 bold")
next_button.grid(row=10, column=1, padx=100, pady=50)

# Create and configure the result label
result_label = Label(window, text=msg, font="Arial 19 bold", bg="lightgrey")

# Start the Tkinter event loop
window.mainloop()
