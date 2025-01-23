import sys


class Dice:
    def __init__(self, faces):
        if len(faces) < 2:
            print("Each dice must have at least 2 sides.")
            sys.exit()
        self.faces = faces

class DiceParser:
    def parse_dice_parameters(self, args):
        dice_list = []
        if args:
            line = ' '.join(args).strip()
        else:
            print("No dice provided. Example: python main.py 1,2,3 4,5 6,7,8,9")
            sys.exit()

        try:
            dice_groups = line.split()
            for group in dice_groups:
                dice = list(map(int, group.split(',')))
                dice_list.append(Dice(dice))
            if len(dice_list) < 3:
                print("You must provide at least 3 dice.")
                sys.exit()
        except ValueError:
            print("Invalid input. Please ensure all dice faces are integers.")
            sys.exit()
        return dice_list