from pathlib import Path
import json


def filter_new_posts(existing_data: list, new_data: list) -> list:
    """
    Filters out posts that already exist based on post_id.
    """
    existing_ids = {item["post_id"] for item in existing_data}

    return [
        item for item in new_data
        if item["post_id"] not in existing_ids
    ]


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


#def create_json(posts_list, json_file):
#    path = Path(f"data/{json_file}")
#    if path.is_file():
#        with open(path, "a") as file:
#            json.dump(posts_list, file, indent=2)
#            return f'The data is added to the <{json_file}> file'
#    else:
#        with open(path, "w") as file:
#            json.dump(posts_list, file, indent=2)
#            return f'created <{json_file}> file and data written to it'


#def create_csv(csv_file, df):
#    file_path = Path(f'data/{csv_file}')
#    if file_path.exists():
#        df.to_csv(file_path, index=False, mode="a", header=False)
#        return f'The data is added to the <{csv_file}> file.'
#    else:
#        file_path.parent.mkdir(parents=True, exist_ok=True)
#        df.to_csv(file_path, index=False, mode="w", header=True)
#        return f'created <{csv_file}> file and data written to it'


#def read_csv(csv_file):
#    file_path = Path(f'data/{csv_file}')
#    read_df = pd.read_csv(file_path)
#    return read_df


#def create_companies_df(data_df, companies_df):
#    companys_lists = []
#    new_companies_count = 0
#    for line in range(len(data_df)):
#        line_posts=eval(data_df['posts'][line])
#        for post in range(len(line_posts)):
#            if line_posts[post]['company'] not in [i['company'] for i in companys_lists]:
#                companys_lists.append({'company': line_posts[post]['company'], 'img_url': line_posts[post]['img_url']})

#    for row in companys_lists:
#        if not (companies_df['company'] == row['company']).any():
#            new_companies_count += 1
#            companies_df = pd.concat([companies_df, pd.DataFrame(row, index=[0])], ignore_index=True)

#    companies_df.to_csv('data/companies.csv', index=False, mode="w", header=True)
#    return new_companies_count
