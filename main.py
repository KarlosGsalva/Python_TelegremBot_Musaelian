from itertools import cycle


class TicTacToe:
    def __init__(self, player1='X', player2='O'):
        self.player1 = player1
        self.player1_steps = False
        self.player2 = player2
        self.player2_steps = False
        self.current_player = cycle((self.player1, self.player2))
        self.board = [[''] * 3 for _ in range(3)]
        self.max_value_width = max(map(len, self.board))

    def ask_move(self):
        current_player = self.change_player()
        player_step = self.player1_steps if current_player == self.player1 else self.player2_steps

        if not player_step:
            print(self._first_step_warning(current_player))
        else:
            print(self._non_first_step_warning(current_player))

        self._draw_board()
        x, y = int(input('Координата х: ')), int(input('Координата y: '))

        while not self._check_right_coord(x, y, self.board):
            print(self._mistake_input_warning())
            x, y = int(input('Координата х: ')), int(input('Координата y: '))

        self._make_move(current_player, x, y)

        if self._check_win(current_player, self.board):
            print()
            self._draw_board()
            print(self._winner_warning(current_player))
            if self._ask_restart():
                return TicTacToe().ask_move()
            print("\nОк, тогда до встречи, надеюсь, увидимся снова ;)")
            return
        print(f"\nОтлично, теперь ход переходит к сопернику\n")
        return self.ask_move()

    def _make_move(self, player: str, x: int, y: int):
        self.board[x][y] = player
        match player:
            case self.player1:
                self.player1_steps = True
            case self.player2:
                self.player2_steps = True

    @staticmethod
    def _check_win(player: str, board: list[list]):
        for i in range(3):
            # Проверка по горизонтали
            if board[i] == [player, player, player]:
                return True

            # Проверка по вертикали
            if board[0][i] == player and board[1][i] == player and board[2][i] == player:
                return True

        # Проверка по диагонали слева направо
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return True

        # Проверка по диагонали справа налево
        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return True

        return False

    def _draw_board(self) -> None:
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
    def _check_right_coord(x, y, board) -> bool:
        return 0 <= x < 3 and 0 <= y < 3 and board[x][y] not in ('X', 'O')

    @staticmethod
    def _first_step_warning(player):
        text = (f"Привет, Игрок {player}, пожалуйста посмотрите на доску и выберите координаты на "
                f"которые Вы хотели бы поставить {player},\nпри этом координаты должны быть в "
                f"диапазоне от 0 до 2 включительно:")
        return text

    @staticmethod
    def _non_first_step_warning(player):
        text = (f"Что ж, Игрок {player}, давайте продолжим выбери координаты на "
                f"которые ты хотел бы поставить {player},\nпри этом координаты должны "
                f"быть в диапазоне от 0 до 2 включительно, также учтите, что место, \n"
                f"по указанным координатам на поле, не должно быть занято ;)\n")
        return text

    @staticmethod
    def _mistake_input_warning():
        text = (f"\nВы ввели некоректное число, напомним, координаты должны быть в "
                f"диапазоне от 0 до 2 включительно\n"
                f"также следует учесть, чтобы поле не было занято Вами или соперником ;)")
        return text

    @staticmethod
    def _winner_warning(player):
        text = f"\nИтак у нас появился победитель, Игрок {player}, поздравляем ;) !"
        return text

    @staticmethod
    def _ask_restart():
        restart = input("\nХотите сыграть еще раз? Нажмите (y/n) или (1/0),\n"
                        "где 'y' или '1' это согласие на начало новой игры: ")
        return restart.lower() in ('y', '1')

    def change_player(self):
        return next(self.current_player)


try:
    if __name__ == '__main__':
        TicTacToe().ask_move()
except KeyboardInterrupt:
    print("\n\nExiting... Игра прекращена командой консоли")
