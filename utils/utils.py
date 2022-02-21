def build_username(user: dict):
    return f'{user["first_name"]} {user["last_name"]}'

def build_window_title(prefix: str, label: str):
    return f'{prefix}: {label}'
