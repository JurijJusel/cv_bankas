from pathlib import Path
import json
from utils.scraper_helpers import filter_new_posts


def write_data_to_json_file(data: list | dict, json_file_path: str) -> str:
    """
    Writes data to a JSON file. If the file does not exist,
    it creates the file and writes the data.
    If the file exists, it appends new data skipping duplicates by product_code.
    Args:
        data (list | dict): The data to write to the JSON file.
            Can be a list or a dictionary.
        json_file_path (str): The path to the JSON file.
    Returns:
        str: A message indicating whether the file was created or updated.
    Raises:
        ValueError: If the provided data is not a list or a dictionary.
        Exception: If an error occurs while writing to the file.
    """
    path = Path(json_file_path)

    new_data = data if isinstance(data, list) else [data]

    if not isinstance(data, (list, dict)):
        raise ValueError("The provided data must be a list or a dictionary.")

    try:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                existing_data = json.loads(content) if content.strip() else []

            new_data = filter_new_posts(existing_data, new_data)

            if not new_data:
                return f"Data already exists in '{json_file_path}'. No new data to append."

            existing_data.extend(new_data)
            message = f"Data appended to existing file: '{json_file_path}'."
        else:
            existing_data = new_data
            message = f"File created: '{json_file_path}'."

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)

        return message

    except Exception as e:
        print(f"An error occurred: {e}")
        raise
