from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

def format_program_name(name: str) -> str:
    return name.strip().title()