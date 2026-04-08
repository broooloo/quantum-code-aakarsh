import random

while True:
    input("Press Enter to roll the dice 🎲")
    print("You got:", random.randint(1, 6))

    again = input("Roll again? (y/n): ")
    if again.lower() != 'y':
        break
