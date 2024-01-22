from itertools import cycle


class TicTacToe:
    def __init__(self, player1='X', player2='O'):
        self.player1 = player1
        self.player1_turn = False
        self.player2 = player2
        self.player2_turn = False
        self.steps_taken_number = 0
        self.current_player = cycle((self.player1, self.player2))
        self.board = [[''] * 3 for _ in range(3)]
        self.max_value_width = max(map(len, self.board))

    def ask_move(self):
        # Переключаем игрока
        current_player = next(self.current_player)

        # Пишем тип сообщения в зависимости от того,
        # первый это шаг игрока или нет
        self._print_welcome_message(current_player)

        # Рисуем поле с координатами для наглядности
        self._draw_board()

        # Запрашиваем и проверяем координаты хода
        x, y = self._get_coordinates()

        # Делаем ход
        self._make_move(current_player, x, y)

        # Если игроки сделали меньше 5 ходов нет смысла
        # проверять победителя, запрашиваем следующий ход
        if self.steps_taken_number < 5:
            print(self._opponent_step_warning())
            return self.ask_move()

        # 9 шагов поле заполнено, победитель не выявлен
        # объявляем ничью, запрашиваем новую партию или прощаемся
        elif self.steps_taken_number == 9:
            print(self._draw_declare())
            if self._ask_restart():
                return TicTacToe().ask_move()
            print(self._hope_declare())
            return

        # Проверяем победителя, объявляем,
        # запрашиваем новую партию или прощаемся
        else:
            if self._check_win(current_player, self.board):
                print()
                self._draw_board()
                print(self._winner_warning(current_player))
                if self._ask_restart():
                    return TicTacToe().ask_move()
                print(self._hope_declare())
                return
            print(self._opponent_step_warning())
            return self.ask_move()

    def _make_move(self, player: str, x: int, y: int) -> None:
        self.board[x][y] = player
        match player:
            case self.player1:
                self.player1_turn = True
            case self.player2:
                self.player2_turn = True
        self.steps_taken_number += 1

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

    def _print_welcome_message(self, current_player) -> None:
        if not (self.player1_turn and self.player2_turn):
            print(self._first_step_warning(current_player))
        else:
            print(self._non_first_step_warning(current_player))

    def _get_coordinates(self) -> tuple[int, int]:
        while True:
            xy_coord = input('\nВведите "х" и "y" координаты двузначным числом,\n'
                             'где первое число это координата x, второе координата y: ')
            x_coord, y_coord = int(xy_coord) // 10, int(xy_coord) % 10
            if self._check_right_coord(x_coord, y_coord):
                return x_coord, y_coord
            else:
                print(self._mistake_input_warning())

    def _check_right_coord(self, x, y) -> bool:
        if x == '' or y == '':
            return False
        if not (0 <= x < 3 and 0 <= y < 3):
            return False
        if self.board[x][y] in (self.player1, self.player2):
            return False
        return True

    @staticmethod
    def _first_step_warning(player):
        text = (f"Привет, Игрок {player}, пожалуйста посмотрите на доску и выберите координаты на "
                f"которые Вы хотели бы поставить {player},\nпри этом координаты должны быть в "
                f"диапазоне от 0 до 2 включительно:\n")
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

    @staticmethod
    def _draw_declare():
        return "\nУважаемые игроки, у вас ничья ;)"

    @staticmethod
    def _opponent_step_warning():
        return "\nОтлично, теперь ход переходит к сопернику\n"

    @staticmethod
    def _hope_declare():
        return "\nОк, тогда до встречи, надеюсь, увидимся снова ;)"


try:
    if __name__ == '__main__':
        TicTacToe().ask_move()
except KeyboardInterrupt:
    print("\n\nExiting... Игра прекращена командой консоли")
