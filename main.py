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
            print(f"Привет, Игрок {player}, пожалуйста посмотрите на доску и "
                  f"выберите координаты на которые Вы хотели бы поставить {player},\n"
                  f"при этом координаты должны быть в диапазоне от 0 до 2 включительно\n")
        else:
            print(f"\nЧто ж, Игрок {player}, давай продолжим "
                  f"выбери координаты на которые ты хотел бы поставить {player},\n"
                  f"при этом координаты должны быть в диапазоне от 0 до 2 включительно\n")
        self.draw_board()
        x, y = int(input('Координата х: ')), int(input('Координата y: '))

        while not (0 <= x < 3 and 0 <= y < 3 and self.board[x][y] != 'X' and self.board[x][y] != 'O'):
            print(f"\nВы ввели некоректное число, напомним, координаты должны быть "
                  f"в диапазоне от 0 до 2 включительно также следует учесть, чтобы поле\n"
                  f"не было занято Вами или соперником ;)")
            x, y = int(input('Координата х: ')), int(input('Координата y: '))
            continue
        print(f"Отлично, теперь ход пеерходит к сопернику\n")
        return self.make_move(player, x, y)

    def make_move(self, player: str, x: int, y: int):
        self.board[x][y] = player
        match player:
            case self.player1:
                self.player1_steps += 1
            case self.player2:
                self.player2_steps += 1
        self.ask_move()

    def check_win(self, player: str, board: list[list]):
        pass

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

    def change_player(self):
        return next(self.player_turn)


try:
    if __name__ == '__main__':
        TicTacToe().ask_move()
except KeyboardInterrupt:
    print("\n\nExiting... Игра прекращена через консоль")
