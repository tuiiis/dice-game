import random
import sys
from game.dice import DiceParser
from game.hmac_protocol import RandomGenerator
from game.odds import ProbabilityCalculator, TableGenerator

class DiceGame:
    def __init__(self):
        print("Starting the Dice Game...")
        self.dice_parser = DiceParser()
        self.random_generator = RandomGenerator()
        self.probability_calculator = ProbabilityCalculator()
        self.table_generator = TableGenerator()
        self.full_dice_list = None
        self.chances = None

    def choose_dice_index(self, dice_list, player):
        while True:
            print("\nAvailable dice:")
            for i, dice in enumerate(dice_list):
                print(f"{i} - {dice.faces}")
            print("X - exit\n? - help")
            choice = input(f"{player}, choose a dice index: ").strip().lower()
            if choice == 'x':
                print("Game exited.")
                exit()
            elif choice == '?':
                    self.table_generator.display_chances(self.full_dice_list, self.chances)
            else:
                try:
                    index = int(choice)
                    if 0 <= index < len(dice_list):
                        print(f"{player} chose dice: {dice_list[index].faces}")
                        return index
                    else:
                        print("Invalid choice. Try again.")
                except ValueError:
                    print("Invalid input. Try again.")

    def throw_dice(self, dice, player):
        secret_key = self.random_generator.generate_random_bytes(32)
        throw_index = self.random_generator.generate_random_int(len(dice.faces))
        #throw_value = dice.faces[throw_index]
        hmac_value = self.random_generator.compute_hmac(secret_key, str(throw_index))
        print(f"HMAC for dice throw: {hmac_value}")

        modulo_choice = None
        while modulo_choice is None:
            print("\nAdd your number modulo (choose a value):")
            options = [f"{i} - {i}" for i in range(len(dice.faces))] + ['? - help', 'X - exit']
            print("\n".join(options))
            choice = input("user chose modulo: ").strip().lower()
            if choice == 'x':
                print("Game exited.")
                exit()
            elif choice == '?':
                print(f"Choose a modulo number between 0 and {len(dice.faces) - 1}.")
            else:
                try:
                    modulo_choice = int(choice)
                    if 0 <= modulo_choice < len(dice.faces):
                        break
                    else:
                        print("Invalid modulo. Try again.")
                except ValueError:
                    print("Invalid input. Try again.")

        print(f"The dice throw: {throw_index}")
        print(f"Secret key: {secret_key.hex()}")

        result = (modulo_choice + throw_index) % len(dice.faces)
        print(f"The result is {modulo_choice} + {throw_index} % {len(dice.faces)} = {result}")
        print(f"{dice.faces}[{result}] = {dice.faces[result]}")
        return dice.faces[result]

    def play(self):
        self.full_dice_list = self.dice_parser.parse_dice_parameters(sys.argv[1:])
        print(f"Dice parameters: {[dice.faces for dice in self.full_dice_list]}")

        # Store chances in the instance attribute
        self.chances = self.probability_calculator.calculate_chances(self.full_dice_list)
        dice_list = self.full_dice_list[:]

        secret_key = self.random_generator.generate_random_bytes(32)
        computer_value = self.random_generator.generate_random_int(2)
        hmac_value = self.random_generator.compute_hmac(secret_key, str(computer_value))
        print(f"HMAC: {hmac_value}")

        user_value = None
        while user_value not in [0, 1]:
            try:
                user_value = int(input("Choose a value (0 or 1): "))
            except ValueError:
                pass
            if user_value not in [0, 1]:
                print("Invalid input. Please choose 0 or 1.")

        print(f"Computer's value: {computer_value}")
        print(f"Secret key: {secret_key.hex()}")

        user_guessed_correctly = computer_value == user_value
        if user_guessed_correctly:
            print("You guessed correctly! You go first.")
            user_dice_index = self.choose_dice_index(dice_list, "user")
            user_dice = dice_list.pop(user_dice_index)
            computer_dice_index = random.choice(range(len(dice_list)))
            computer_dice = dice_list.pop(computer_dice_index)
            print(f"Computer chose dice: {computer_dice.faces}")
        else:
            print("You guessed incorrectly. Computer goes first.")
            computer_dice_index = random.choice(range(len(dice_list)))
            computer_dice = dice_list.pop(computer_dice_index)
            print(f"Computer chose dice: {computer_dice.faces}")
            user_dice_index = self.choose_dice_index(dice_list, "user")
            user_dice = dice_list.pop(user_dice_index)

        print("\nIt's the computer's turn to throw the dice.")
        computer_points = self.throw_dice(computer_dice, "computer")

        print("\nIt's your turn to throw the dice.")
        user_points = self.throw_dice(user_dice, "user")

        print(f"\nFinal Points:\nUser points: {user_points}\nComputer points: {computer_points}")

        if user_points > computer_points:
            print("You win!")
        elif user_points < computer_points:
            print("Computer wins!")
        else:
            print("It's a tie!")
