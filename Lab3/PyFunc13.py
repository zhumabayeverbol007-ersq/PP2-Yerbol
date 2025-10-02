import random

def guess_the_number():
    name = input("Hello! What is your name?\n")
    print(f"\nWell, {name}, I am thinking of a number between 1 and 20.")

    number = random.randint(1, 20)

    print("Guess the number (1-20)! Enter 'q' to quit.")

    while True:
        guess = input("Enter your guess: ")
        if guess.lower() == 'q': 
            print("You exited the game. Goodbye!")
            break
        elif guess.isdigit():
            guess = int(guess)
            if guess > number:
                print("Too high!")
            elif guess < number:
                print("Too low!")
            else:
                print(f"Congratulations, {name}! You guessed it!")
                break
        else:
            print("Please enter a valid number or 'q' to quit.")

guess_the_number()
