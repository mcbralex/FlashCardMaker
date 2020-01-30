#Alex McBride CIS 345 12pm Final
from tkinter import *
import os
import json
from difflib import get_close_matches
import random

#global variables
questionList = []
count = 0
correct = 0
points = 0

class Question:
    """Question Class"""

    def __init__(self, qtext="", choice=None, correct_answer="", feedback_correct="", feedback_incorrect='', point_value="0"):

        self.__text = qtext
        if choice == None:
            self.__choice = list()
        else:
            self.__choice = choice
        self.__correct_answer = correct_answer
        self.__feedback_correct = feedback_correct
        self.__feedback_incorrect = feedback_incorrect
        self.__point_value = point_value

    @property
    def text(self):
        return self.qtext
    @text.setter
    def text(self, qtext):
        self.__qtext = qtext

    @property
    def points(self):
        return self.__point_value
    @points.setter
    def points(self, points):
        self.__point_value = points

    @property
    def answer(self):
        return self.__correct_answer

    @answer.setter
    def points(self, answer):
        self.__correct_answer = answer

    @property
    def correct_feedback(self):
        return self.__feedback_correct

    @correct_feedback.setter
    def correct_feedback(self, feedback):
        self.__feedback_correct = feedback

    @property
    def incorrect_feedback(self):
        return self.__feedback_incorrect

    @correct_feedback.setter
    def correct_feedback(self, feedback):
        self.__feedback_incorrect = feedback

    def display_choice(self):
        for i in self.choice:
            print(i)

    def set_display_choice(self, choice):
        self.__choice.append(choice)


def load_info():
    """loads json file and makes data into a list of Question objects"""
    global questionList
    questionList = []
    try:
        with open('questions.json') as file:
            data = json.load(file)

    except FileNotFoundError or IOError:
        print('file not found')
        # loops through file and saves to data as dictionary
    finally:
        count = 1
        for i in range(len(data)):
            temp_question = Question()
            temp_question.qtext = data[i]["text"]
            temp_question.point_value = data[i]["points"]
            temp_question.choices = data[i]["choices"]
            temp_question.correct_answer = data[i]["answer"]
            temp_question.feedback_correct = data[i]["correctFeedback"]
            temp_question.feedback_incorrect= data[i]["incorrectFeedback"]
            count = count + 1
            questionList.append(temp_question)

    print('\n\ndata loaded')


def delete_question(question_text,frame):
    """deletes question from frame json file and questionList"""
    global questionList
    obj = json.load(open("questions.json"))

    # Iterate through the objects in the JSON and pop (remove)
    # the obj once we find it.
    for i in range(0,len(obj)):
        if obj[i]["text"] == question_text:
            print(question_text)
            print(obj[i]["text"])
            obj.pop(i)

            break
    open("questions.json", "w").write(
        json.dumps(obj)
    )
    frame.destroy()
    load_info()

    display_question()


def add_question(text, points, a, b, c, d, answer, correctFeedback, incorrectFeedback, frame):
    """runs validation and adds question to JSON list and refreshes frame"""
    frame = frame
    print(text)

    #makshift validation
    if text == "Enter Question Text":
        error_text = Label(frame, text="Please add question text", fg='red')
        error_text.grid(row=len(questionList) + 7, column=2)
    elif points == "1-10":
        error_points = Label(frame, text="points", fg='red')
        error_points.grid(row=len(questionList) + 7, column=3)
    elif a == "Choice 1" or b == "Choice 2" or c == "Choice 3" or d == "Choice 4":
        error_choices = Label(frame, text="Enter 4 choices", fg='red')
        error_choices.grid(row=len(questionList) + 11, column=4)
    elif answer == "Correct Answer":
        error_answer = Label(frame, text="points", fg='red')
        error_answer.grid(row=len(questionList) + 7, column=5)
    elif correctFeedback == "Correct Feedback":
        error_correct = Label(frame, text="Add feedack", fg='red')
        error_correct.grid(row=len(questionList) + 7, column=6)
    elif incorrectFeedback == "Incorrect Feedback":
        error_incorrect = Label(frame, text="Add feedack", fg='red')
        error_incorrect.grid(row=len(questionList) + 7, column=6)

    #adds new question to JSON file
    else:
        newQuestion = {"text": "", "points": 0, "choices": [], "answer": "", "correctFeedback": "", "incorrectFeedback": ""}
        newQuestion["text"] = text
        newQuestion["points"] = points
        newQuestion["choices"] = [a,b,c,d]
        newQuestion["answer"] = answer
        newQuestion["correctFeedback"] = correctFeedback
        newQuestion["incorrectFeedback"] = incorrectFeedback

        obj = json.load(open("questions.json"))
        obj.append(newQuestion)
        open("questions.json", "w").write(
        json.dumps(obj))

        frame.destroy()
        load_info()
        display_question()


def edit_question(question,frame,i):
    """Function to edit and save existing questions"""
    global questionList
    print(question.points)

    #creates text boxes populated with the current question that can be edited.
    textbox_text = Entry(frame, width=20, fg='grey')
    textbox_text.insert(END, f"{question.text}")
    textbox_text.grid(row=i + 6, column=2)

    textbox_points = Entry(frame, width=5, fg='grey')
    textbox_points.insert(END, f"{question.point_value}")
    textbox_points.grid(row=i + 6, column=3)

    textbox_choices_a = Entry(frame, width=20, fg='grey')
    textbox_choices_a.insert(END, f"{question.choices[0]}")
    textbox_choices_a.grid(row=i + 6, column=4)

    textbox_choices_b = Entry(frame, width=20, fg='grey')
    textbox_choices_b.insert(END, f"{question.choices[1]}")
    textbox_choices_b.grid(row=i + 7, column=4)

    textbox_choices_c = Entry(frame, width=20, fg='grey')
    textbox_choices_c.insert(END, f"{question.choices[2]}")
    textbox_choices_c.grid(row=i + 8, column=4)

    textbox_choices_d = Entry(frame, width=20, fg='grey')
    textbox_choices_d.insert(END, f"{question.choices[3]}")
    textbox_choices_d.grid(row=i + 9, column=4)

    textbox_answer = Entry(frame, width=10, fg='grey')
    textbox_answer.insert(END, f"{question.correct_answer}")
    textbox_answer.grid(row=i + 6, column=5)

    textbox_correct_feedback = Entry(frame, width=12, fg='grey')
    textbox_correct_feedback.insert(END, f"{question.feedback_correct}")
    textbox_correct_feedback.grid(row=i + 6, column=6)

    textbox_incorrect_feedback = Entry(frame, width=12, fg='grey')
    textbox_incorrect_feedback.insert(END, f"{question.feedback_incorrect}")
    textbox_incorrect_feedback.grid(row=i + 6, column=7)

    #saves the edit
    button_save_question = Button(frame, command=lambda: save_edit(textbox_text.get(), textbox_points.get(),
                                                                     textbox_choices_a.get(),
                                                                     textbox_choices_b.get(), textbox_choices_c.get(),
                                                                     textbox_choices_d.get(), textbox_answer.get(),
                                                                     textbox_correct_feedback.get(),
                                                                     textbox_incorrect_feedback.get(),
                                                                     frame,i), text="Save", height=2, width=10)
    button_save_question.grid(row=i+ 6, column=8, columnspan=2)


def save_edit(text, points, a, b, c, d, answer, correctFeedback, incorrectFeedback, frame,i):
    """saves the edited question and replaces the old one"""
    newQuestion = {"text": "", "points": 0, "choices": [], "answer": "", "correctFeedback": "", "incorrectFeedback": ""}
    newQuestion["text"] = text
    newQuestion["points"] = points
    newQuestion["choices"] = [a, b, c, d]
    newQuestion["answer"] = answer
    newQuestion["correctFeedback"] = correctFeedback
    newQuestion["incorrectFeedback"] = incorrectFeedback

    #saves to the json file
    obj = json.load(open("questions.json"))
    obj[i] = newQuestion
    open("questions.json", "w").write(
        json.dumps(obj))

    frame.destroy()
    load_info()
    display_question()


def search_questions(search,frame):
    """search question function"""

    global questionList

    if search == "":
        frame.grid_forget()
        display_question(0)

    textList = []
    choiceList = []
    feedbackList = []
    searchList = []

    #creates lists to be passed into the get close match function
    for i in range(len(questionList)):

       textList.append(questionList[i].text)
       choiceList.append(questionList[i].choices)
       feedbackList.append(questionList[i].feedback_correct)

    textList =  get_close_matches(search,textList,cutoff=.6)

    if not textList:
        search_lbl2 = Label(frame, text="No matching results", height=2)
        search_lbl2.grid(row=1, column=6, columnspan=3)
    else:

    #compares the results of the get close match function to the questionList
        for i in range(len(questionList)):
            for j in range(len(textList)):
                if textList[j] == questionList[i].text or textList[j] == questionList[i].choices or textList[j] == questionList[i].feedback_correct:
                    searchList.append(questionList[i])



        #calls display)funciton to use the new searchList to display questions
        frame.destroy()
        display_question(1,searchList)


def quiz_game(frame="", gameWindow=""):
    """quiz game function"""
    global questionList, count, correct, points
    print(count)

    if count == 0:

        gameWindow = Tk()
        gameWindow.title('Quiz')
        gameWindow.geometry("280x300")
    if count >= 1:

        frame.grid_forget()

    frame = Frame(gameWindow)
    frame.grid()

    gameList = []

    #results screen
    if count == 3:
        game_lbl = Label(frame, text="Results", width=20)
        game_lbl.grid(row=1, column=4, columnspan=4)

        result = Label(frame, text=f'You got {correct} out of 3 questions', width=20)
        result.grid(row=2, column=4, columnspan=4)

        pointslbl = Label(frame, text=f'Point total: {points}')
        pointslbl.grid(row=8, column=3, columnspan=4)

    else:

        #creates 3 questionList
        gameList.append(questionList[random.randint(0, len(questionList) - 6)])
        gameList.append(questionList[random.randint(3, len(questionList) - 3)])
        gameList.append(questionList[random.randint(6, len(questionList) - 1)])

        game_lbl = Label(frame, text=gameList[count].text, width=30)
        game_lbl.grid(row=1, column=4, columnspan=3)

        a_lbl = Button(frame,
                        command=lambda: selected_answer(gameList[count].choices[0], gameList[count], frame, gameWindow),
                        text=gameList[count].choices[0], height=5, width=15)
        a_lbl.grid(row=3, column=3, columnspan=2)

        b_lbl = Button(frame,
                        command=lambda: selected_answer(gameList[count].choices[1], gameList[count], frame, gameWindow),
                        text=gameList[count].choices[1], height=5, width=15)
        b_lbl.grid(row=3, column=6, columnspan=2)

        c_lbl = Button(frame,
                        command=lambda: selected_answer(gameList[count].choices[2], gameList[count], frame, gameWindow),
                        text=gameList[count].choices[2], height=5, width=15)
        c_lbl.grid(row=4, column=3, columnspan=2)

        d_lbl = Button(frame,
                        command=lambda: selected_answer(gameList[count].choices[3], gameList[count], frame, gameWindow),
                        text=gameList[count].choices[3], height=5, width=15)
        d_lbl.grid(row=4, column=6, columnspan=2)

    gameWindow.mainloop()


def selected_answer(text, gameList, frame, gameWindow):
    """funciton that decides if answer is correct"""
    global count, correct, points
    count = count +1

    if text == gameList.correct_answer:
        correct = correct +1
        points = points + int(gameList.point_value)
        correct_lbl = Label(frame, text = gameList.feedback_correct)
        correct_lbl.grid(row = 6, column=3, columnspan=4)

        result = Label(frame, text=f'You got {correct} out of 3 questions')
        result.grid(row=7, column=3, columnspan=4)

        pointslbl = Label(frame, text=f'Point total: {points}')
        pointslbl.grid(row=8, column=3, columnspan=4)

        next_button = Button(frame, command= lambda: quiz_game(frame,gameWindow),text = "Next", width = 10)
        next_button.grid(row=5, column=3, columnspan=4)
    else:
        points = points + 1
        incorrect_lbl = Label(frame,text = gameList.feedback_incorrect)
        incorrect_lbl.grid(row=6, column=3)

        pointslbl = Label(frame, text=f'Point total: {points}')
        pointslbl.grid(row=8, column=3, columnspan=4)

        result = Label(frame, text=f'You got {correct} out of 3 questions', width=20)
        result.grid(row=2, column=4, columnspan=3)

        next_button = Button(frame, command = lambda : quiz_game(frame,gameWindow),text = "Next", width = 10)
        next_button.grid(row = 5, column = 3)


def home(frame):
    """reverts list back to questionList"""
    frame.grid_forget()
    display_question(0)


def display_question(search= "", searchList= ""):
    """Displays each question and creates frame"""
    global  questionList
    frame = Frame(window)
    frame.grid()
    load_info()

    if search == 1:
        home_btn = Button(frame, command=lambda: home(frame), text="Show All")
        home_btn.grid(row=3, column=7, columnspan=3)

        print(searchList[0].text)
        questionList = searchList

    #Top Menu System
    title_lbl = Label(frame, text = "Mental Anguish",font=("Courier", 44))
    title_lbl.grid(row = 0, column = 0, columnspan = 9)

    blank_lbl2 = Label(frame, text="", height=2)
    blank_lbl2.grid(row=1, column=0, columnspan=9)

    button_play = Button(frame, command=lambda: quiz_game(), text="Quiz Me!", font= ("Courier", 20),height=2, width=15)
    button_play.grid(row=2, column=0, columnspan = 9)

    search_lbl2 = Label(frame, text="Search For a Question", height=2)
    search_lbl2.grid(row=1, column=6, columnspan=3)

    search_entry = Entry(frame)
    search_entry.grid(row=2, column=6, columnspan=3)

    search_btn = Button(frame, command= lambda : search_questions(search_entry.get(),frame), text="search")
    search_btn.grid(row=3, column=6, columnspan=3)

    blank_lbl = Label(frame, text="", height = 2)
    blank_lbl.grid(row=3, column=0, columnspan=9)

    list_lbl = Label(frame, text="Question List", font=("Courier 20 underline bold"))
    list_lbl.grid(row=4, column=0, columnspan=3)

    #top question labels
    feedback_lbl = Label(frame, text=f'Question',font= ('Courier 14 underline bold'))
    feedback_lbl.grid(row=5, column=1)
    feedback_lbl = Label(frame, text="Text", width = 20,font= ('Courier 14 underline bold'))
    feedback_lbl.grid(row=5, column=2)
    feedback_lbl = Label(frame, text="Points",font= ('Courier 14 underline bold'))
    feedback_lbl.grid(row=5, column=3)
    feedback_lbl = Label(frame, text="Choices", width = 20,font= ('Courier 14 underline bold'))
    feedback_lbl.grid(row=5, column=4)
    feedback_lbl = Label(frame, text="Correct Answer",font= ('Courier 14 underline bold'))
    feedback_lbl.grid(row=5, column=5)
    feedback_lbl = Label(frame, text="Correct Feedback",font= ('Courier 14 underline bold'))
    feedback_lbl.grid(row=5, column=6)
    feedback_lbl = Label(frame, text="Incorrect Feedback",font= ('Courier 14 underline bold'))
    feedback_lbl.grid(row=5, column=7)

    #loops through question list to print questions
    for i in range(len(questionList)):
        number_lbl = Label(frame, text=f'{i + 1}')
        number_lbl.grid(row = i+6, column=1)
        feedback_lbl = Label(frame, text=questionList[i].text)
        feedback_lbl.grid(row = i+6, column=2)
        feedback_lbl = Label(frame, text=questionList[i].point_value)
        feedback_lbl.grid(row=i+6, column=3)
        feedback_lbl = Label(frame, text=questionList[i].choices)
        feedback_lbl.grid(row=i+6, column=4)
        feedback_lbl = Label(frame, text=questionList[i].correct_answer)
        feedback_lbl.grid(row=i+6, column=5)
        feedback_lbl = Label(frame, text=questionList[i].feedback_correct)
        feedback_lbl.grid(row=i+6, column=6)
        feedback_lbl = Label(frame, text=questionList[i].feedback_incorrect)
        feedback_lbl.grid(row=i+6, column=7)

        button_delete = Button(frame, command=lambda i=i: delete_question(questionList[i].text,frame), text="Delete", height=2, width=5)
        button_delete.grid(row=i+6, column=8)
        button_edit = Button(frame, command=lambda i=i: edit_question(questionList[i],frame,i), text="Edit", height=2, width=5)
        button_edit.grid(row=i+6, column=9)

    textbox_question = Label(frame, width = 10, text = "New Question")
    textbox_question.grid(row=len(questionList)+6, column=1)

    textbox_text = Entry(frame, width =20, fg = 'grey')
    textbox_text.insert(END, "Enter Question Text")
    textbox_text.grid(row=len(questionList)+6, column=2)

    textbox_points = Entry(frame, width=5, fg='grey')
    textbox_points.insert(END, "1-10")
    textbox_points.grid(row=len(questionList) + 6, column=3)

    textbox_choices_a = Entry(frame, width=20, fg='grey')
    textbox_choices_a.insert(END, "Choice 1")
    textbox_choices_a.grid(row=len(questionList) + 6, column=4)

    textbox_choices_b = Entry(frame, width=20,fg='grey')
    textbox_choices_b.insert(END, "Choice 2")
    textbox_choices_b.grid(row=len(questionList) + 7, column=4)

    textbox_choices_c = Entry(frame, width=20, fg='grey')
    textbox_choices_c.insert(END, "Choice 3")
    textbox_choices_c.grid(row=len(questionList) + 8, column=4)

    textbox_choices_d = Entry(frame, width=20, fg='grey')
    textbox_choices_d.insert(END, "Choice 4")
    textbox_choices_d.grid(row=len(questionList) + 9, column=4)

    textbox_answer = Entry(frame, width=10,fg = 'grey')
    textbox_answer.insert(END, "Correct answer")
    textbox_answer.grid(row=len(questionList) + 6, column=5)

    textbox_correct_feedback = Entry(frame, width=12, fg = 'grey')
    textbox_correct_feedback.insert(END, "Correct feedback")
    textbox_correct_feedback.grid(row=len(questionList) + 6, column=6)

    textbox_incorrect_feedback = Entry(frame, width=12, fg = 'grey')
    textbox_incorrect_feedback.insert(END, "Incorrect feedback")
    textbox_incorrect_feedback.grid(row=len(questionList) + 6, column=7)

    button_add_question = Button(frame, command=lambda: add_question(textbox_text.get(), textbox_points.get(), textbox_choices_a.get(),
                                                                    textbox_choices_b.get(), textbox_choices_c.get(),
                                                                    textbox_choices_d.get(), textbox_answer.get(),
                                                                    textbox_correct_feedback.get(), textbox_incorrect_feedback.get(),
                                                                    frame), text="Add", height=2, width=8)

    button_add_question.grid(row=len(questionList)+6, column=8, columnspan=2)


window = Tk()
window.title('Mental Anguish')
window.geometry("1200x900")

load_info()
display_question()

window.mainloop()