import json

def check_capacity(max_capacity: int, guests: list) -> bool:
    #Временная сложность алгоритма O(n*log(n))
    #Пространственная сложность O(n)
    '''
    Метод проверки вместимости гостиницы
    '''
    #Создаем список со всеми заездами и выездами
    events = []
    #Проходя по списку гостей, записываем события в кортеж:
    # (дата и время, код события(1 - заезд, -1 - выезд)).
    # ---расшифровка--- +1 человек при заезде, -1 при выезде
    #Сложность O(n) - проходим 1 раз по длине гостей
    for guest in guests:
        events.append((guest['check-in'], 1))
        events.append((guest['check-out'], -1))
    #Сортируем по времени. Базовый алгоритм сортировки Timsort - в худшем случае (nlogn).
    #В нашем случае тк каждый гость въезжает и выезжает кол-во операций n -> 2n 
    #(2n*log(2n)) - но в общем это все еще сложность O(nlog(n)).
    events.sort() 

    current_guests_count = 0
    #Проходим еще раз по отсортированному массиву - кол-во опер 2n - сложность O(N)
    for _, event_type in events:
        #Тк наш масив отсортирован по времени, кол-во гостей меняется в строго хронологическом порядке
        current_guests_count += event_type
        #И если в какой то момент кол-во гостей превысит макс допустимое кол-во значит слишком много колизий
        #времени пребывания, превышающих общую вместимость.
        if current_guests_count > max_capacity:
            #В этом случае возвращаем - False
            return False
    #во всех остальных True
    return True


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())

    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)

    result = check_capacity(max_capacity, guests)
    print(result)