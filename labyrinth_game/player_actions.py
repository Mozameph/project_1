# labyrinth_game/player_actions.py

"""
Функции действий игрока в игре 'Лабиринт сокровищ'.
Содержит функции перемещения, взаимодействия с предметами и управления инвентарем.
"""

from labyrinth_game.constant import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def get_input(prompt="> "):
    """
    Безопасно получает ввод от пользователя.
    """
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state):
    """
    Показывает содержимое инвентаря игрока.
    """
    inventory = game_state["player_inventory"]
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")


def move_player(game_state, direction):
    """
    Перемещает игрока в указанном направлении.
    """
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]

    if direction in room_data["exits"]:
        next_room_name = room_data["exits"][direction]

        # Проверка для перехода в treasure_room
        if next_room_name == "treasure_room":
            if "rusty_key" in game_state["player_inventory"]:
                print(
                    "Вы используете найденный ключ, чтобы открыть "
                    "путь в комнату сокровищ."
                )
                game_state["current_room"] = next_room_name
                game_state["steps_taken"] += 1
                describe_current_room(game_state)
                random_event(game_state)
                return True
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return False

        # Обычное перемещение для других комнат
        game_state["current_room"] = next_room_name
        game_state["steps_taken"] += 1
        print(f"Вы переместились {direction}.")
        describe_current_room(game_state)
        random_event(game_state)
        return True
    else:
        print("Нельзя пойти в этом направлении.")
        return False


def take_item(game_state, item_name):
    """
    Позволяет игроку поднять предмет из текущей комнаты.
    """
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]

    # Предметы, которые нельзя поднять
    untakable_items = ["treasure_chest", "bed"]

    if item_name in untakable_items:
        print(f"Вы не можете поднять {item_name}.")
        return False

    if item_name in room_data["items"]:
        room_data["items"].remove(item_name)
        game_state["player_inventory"].append(item_name)
        print(f"Вы подняли: {item_name}.")
        return True
    else:
        print("Такого предмета здесь нет.")
        return False


def use_item(game_state, item_name):
    """
    Позволяет игроку использовать предмет из инвентаря.
    """
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    # Использование предметов
    if item_name == "torch":
        print("Вы зажгли факел. Стало светлее.")
    elif item_name == "sword":
        print("Вы почувствовали себя увереннее с мечом в руках.")
    elif item_name == "bronze_box":
        if "rusty_key" not in inventory:
            print("Вы открыли бронзовую шкатулку. Внутри вы нашли rusty_key!")
            inventory.append("rusty_key")
        else:
            print("Шкатулка уже пуста.")
    elif item_name == "rusty_key":
        print("Ржавый ключ. Возможно, он от чего-то отпирает.")
    elif item_name == "ancient_book":
        print("Вы читаете древнюю книгу: 'Секрет сокровищницы - в числе десяти'")
    elif item_name == "beef":
        print("Вы съели неплохо приготовленную говядину!")
    elif item_name == "chicken":
        print("Вы пообедали хрустящей курочкой!")
    elif item_name == "clock":
        print("Время искать сокровища!")
    elif item_name == "treasure_key":
        print("Блестящий ключ от сокровищницы!")
    elif item_name == "coin":
        print("Монетка.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")