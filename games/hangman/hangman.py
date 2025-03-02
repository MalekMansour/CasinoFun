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
        self.entry = tk.Entry(self.root, font=("Helvetica", 24))
        self.entry.pack(pady=20)
        self.entry.bind("<Return>", self.check_guess)
        self.draw_hangman()

    def update_word_display(self):
        display = " ".join([letter if letter in self.guesses else "_" for letter in self.word])
        self.word_display.set(display)

    def check_guess(self, event):
        guess = self.entry.get().upper()
        self.entry.delete(0, tk.END)
        if guess in self.guesses or len(guess) != 1 or not guess.isalpha():
            return
        self.guesses.append(guess)
        if guess not in self.word:
            self.mistakes += 1
            self.draw_hangman()
        self.update_word_display()
        self.check_game_over()

    def draw_hangman(self):
        self.canvas.delete("hangman")
        if self.mistakes > 0:
            self.canvas.create_line(100, 350, 300, 350, tags="hangman")  # Base
        if self.mistakes > 1:
            self.canvas.create_line(200, 350, 200, 50, tags="hangman")  # Pole
        if self.mistakes > 2:
            self.canvas.create_line(200, 50, 300, 50, tags="hangman")  # Top bar
        if self.mistakes > 3:
            self.canvas.create_line(300, 50, 300, 100, tags="hangman")  # Rope
        if self.mistakes > 4:
            self.canvas.create_oval(275, 100, 325, 150, tags="hangman")  # Head
        if self.mistakes > 5:
            self.canvas.create_line(300, 150, 300, 250, tags="hangman")  # Body
        if self.mistakes > 6:
            self.canvas.create_line(300, 170, 250, 200, tags="hangman")  # Left arm
            self.canvas.create_line(300, 170, 350, 200, tags="hangman")  # Right arm
            self.canvas.create_line(300, 250, 250, 300, tags="hangman")  # Left leg
            self.canvas.create_line(300, 250, 350, 300, tags="hangman")  # Right leg

    def check_game_over(self):
        if "_" not in self.word_display.get():
            self.end_game("Congratulations! You won!")
        elif self.mistakes >= self.max_mistakes:
            self.end_game(f"Game Over! The word was {self.word}")

    def end_game(self, message):
        self.entry.unbind("<Return>")
        self.entry.config(state="disabled")
        self.label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()