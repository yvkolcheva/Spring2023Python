
import typing as tp
import pathlib
import random

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)



def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
     Сгруппировать значения values в список, состоящий из списков по n элементов

     >>> group([1,2,3,4], 2)
     [[1, 2], [3, 4]]
     >>> group([1,2,3,4,5,6,7,8,9], 3)
     [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
     """
    a = []
    for i in range(n):
        a.append(values[i * n: (i + 1) * n])
    return a



def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]
    pass


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return list(posi[pos[1]] for posi in grid)
    pass


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row = 3 * (pos[0] // 3)
    col = 3 * (pos[1] // 3)
    finish = []
    for i in range(3):
        for j in range(3):
            finish.append(grid[row + i][col + j])
    return finish
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    
    Внизу второй вариант кода, который мне жалко было стрирать из-за того, что я слишком долго над ним билась,
    да, он абсолютно не эффективен, но тоже рабочий
    a,b,c=[],[],[]
    au=1
    l=0
    m=0
    aaa=0
    for i in grid: a.append(group(i,3))
    for j in a:
        if au==0:
            au=2
            continue

        if au==2:
            au=1
            continue

        for k in range(3):
                while l!=3:
                    z = a[m]
                    c.append(z[k])

                    m+=1
                    l+=1
                    
                m=aaa
                b.append(c)
                c=[]
                l=0
                z=j.copy
                au=0
        aaa+=3
        continue
        




    if pos[0]<3:
        if pos[1]<3: return (b[0][0]+b[0][1]+b[0][2])
        elif pos[1]<6: return (b[1][0]+b[1][1]+b[1][2])
        elif pos[1]<9: return(b[2][0]+b[2][1]+b[2][2])
    elif pos[0]<6:
        if pos[1]<3: return (b[3][0]+b[3][1]+b[3][2])
        elif pos[1]<6: return (b[4][0]+b[4][1]+b[4][2])
        elif pos[1]<9: return(b[5][0]+b[5][1]+b[5][2])
    elif pos[0]<9:
        if pos[1]<3: return (b[6][0]+b[6][1]+b[6][2])
        elif pos[1]<6: return (b[7][0]+b[7][1]+b[7][2])
        elif pos[1]<9: return(b[8][0]+b[8][1]+b[8][2])
"""



def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i,k in enumerate(grid):
        for j,l in enumerate(k):
            if l== ".": return (i,j)
    return None



def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    a={'1','2','3','4','5','6','7','8','9'}
    b = set(get_row(grid,pos))
    c = set(get_col(grid,pos))
    d = set(get_block(grid,pos))

    return(a.difference(b,c,d))




def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    row, col = pos
    for i in find_possible_values(grid, pos):
        grid[row][col] = i
        mean = solve(grid)
        if mean:
            return mean
    grid[row][col] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    for row in range(len(solution)):
        result = set(get_row(solution, (row, 0)))
        if result != set('123456789'):
            return False

    for col in range(len(solution)):
        result = set(get_col(solution, (0, col)))
        if result != set('123456789'):
            return False

    for row in range(0, len(solution)-1, 3):
        for col in range(0, len(solution)-1, 3):
            result = set(get_block(solution, (row, col)))
            if result != set('123456789'):
                return False

    return True



def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = solve([['.' for i in range(9)] for j in range(9)])
    N = 81 - N

    while N > 0:
        rand_i = random.randint(0, 8)
        rand_j = random.randint(0, 8)
        if grid[rand_i][rand_j] != '.':
            grid[rand_i][rand_j] = '.'
            N -= 1
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)