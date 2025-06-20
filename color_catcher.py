import tkinter as tk
import random

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
BALL_SIZE = 30
BASKET_WIDTH = 100
BASKET_HEIGHT = 20
START_SPEED = 5
BALL_INTERVAL = 1000  # ms

class ColorCatcher:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Color Catcher Game")

        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="#e0f7fa")
        self.canvas.pack()

        # Game variables
        self.score = 0
        self.lives = 3
        self.speed = START_SPEED
        self.balls = []
        self.running = True

        # UI elements
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text="Score: 0", font=("Arial", 16, "bold"))
        self.lives_text = self.canvas.create_text(10, 35, anchor="nw", text="Lives: 3", font=("Arial", 14))

        # Basket
        self.basket = self.canvas.create_rectangle(
            WINDOW_WIDTH // 2 - BASKET_WIDTH // 2,
            WINDOW_HEIGHT - BASKET_HEIGHT - 10,
            WINDOW_WIDTH // 2 + BASKET_WIDTH // 2,
            WINDOW_HEIGHT - 10,
            fill="#007acc", outline="black", width=2
        )

        # Bind keys
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)

        # Start game
        self.spawn_ball()
        self.update_game()

    def move_left(self, event):
        self.canvas.move(self.basket, -25, 0)

    def move_right(self, event):
        self.canvas.move(self.basket, 25, 0)

    def spawn_ball(self):
        x = random.randint(0, WINDOW_WIDTH - BALL_SIZE)
        color = random.choice(["green", "red", "green", "green"])  # More green than red
        ball = self.canvas.create_oval(x, 0, x + BALL_SIZE, BALL_SIZE, fill=color, outline="black")
        self.balls.append((ball, color))
        if self.running:
            self.root.after(BALL_INTERVAL, self.spawn_ball)

    def update_game(self):
        to_remove = []
        for ball, color in self.balls:
            self.canvas.move(ball, 0, self.speed)
            coords = self.canvas.coords(ball)
            basket_coords = self.canvas.coords(self.basket)

            # Check if ball hits basket
            if coords[3] >= basket_coords[1]:
                if self.check_overlap(coords, basket_coords):
                    if color == "green":
                        self.score += 1
                    else:
                        self.lives -= 1
                    to_remove.append((ball, color))
                    self.update_ui()
                elif coords[3] > WINDOW_HEIGHT:
                    to_remove.append((ball, color))

        for item in to_remove:
            self.canvas.delete(item[0])
            if item in self.balls:
                self.balls.remove(item)

        if self.lives <= 0:
            self.end_game()
        elif self.running:
            # Increase difficulty as score rises
            if self.score % 5 == 0 and self.score != 0:
                self.speed = START_SPEED + self.score // 5
            self.root.after(30, self.update_game)

    def check_overlap(self, ball_coords, basket_coords):
        return (
            ball_coords[2] > basket_coords[0] and
            ball_coords[0] < basket_coords[2]
        )

    def update_ui(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")

    def end_game(self):
        self.running = False
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
            text="Game Over\nPress Esc to Exit",
            font=("Arial", 24, "bold"),
            fill="red",
            justify="center"
        )
        self.canvas.bind_all("<KeyPress-Escape>", lambda e: self.root.destroy())

def main():
    root = tk.Tk()
    game = ColorCatcher(root)
    root.mainloop()

main()
