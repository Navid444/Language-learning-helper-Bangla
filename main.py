from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
data = None

try:
    data = pandas.read_csv(
        "data/words_to_learn.csv", header=None, names=["Bangla", "English"]
    )

except FileNotFoundError:
    original_data = pandas.read_csv(
        "data/hard_bangla_words.csv", header=None, names=["Bangla", "English"]
    )
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    screen.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Bangla", fill="black")
    canvas.itemconfig(card_word, text=current_card["Bangla"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = screen.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_image)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


screen = Tk()
screen.title("Flash Card")
screen.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = screen.after(3000, func=flip_card)


card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
right_checkmark_image = PhotoImage(file="images/right.png")
wrong_chechmark_image = PhotoImage(file="images/wrong.png")


canvas = Canvas(width=800, height=526)
card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic", "bold"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


unknown_button = Button(
    image=wrong_chechmark_image,
    bg=BACKGROUND_COLOR,
    highlightthickness=0,
    command=next_card,
)
unknown_button.grid(column=0, row=1)

known_button = Button(
    image=right_checkmark_image,
    bg=BACKGROUND_COLOR,
    highlightthickness=0,
    command=is_known,
)
known_button.grid(column=1, row=1)


next_card()


screen.mainloop()
