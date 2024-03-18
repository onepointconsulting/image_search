from datetime import datetime

def generate_file_timestamp() -> str:
    current_timestamp = datetime.now()
    return current_timestamp.strftime("%Y%m%d_%H%M%S")