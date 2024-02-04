import random
import string
import tempfile


def save_file_to_temp_directory(data: bytes) -> str:
    temp_dir = tempfile.gettempdir()
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    temp_file_name = temp_dir + "/" + random_string
    with open(temp_file_name, "wb") as temp_file:
        temp_file.write(data)

    return temp_file_name
