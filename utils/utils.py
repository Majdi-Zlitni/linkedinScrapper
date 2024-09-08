import requests
class utilities:
    def save_file_to_folder(file_url, file_path):
        """Save a file (image, PDF, MP4, etc.) to a folder."""
        try:
            response = requests.get(file_url, stream=True)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"File saved to {file_path}")
            else:
                print(f"Failed to download file from {file_url}")
        except Exception as e:
            print(f"An error occurred while downloading the file: {e}")