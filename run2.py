import sys

import collections


# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def solve(data) -> int:
    """
    Находит минимальное количество шагов для сбора всех ключей в лабиринте.
    
    Args:
        data: Список строк, представляющих лабиринт
        
    Returns:
        int: Минимальное количество шагов или -1, если невозможно собрать все ключи
        
    Raises:
        ValueError: Если размер лабиринта превышает 100 клеток в любую сторону
    """
    #находим кол-во колонок и столбцов в лабиринте - ширина и высота
    rows, cols = len(data), len(data[0])
    
    # Проверяем размер лабиринта 
    if rows > 100 or cols > 100:
        raise ValueError("Некорректный размер лабиринта")
    
    # Находим начальные позиции роботов и количество ключей
    robots = []
    total_keys = 0
    #Проходим по всему лабиринту
    for x in range(rows): #ширина
        for y in range(cols):#высота
            if data[x][y] == '@':
                robots.append((x, y))
            #кол-во маленьких букв = кол-во ключей
            elif data[x][y].islower():
                total_keys += 1
    
    # Создаем начальное состояние: (позиции_роботов, собранные_ключи)
    # Используем кортежи тк они неизменяемые
    initial_state = (tuple(robots), frozenset())
    
    # Очередь для BFS: (состояние, количество_шагов)
    queue = collections.deque([(initial_state, 0)])
    
    # Множество посещенных состояний
    visited = {initial_state}
    
    # Направления движения: вверх, вниз, влево, вправо
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        (robots_pos, collected_keys), steps = queue.popleft()
        
        #Условия выхода
        if len(collected_keys) == total_keys:
            return steps
        
        #Проходим по каждому из 4 роботов
        for robot_idx in range(4):
            current_pos = robots_pos[robot_idx]
            #Пробуем двигать во все стороны
            for dx, dy in directions:
                x, y = current_pos[0] + dx, current_pos[1] + dy # Высчитываем новую позицию
                # Проверяем, что новая позиция в пределах лабиринта
                if 0 <= x < rows and 0 <= y < cols:
                    cell = data[x][y]
                    # Пропускаем стены
                    if cell == '#':
                        continue
                    # Проверяем дверь
                    if cell.isupper() and cell.lower() not in collected_keys:
                        continue
                    
                    # Создаем новое состояние
                    new_robots = list(robots_pos)  #копируем состояния роботов
                    new_robots[robot_idx] = (x, y) #меняем состояние у текущего
                    new_robots = tuple(new_robots) #приводим к кортежу
                    # Обновляем собранные ключи
                    new_keys = set(collected_keys) #копируем мн-во
                    if cell.islower():
                        new_keys.add(cell) #добавляем ключ если робот в клетке с ключом
                    new_keys = frozenset(new_keys) #создаем неизм мн-во с текущим состоянием

                    new_state = (new_robots, new_keys)
                    # Если состояние не посещено, добавляем его в очередь
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, steps + 1))
    return -1  # Если не удалось собрать все ключи


def main():
    try:
        data = get_input()
        result = solve(data)
        print(result)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()