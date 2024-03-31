import html
import random
from tkinter import *
from questions import *
from functools import partial

categories = list(map_category.keys())
category_map = map

class Screens:

    def __init__(self):
        self.main_screen = Tk()
        self.main_screen.minsize(500, 600)
        self.main_screen.title("Start")
        self.main_screen.config(bg="orange")
        self.move_to_second = Button(self.main_screen, text="Start Game", highlightbackground="orange",
                                     command=self.move_to_second)
        self.move_to_second.config(width=10, height=2)
        self.move_to_second.place(x=190, y=150)
        self.info = Label(
            text="Welcome to the ultimate quiz challenge!\n\nTest your knowledge and\nhave fun \nwith our exciting questions.",
            font=('Courier', 18, 'bold'), bg="orange", fg="dodger blue")
        self.info.place(x=40, y=250)
        self.score = 0

    def move_to_second(self):
        self.main_screen.withdraw()
        self.__second_screen = Toplevel(self.main_screen, bg="dodger blue")
        self.__second_screen.title("Categories")
        self.__second_screen.minsize(600, 450)

        self.__move_to_main = Button(self.__second_screen, text="Move to Start Screen",
                                     highlightbackground="dodger blue", command=self.to_start)
        self.__move_to_main.grid(row=0, column=0)

        self.second_screen_categories()

        # WHEN SECONDARY WINDOW GOT CLOSED
        self.__second_screen.protocol("WM_DELETE_WINDOW", self.shut_down_all)

    def second_screen_categories(self):
        # half =len(categories)//2
        headline = Label(self.__second_screen, text="Choose Category", bg="dodger blue", font=('Courier', 28, 'bold'),
                         fg="dark orange", pady=60)
        headline.grid(row=1, column=1)
        for i in range(0, len(categories)):
            b = Button(self.__second_screen, text=categories[i], highlightbackground="dodger blue",
                       command=partial(self.third_screen, categories[i]))
            if i >= len(categories) / 2:
                b.grid(row=3, column=i - (len(categories) // 2), padx=50, pady=20)
            else:
                b.grid(row=2, column=i, padx=50, pady=20)

    def third_screen(self, category_chosen):
        self.categories_to_quiz()

        # Create a PhotoImage instance as an instance variable
        self.bubble = PhotoImage(file="bub12.png")
        self.bubble = self.bubble.subsample(2)

        self.quote_shape = Canvas(self.__third, width=8000, height=600, bg="dodger blue", highlightthickness=0)
        self.quote_shape.create_image(420, 240, image=self.bubble)
        self.quote_shape.place(x=80, y=30)

        self.score = 0
        self.score_label = Label(self.__third, text=f"SCORE: {self.score}", bg="dodger blue",
                                 font=('Arial', 20, 'bold'))
        self.score_label.place(x=20, y=15)

        try:
            question_dict = Questions(category_chosen).ques
        except Exception:
            print("Error:")
        else:
            self.quest_ans_list = list(enumerate(question_dict.items()))
            self.answer_buttons = self.answer_question_prod()
            self.quiz(self.quest_ans_list, 0, 'a', 'b')

    def answer_question_prod(self):
        q_a = []
        OPTIONS = 4
        for i in range(0, OPTIONS):
            b = Button(self.__third, text="", highlightbackground="dodger blue")
            b.place(x=330, y=530 + 40 * i)
            q_a.append(b)
        self.question_txt = self.quote_shape.create_text(435, 250, text="", width=320, font=('Courier', 17, 'bold'),
                                                         fill='red3')
        return q_a

    def quiz(self, question_dict, number_of_questions, selected, correct):
        if selected == correct:
            self.score += 1
            self.score_label.config(text=f"SCORE: {self.score}")

        if number_of_questions < len(question_dict):

            q = html.unescape(question_dict[number_of_questions][1][0])
            self.quote_shape.itemconfig(self.question_txt, text=f"{q}")

            ans = [html.unescape(x) for x in question_dict[number_of_questions][1][1]]
            correct = ans[0]
            random.shuffle(ans)

            number_of_questions += 1
            for i in range(0, len(self.answer_buttons)):
                self.answer_buttons[i].config(text=ans[i],
                                              command=partial(self.quiz, question_dict, number_of_questions, ans[i],
                                                              correct))
        else:
            for i in self.answer_buttons:
                i.destroy()

            self.score_label.destroy()
            self.quote_shape.itemconfig(self.question_txt, text=f"End of the game\nScore: {self.score}/20")

    def categories_to_quiz(self):
        self.__second_screen.withdraw()
        self.__third = Toplevel(self.__second_screen, bg="dodger blue")
        self.__third.title("Quiz 20*")
        self.__third.minsize(1000, 700)

        self.__move_to_second = Button(self.__third, highlightbackground="dodger blue", text="Move to Categories",
                                       command=self.to_categories)
        self.__move_to_second.place(x=10, y=650)

        self.__third.protocol("WM_DELETE_WINDOW", self.shut_down_all)

    def to_categories(self):
        self.__third.destroy()
        self.__second_screen.deiconify()

    def to_start(self):
        self.main_screen.deiconify()
        self.__second_screen.destroy()

    def shut_down_all(self):
        self.__second_screen.destroy()
        self.main_screen.destroy()


scr = Screens()
scr.main_screen.mainloop()