import tkinter as tk
from random import choice

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.word_list = self.load_words()
        self.word = choice(self.word_list).upper()
        self.guesses = []
        self.mistakes = 0
        self.max_mistakes = 6
        self.setup_ui()

    def load_words(self):
        with open("games/hangman/words.txt", "r") as file:
            words = file.read().splitlines()
        return words

    def setup_ui(self):
        self.word_display = tk.StringVar()
        self.update_word_display()
        self.label = tk.Label(self.root, textvariable=self.word_display, font=("Helvetica", 24))
        self.label.pack(pady=20)
        self.letter_frame = tk.Frame(self.root)
        self.letter_frame.pack(pady=20)
        self.create_letter_buttons()
        self.draw_hangman()

    def create_letter_buttons(self):
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            button = tk.Button(self.letter_frame, text=letter, font=("Helvetica", 18), width=4, command=lambda l=letter: self.check_guess(l))
            button.grid(row=(ord(letter) - 65) // 9, column=(ord(letter) - 65) % 9)

    def update_word_display(self):
        display = " ".join([letter if letter in self.guesses else "_" for letter in self.word])
        self.word_display.set(display)

    def check_guess(self, guess):
        if guess in self.guesses or not guess.isalpha():
            return
        self.guesses.append(guess)
        button = self.letter_frame.grid_slaves(row=(ord(guess) - 65) // 9, column=(ord(guess) - 65) % 9)[0]
        button.config(state="disabled", disabledforeground="grey")
        if guess not in self.word:
            self.mistakes += 1
            self.draw_hangman()
        self.update_word_display()
        self.check_game_over()

    def draw_hangman(self):
        self.canvas.delete("hangman")
        self.canvas.create_line(100, 350, 300, 350, tags="hangman")  
        self.canvas.create_line(200, 350, 200, 50, tags="hangman")  
        self.canvas.create_line(200, 50, 300, 50, tags="hangman")  
        self.canvas.create_line(300, 50, 300, 100, tags="hangman")  
        
        # Draw the parts based on the number of mistakes
        if self.mistakes > 0:
            self.canvas.create_oval(275, 100, 325, 150, tags="hangman")  # Head
        if self.mistakes > 1:
            self.canvas.create_line(300, 150, 300, 250, tags="hangman")  # Body
        if self.mistakes > 2:
            self.canvas.create_line(300, 170, 250, 200, tags="hangman")  # Left arm
        if self.mistakes > 3:
            self.canvas.create_line(300, 170, 350, 200, tags="hangman")  # Right arm
        if self.mistakes > 4:
            self.canvas.create_line(300, 250, 250, 300, tags="hangman")  # Left leg
        if self.mistakes > 5:
            self.canvas.create_line(300, 250, 350, 300, tags="hangman")  # Right leg

    def check_game_over(self):
        if "_" not in self.word_display.get():
            self.end_game(f"Congratulations! You won! The word was {self.word}")
        elif self.mistakes >= self.max_mistakes:
            self.end_game(f"Game Over! The word was {self.word}")

    def end_game(self, message):
        for button in self.letter_frame.winfo_children():
            button.config(state="disabled")
        self.label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()