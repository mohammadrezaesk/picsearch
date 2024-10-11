import os
import requests


def download_image(url, image_name, save_directory):
    try:
        image_format = url.split(".")[-1]
        image_name = image_name + "." + image_format
        file_path = os.path.join(save_directory, image_name)
        if os.path.exists(file_path):
            return file_path
        response = requests.get(url)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {file_path}")
        return file_path

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return None


def download_images(url_list, save_directory):
    os.makedirs(save_directory, exist_ok=True)

    for url, image_name in url_list:
        download_image(url, image_name, save_directory)


def remove_file(file_path):
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)  # Remove the file
            print(f"Successfully removed: {file_path}")
        else:
            print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error removing file {file_path}: {e}")
