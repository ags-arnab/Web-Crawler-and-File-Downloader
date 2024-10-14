import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures

def create_directory_structure(base_path, subdir):
    dir_path = os.path.join(base_path, subdir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def download_file(url, save_path):
    try:
        if os.path.exists(save_path):
            print(f"File already exists, skipping download: {save_path}")
            return
        print(f"Starting download: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024 * 32):  # Increase chunk size to improve download speed
                f.write(chunk)
        print(f"Downloaded: {save_path}")
    except requests.RequestException as e:
        print(f"Failed to download {url}. Error: {e}")

def is_directory_link(href):
    return href.endswith('/')

def is_valid_file_link(href):
    # Exclude links ending with .aspx, allow all other file types
    return not href.endswith('.aspx')

def crawl_and_download(index_url, save_directory, base_url, visited_urls=None):
    if visited_urls is None:
        visited_urls = set()
    if index_url in visited_urls:
        return
    visited_urls.add(index_url)
    try:
        response = requests.get(index_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        sub_links = []
        download_tasks = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href or href.startswith("../"):
                continue
            full_url = urljoin(index_url, href)

            # Ensure we only crawl within the provided base directory
            if not full_url.startswith(base_url):
                continue

            if is_directory_link(href):
                subdir_name = os.path.basename(os.path.normpath(href))
                new_save_directory = create_directory_structure(save_directory, subdir_name)
                sub_links.append((full_url, new_save_directory))
            elif is_valid_file_link(href):
                parsed_url = urlparse(full_url)
                file_name = os.path.basename(parsed_url.path)
                if not file_name:  # Skip if file_name is empty
                    continue
                save_path = os.path.join(save_directory, file_name)
                download_tasks.append((full_url, save_path))

        # Use ThreadPoolExecutor to download files concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(download_file, url, path) for url, path in download_tasks]
            concurrent.futures.wait(futures)

        # Recursively crawl subdirectories after downloading all files in the current directory
        for sub_url, sub_save_directory in sub_links:
            crawl_and_download(sub_url, sub_save_directory, base_url, visited_urls)

    except requests.RequestException as e:
        print(f"Failed to crawl {index_url}. Error: {e}")

if __name__ == "__main__":
    base_url = input("Enter the index directory URL: ")
    download_location = os.path.join(os.getcwd(), "downloaded_files")

    if not os.path.exists(download_location):
        os.makedirs(download_location)

    crawl_and_download(base_url, download_location, base_url)
