from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"

try:
    words_to_learn = pandas.read_csv('data/unknown_words.csv')
    words = words_to_learn.to_dict(orient='records')
except FileNotFoundError:
    data = pandas.read_csv('data/french_words.csv')
    words = data.to_dict(orient='records')
except pandas.errors.EmptyDataError:
    data = pandas.read_csv('data/french_words.csv')
    words = data.to_dict(orient='records')

random_word = {}

def next_card():
    global random_word, card_timer
    window.after_cancel(card_timer)
    random_word = random.choice(words)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=random_word['French'], fill='black')
    canvas.itemconfig(card_img, image=front_img)
    card_timer = window.after(3000, func=flip_card)

def flip_card():
    global random_word
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=random_word['English'], fill='white')
    canvas.itemconfig(card_img, image=back_img)

def known_word():
    global random_word
    words.remove(random_word)
    new_data = pandas.DataFrame(words)
    new_data.to_csv('data/unknown_words.csv', index=False)
    next_card()




window = Tk()
window.title('FlashCard')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file='images/card_front.png')
back_img = PhotoImage(file='images/card_back.png')
card_img = canvas.create_image(400, 263, image=front_img)
card_title = canvas.create_text(400, 150, text='', font=('Arial', 40, 'italic'))
card_word = canvas.create_text(400, 250, text='', font=('Arial', 60, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

cancel_img = PhotoImage(file='images/wrong.png')
cancel_btn = Button(image=cancel_img, highlightthickness=0, command=next_card)
cancel_btn.grid(row=1, column=0)

check_img = PhotoImage(file='images/right.png')
check_btn = Button(image=check_img, highlightthickness=0, command=known_word)
check_btn.grid(row=1, column=1)

next_card()

window.mainloop()

