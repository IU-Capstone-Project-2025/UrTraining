users = [
    {"id": 1, "name": "Alice", "age": 28, "goal": "Weight Loss"},
    {"id": 2, "name": "Bob", "age": 35, "goal": "Strength"},
    {"id": 3, "name": "Clara", "age": 22, "goal": "Flexibility"},
]

def get_user_by_id(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return None