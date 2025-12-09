import turtle
import random
import time

# -------------------------------
# CONFIG
# -------------------------------
STARTING_HEALTH = 3
SCORE_PER_WIN = 10
HARD_MODE_START = 6
ZODIAC_HEALTH = 3       # <-- How many questions per zodiac
BOSS_HEALTH = 5         # <-- More questions for boss

# List of zodiac names + symbols
zodiacs = [
    ("Aries", "♈"), ("Taurus", "♉"), ("Gemini", "♊"), ("Cancer", "♋"),
    ("Leo", "♌"), ("Virgo", "♍"), ("Libra", "♎"), ("Scorpio", "♏"),
    ("Sagittarius", "♐"), ("Capricorn", "♑"), ("Aquarius", "♒")
]

FINAL_BOSS = ("Pisces — The Zodiac Overlord", "♓")

# -------------------------------
# SCREEN SETUP
# -------------------------------
screen = turtle.Screen()
screen.title("Turtle vs. Zodiac — Multi-Battle Edition!")
screen.bgcolor("black")

player = turtle.Turtle()
player.shape("turtle")
player.color("lightgreen")
player.turtlesize(2.5)      # <-- Bigger turtle
player.penup()
player.goto(0, -200)

# Writer turtles
writer = turtle.Turtle()
writer.hideturtle()
writer.color("white")
writer.penup()

hud = turtle.Turtle()
hud.hideturtle()
hud.color("cyan")
hud.penup()
hud.goto(-270, 250)

# Zodiac symbol display
symbol_turtle = turtle.Turtle()
symbol_turtle.hideturtle()
symbol_turtle.color("yellow")
symbol_turtle.penup()

# -------------------------------
# HUD FUNCTIONS
# -------------------------------
def update_hud(score, health):
    hud.clear()
    hud.write(f"Score: {score}   Health: {health}",
              font=("Courier", 16, "bold"))

def show_message(msg, y=0, size=20, color="white"):
    writer.clear()
    writer.goto(0, y)
    writer.color(color)
    writer.write(msg, align="center", font=("Courier", size, "bold"))

def show_symbol(symbol):
    symbol_turtle.clear()
    symbol_turtle.goto(0, 100)
    symbol_turtle.write(symbol, align="center",
                        font=("Courier", 60, "bold"))

def hide_symbol():
    symbol_turtle.clear()

# -------------------------------
# PROBLEM GENERATOR
# -------------------------------
def generate_problem(hard_mode=False, boss=False):
    ops = ["+", "-", "*", "/"]
    op = random.choice(ops)

    # difficulty levels
    if boss:
        a = random.randint(20, 60)
        b = random.randint(2, 20)
    elif hard_mode:
        a = random.randint(10, 25)
        b = random.randint(1, 15)
    else:
        a = random.randint(1, 10)
        b = random.randint(1, 10)

    if op == "/":
        a = a * b  # clean division

    if op == "+": answer = a + b
    elif op == "-": answer = a - b
    elif op == "*": answer = a * b
    elif op == "/": answer = a // b

    return f"What is {a} {op} {b} ?", answer

# -------------------------------
# BATTLE FUNCTION (MULTI-QUESTION)
# -------------------------------
def battle(zodiac_name, zodiac_symbol, score, health,
           hard_mode=False, boss=False):
    # Show zodiac symbol
    show_symbol(zodiac_symbol)

    # Set health
    enemy_health = BOSS_HEALTH if boss else ZODIAC_HEALTH

    show_message(f"{zodiac_name} challenges you!", 180, 22, "yellow")
    time.sleep(1)

    # Multi-question battle
    while enemy_health > 0 and health > 0:
        question, correct = generate_problem(hard_mode, boss)
        show_message(f"{question}", 80, 20)

        attempt = screen.textinput("Math Question", question)

        if attempt and attempt.replace("-", "").isdigit():
            if int(attempt) == correct:
                enemy_health -= 1
                show_message(f"Hit! {zodiac_name} HP: {enemy_health}",
                             0, 22, "lightgreen")
                score += SCORE_PER_WIN
            else:
                health -= 1
                show_message(f"Wrong! You took damage! HP:{health}",
                             0, 22, "red")
        else:
            health -= 1
            show_message(f"Invalid input! HP:{health}",
                         0, 22, "red")

        update_hud(score, health)
        time.sleep(1)

    hide_symbol()
    return enemy_health == 0, score, health

# -------------------------------
# MAIN GAME LOOP
# -------------------------------
score = 0
health = STARTING_HEALTH
update_hud(score, health)

for i, (name, symbol) in enumerate(zodiacs):
    hard_mode = i >= HARD_MODE_START

    won, score, health = battle(name, symbol, score, health, hard_mode)

    if not won:
        show_message("💀 GAME OVER — You lost!", -20, 26, "red")
        screen.mainloop()
        exit()

# -------------------------------
# FINAL BOSS
# -------------------------------
boss_name, boss_symbol = FINAL_BOSS

show_message("⚡ FINAL BOSS APPROACHES ⚡", 180, 26, "yellow")
time.sleep(2)

won, score, health = battle(
    boss_name, boss_symbol, score, health, hard_mode=True, boss=True
)

if won:
    show_message("🏆 YOU DEFEATED THE ZODIAC OVERLORD! YOU WIN!",
                 -20, 26, "lightgreen")
else:
    show_message("💀 The Zodiac Boss Defeated You!", -20, 26, "red")

screen.mainloop()
