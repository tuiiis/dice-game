from tabulate import tabulate

class ProbabilityCalculator:
    def calculate_chances(self, dice_list):
        n = len(dice_list)
        chances = [[0.0 for _ in range(n)] for _ in range(n)]

        for i, dice1 in enumerate(dice_list):
            for j, dice2 in enumerate(dice_list):
                if i == j:
                    continue
                wins = 0
                total = 0
                for face1 in dice1.faces:
                    for face2 in dice2.faces:
                        if face1 > face2:
                            wins += 1
                        total += 1
                chances[i][j] = wins / total
        return chances

class TableGenerator:
    def display_chances(self, all_dice_list, chances):
        headers = ["User dice v"] + [','.join(map(str, dice.faces)) for dice in all_dice_list]
        table = []
        for i, dice in enumerate(all_dice_list):
            row = [','.join(map(str, dice.faces))]
            for j, chance in enumerate(chances[i]):
                if i == j:
                    row.append(f"- ({1 - chance:.4f})")
                else:
                    row.append(f"{chance:.4f}")
            table.append(row)
        print("Probability of the win for the user:")
        print(tabulate(table, headers=headers, tablefmt="grid"))
