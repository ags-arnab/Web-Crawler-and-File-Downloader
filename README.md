# Web Crawler and File Downloader

This project is a Python-based web crawler and file downloader that recursively scans a given directory URL and downloads all the available files, excluding files with a `.aspx` extension. The crawler creates the directory structure locally to match the remote directory structure and uses multithreading to download files concurrently for faster performance.

## Features
- Recursively crawls a given index URL and navigates through subdirectories.
- Downloads all available files, excluding `.aspx` files.
- Creates a local directory structure matching the remote server's structure.
- Utilizes multithreading to speed up file downloads.
- Skips files that are already downloaded to avoid redundant downloads.

## Requirements
- Python 3.x
- `requests` library
- `beautifulsoup4` library

To install the required packages, run the following command:

```sh
pip install requests beautifulsoup4
```

## How to Use
1. Clone this repository or download the script.
2. Run the script by providing the index URL from which files need to be downloaded.
3. The script will create a folder named `downloaded_files` in the current working directory and download all the files into it.

### Running the Script
To run the script, use the following command:

```sh
python download_script.py
```

You will be prompted to enter the URL of the directory to crawl. The crawler will then begin scanning for files and downloading them.

## Code Explanation

### 1. `create_directory_structure(base_path, subdir)`
This function takes in the base path and the subdirectory name, and it creates the directory structure locally if it doesn't exist.

### 2. `download_file(url, save_path)`
This function is responsible for downloading the file from the given URL and saving it to the specified path. It uses streaming to download files in chunks to handle large files efficiently.

### 3. `is_directory_link(href)`
This helper function checks if a given link is a directory link by looking for trailing slashes.

### 4. `is_valid_file_link(href)`
This function checks if a given link is a valid file link, excluding files with a `.aspx` extension. This allows the script to download all file types except `.aspx`.

### 5. `crawl_and_download(index_url, save_directory, base_url, visited_urls=None)`
This function is the core of the script. It takes in the index URL, the local save directory, and the base URL to keep track of the domain. It uses BeautifulSoup to parse the HTML, collects subdirectory and file links, and uses a thread pool to download files concurrently.

### 6. `if __name__ == "__main__":`
This is the entry point of the script. It prompts the user for the index URL and starts the crawling and downloading process.

## Multithreading
The script uses the `ThreadPoolExecutor` from the `concurrent.futures` module to download files concurrently, which significantly speeds up the download process, especially when there are many files.

## Notes
- The script ensures that files are not downloaded twice by checking if the file already exists in the destination directory.
- The `visited_urls` set keeps track of URLs that have already been crawled to avoid infinite loops.
- Only files that are not `.aspx` are downloaded, allowing the user to filter out unnecessary files.

## Example
```sh
Enter the index directory URL: https://example.com/files/
```
The script will start crawling and downloading all files (except `.aspx`) under the provided URL into a folder named `downloaded_files`.

## License
This project is open source and available under the [MIT License](LICENSE).

## Contribution
Feel free to fork this repository, create a new branch, and submit a pull request if you have any improvements or bug fixes.

## Disclaimer
This script is intended for educational purposes. Please ensure you have permission to crawl and download files from the specified URL.

## Author
**Arnab Ghosh**  
GitHub: [ags-arnab](https://github.com/ags-arnab)
