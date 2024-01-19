from itertools import cycle


class TicTacToe:
    def __init__(self, player1='X', player2='O'):
        self.player1 = player1
        self.player1_steps = 0
        self.player2 = player2
        self.player2_steps = 0
        self.player_turn = cycle((self.player1, self.player2))
        self.board = [[''] * 3 for _ in range(3)]
        self.max_value_width = max(map(len, self.board))

    def ask_move(self):
        player = self.change_player()
        player_step = self.player1_steps if player == self.player1 else self.player2_steps

        if not player_step:
            print(self._first_step_warning(player))
        else:
            print(self._non_first_step_warning(player))

        self.draw_board()
        x, y = int(input('Координата х: ')), int(input('Координата y: '))

        while not (0 <= x < 3 and 0 <= y < 3 and self.board[x][y] != 'X' and self.board[x][y] != 'O'):
            print(self._mistake_input_warning())
            x, y = int(input('Координата х: ')), int(input('Координата y: '))
            continue

        print(f"Отлично, теперь ход переходит к сопернику\n")
        return self.make_move(player, x, y)

    def make_move(self, player: str, x: int, y: int):
        self.board[x][y] = player
        match player:
            case self.player1:
                self.player1_steps += 1
            case self.player2:
                self.player2_steps += 1
        self.ask_move()

    @staticmethod
    def check_win(player: str, board: list[list]):
        for i in range(3):
            if board[i] == [player, player, player]:
                return True

            if board[0][i] == player and board[1][i] == player and board[2][i] == player:
                return True

        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return True

        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return True

        return False

    def draw_board(self) -> None:
        for x_coord in range(len(self.board)):
            for y_coord in range(len(self.board)):
                if self.board[x_coord][y_coord]:
                    print(f"{str(self.board[x_coord][y_coord]).center(self.max_value_width)}", end=' ')
                else:
                    print(f"{x_coord},{y_coord}".center(self.max_value_width), end=' ')
                if y_coord < 2:
                    print('|', end=' ')
            print()
            if x_coord < 2:
                print("-" * 16)

    @staticmethod
    def _first_step_warning(player):
        text = (f"Привет, Игрок {player}, пожалуйста посмотрите на доску и выберите координаты на "
                f"которые Вы хотели бы поставить {player},\nпри этом координаты должны быть в "
                f"диапазоне от 0 до 2 включительно:")
        return text

    @staticmethod
    def _non_first_step_warning(player):
        text = (f"\nЧто ж, Игрок {player}, давайте продолжим выбери координаты на "
                f"которые ты хотел бы поставить {player},\nпри этом координаты должны "
                f"быть в диапазоне от 0 до 2 включительно")
        return text

    @staticmethod
    def _mistake_input_warning():
        text = (f"\nВы ввели некоректное число, напомним, координаты должны быть в "
                f"диапазоне от 0 до 2 включительно также следует учесть, чтобы поле\n"
                f"не было занято Вами или соперником ;)")
        return text

    def change_player(self):
        return next(self.player_turn)


try:
    if __name__ == '__main__':
        TicTacToe().ask_move()
except KeyboardInterrupt:
    print("\n\nExiting... Игра прекращена командой консоли")
