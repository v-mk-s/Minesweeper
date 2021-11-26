import random
import json


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_error(s):
    print(bcolors.FAIL + s + bcolors.ENDC)


def print_success(s):
    print(bcolors.OKGREEN + s + bcolors.ENDC)


def print_help():
    help_msg = """\n Enter the coordinates of the cell, as well as the command in the form of a triplet. For example: 2, 3, Open. If you want to open cell,
     2, 3, Flag. If you want to put flag. You can remove flag by typing the same command. \n"""
    print(bcolors.OKBLUE + help_msg + bcolors.ENDC)


class Game:

    def __init__(self):
        pass

    def generateMines(self):
        mines = []

        for i in range(self.n_mines):
            row, col = self.getRandomCell()
            if [row, col] not in mines:
                mines.append((row, col))

        return mines


    def getNeighbors(self, row, col):
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (row + i) < self.gridHeight and -1 < (col + j) < self.gridWidth:
                    neighbors.append((row + i, col + j))

        return neighbors

    def showGrid(self, grid):
        horizontal = '   ' + (4 * self.gridWidth * '-') + '-'

        print('     ', end='')

        for i in range(self.gridWidth):
            print(bcolors.OKBLUE + str(i + 1) + bcolors.ENDC + '   ', end='')

        print('\n' + horizontal)

        for idx, i in enumerate(grid):
            print(bcolors.OKBLUE + str(idx + 1) + bcolors.ENDC + '  |', end='')

            for j in i:
                if j == '0':
                    print(bcolors.OKGREEN + ' ' + j + bcolors.ENDC + ' |', end='')
                elif j == 'X':
                    print(bcolors.FAIL + ' ' + j + bcolors.ENDC + ' |', end='')
                elif j == 'F':
                    print(bcolors.HEADER + ' ' + j + bcolors.ENDC + ' |', end='')
                else:
                    print(bcolors.WARNING + ' ' + j + bcolors.ENDC + ' |', end='')

            print('   ' + bcolors.OKBLUE + str(idx + 1) + bcolors.ENDC, end='')

            print('\n' + horizontal)

        print('      ', end='')
        for i in range(self.gridWidth):
            print(bcolors.OKBLUE + str(i + 1) + bcolors.ENDC + '   ', end='')

        print('\n\n')

    def getRandomCell(self):
        row = random.randint(0, self.gridHeight - 1)
        col = random.randint(0, self.gridWidth - 1)
        return (row, col)

    def getNumberOfNearMines(self):
        for row_idx, row in enumerate(self.private_grid):
            for col_idx, cell in enumerate(row):
                if cell != 'X':
                    values = [self.private_grid[r][c] for r, c in self.getNeighbors(row_idx, col_idx)]
                    self.private_grid[row_idx][col_idx] = str(values.count('X'))

    def showMoreCells(self, row, col):
        if self.public_grid[row][col] != ' ':
            return

        self.public_grid[row][col] = self.private_grid[row][col]

        if self.private_grid[row][col] == '0':
            for r, c in self.getNeighbors(row, col):
                if self.public_grid[r][c] != 'F':
                    self.showMoreCells(r, c)

    def save_game(self):
        data = {
            'grid_width': self.gridWidth,
            'grid_height': self.gridHeight,
            'public-grid': self.public_grid,
            'private-grid': self.private_grid,
            'n_mines': self.n_mines,
            'mines': self.mines,
            'flags': self.flags
        }

        with open('./data.txt', 'w') as outfile:
            json.dump(data, outfile)

    def load_saved_game(self):
        try:
            with open('./data.txt') as json_file:
                data = json.load(json_file)
                self.gridWidth = data['grid_width']
                self.gridHeight = data['grid_height']
                self.public_grid = data['public-grid']
                self.private_grid = data['private-grid']
                self.n_mines = data['n_mines']
                self.mines = data['mines']
                self.flags = data['flags']
            return 1
        except:
            return 0

    def main(self):

        has_saved_game = False

        if self.load_saved_game():
            print('Last incomplete batch found, continue?')

            ans = input('Yes/No: ')

            if ans == 'Yes':
                has_saved_game = True
        else:
            print('No last unfinished game found, create a new game')
            has_saved_game = False

        if has_saved_game:
            self.load_saved_game()
        else:
            self.gridWidth = int(input('Enter width of grid: '))
            self.gridHeight = int(input('Enter height of grid: '))
            self.n_mines = int(input('Enter mines amount: '))
            self.public_grid = [[' ' for i in range(self.gridWidth)] for i in range(self.gridHeight)]
            self.private_grid = [[' ' for i in range(self.gridWidth)] for i in range(self.gridHeight)]
            self.mines = self.generateMines()
            self.flags = []

            for i, j in self.mines:
                self.private_grid[i][j] = 'X'

            self.getNumberOfNearMines()

        is_first_time = True
        while True:
            if is_first_time:
                self.showGrid(self.public_grid)
                is_first_time = False

            opened_by_user = []
            for i in range(len(self.public_grid)):
                for j in range(len(self.public_grid[i])):
                    if self.public_grid[i][j] != ' ' and self.public_grid[i][j] != 'F':
                        opened_by_user.append((i, j))

            opened_private = []
            for i in range(len(self.private_grid)):
                for j in range(len(self.private_grid[i])):
                    if self.private_grid[i][j] != 'X':
                        opened_private.append((i, j))

            opened_by_user_total = len(set(opened_by_user) & set(opened_private))
            total_with_no_mines = len(opened_private)
            print_help()
            prompt = input('Choose cell ({} cels remain to de-mine): '.format(total_with_no_mines - opened_by_user_total))
            result = prompt.split(',')
            col, row, action = int(result[0]) - 1, int(result[1]) - 1, result[2].strip()

            if (-1 < col <= self.gridWidth) and (-1 < row <= self.gridHeight):

                print('\n')

                if action == 'Flag':
                    if self.public_grid[row][col] == ' ':
                        self.public_grid[row][col] = 'F'
                        self.flags.append([row, col])
                        self.showGrid(self.public_grid)
                    elif self.public_grid[row][col] == 'F':
                        self.public_grid[row][col] = ' '
                        self.flags.remove([row, col])
                        self.showGrid(self.public_grid)
                    else:
                        print_error("Can't put flag here")

                elif action == 'Open':
                    if self.private_grid[row][col] == 'X':
                        self.public_grid[row][col] = 'X'
                        self.showGrid(self.public_grid)
                        return print_error('You lost!')
                    else:
                        self.showMoreCells(row, col)
                        self.showGrid(self.public_grid)

                else:
                    print_error('Unknow command')

            else:
                print_error('There is no such cell')

            # Cells that player has not opened yet
            hidden_cells = []
            for row_id, row in enumerate(self.public_grid):
                for col_id, cell in enumerate(row):
                    if cell == ' ' or cell == 'F':
                        hidden_cells.append((row_id, col_id))

            if len(hidden_cells) == len(self.mines):
                return print_success('You won!')

            print('\n')
            self.save_game()


game = Game()

game.main()