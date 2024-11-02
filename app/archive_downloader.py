import os
import json
import requests
import concurrent.futures
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup  # type: ignore
from pathlib import Path
import re
import logging
import typer
from tqdm import tqdm  # Progress bar


class ArchiveDownloader:
    def __init__(self, base_url, project_dir):
        """
        Initialize the downloader

        Args:
            base_url (str): Base URL of the archive.org content
            project_dir (str): Base project directory
        """
        self.base_url = base_url
        self.project_dir = project_dir
        self.reciter_name = self.extract_reciter_name(base_url)
        self.download_url = self.generate_download_url(base_url)
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path(self.project_dir) / "data" / "outputs" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file_name = f"{self.reciter_name}_{self.get_current_date()}.log"
        log_file = log_dir / log_file_name

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )
        self.logger = logging.getLogger(__name__)

    def get_current_date(self):
        """Get current date in YYYYMMDD format."""
        from datetime import datetime

        return datetime.now().strftime("%Y%m%d")

    def extract_reciter_name(self, base_url):
        """Extract the reciter name from the URL."""
        if "details" in base_url:
            return re.search(r"/details/([^/]+)", base_url).group(1)
        else:
            raise ValueError("Invalid URL format. Must contain 'details'.")

    def generate_download_url(self, base_url):
        """Generate the download URL based on the base URL."""
        if "details" in base_url:
            return base_url.replace("/details/", "/download/")
        elif "download" in base_url:
            return base_url
        else:
            raise ValueError(
                "Invalid URL format. Must be either 'details' or 'download'."
            )

    def create_directories(self):
        """
        Create necessary directories

        Returns:
            Path: Download directory path
        """
        download_dir = (
            Path(self.project_dir) / "downloads" / "recitation" / self.reciter_name
        )
        download_dir.mkdir(parents=True, exist_ok=True)
        return download_dir

    def get_file_list(self):
        """
        Get list of files from archive.org download page

        Returns:
            list: List of file information dictionaries
        """
        try:
            response = requests.get(self.download_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            files = []

            # Process table rows
            for row in soup.find_all("tr")[1:]:  # Skip header row
                cols = row.find_all(["td", "th"])
                if len(cols) >= 3:
                    link = cols[0].find("a")
                    if link and "parent" not in link.get("href", ""):
                        filename = link.text.strip()
                        # Correct URL construction to include reciter name
                        url = urljoin(
                            self.download_url, f"{self.reciter_name}/{link.get('href')}"
                        )
                        last_modified = cols[1].text.strip()
                        size = cols[2].text.strip()

                        files.append(
                            {
                                "filename": filename,
                                "url": url,
                                "last_modified": last_modified,
                                "size": size,
                            }
                        )

            return files

        except Exception as e:
            self.logger.error(f"Error getting file list: {e}")
            return []

    def download_file(self, file_info, download_dir):
        """
        Download a single file with support for resuming if already partially downloaded.

        Args:
            file_info (dict): File information dictionary
            download_dir (Path): Download directory path

        Returns:
            dict: Updated file information including local path and status
        """
        filename = file_info["filename"]
        url = file_info["url"]
        file_path = download_dir / filename

        # Check if the file already exists and determine the size
        if file_path.exists():
            existing_size = file_path.stat().st_size
            self.logger.info(
                f"Resuming download for: {filename}, already downloaded {existing_size} bytes"
            )
        else:
            existing_size = 0  # File doesn't exist, start from zero

        # Fetch file size from headers if available
        try:
            head_response = requests.head(url)
            total_size = int(head_response.headers.get("content-length", 0))
        except Exception as e:
            self.logger.error(f"Error fetching head info for {filename}: {e}")
            total_size = 0

        # If file is already complete, skip download
        if existing_size == total_size:
            self.logger.info(f"{filename} is already fully downloaded.")
            file_info["local_path"] = str(file_path)
            file_info["status"] = "already_downloaded"
            return file_info

        # Set headers for resuming download
        headers = {}
        if existing_size > 0:
            headers["Range"] = f"bytes={existing_size}-"

        try:
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()

            with open(file_path, "ab") as f, tqdm(
                desc=filename,
                total=total_size,
                initial=existing_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                leave=True,
            ) as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

            self.logger.info(f"Downloaded: {filename}")
            file_info["local_path"] = str(file_path)
            file_info["status"] = "downloaded"
            return file_info

        except Exception as e:
            self.logger.error(f"Error downloading {filename}: {e}")
            file_info["status"] = "error"
            file_info["error"] = str(e)
            return file_info

    def create_index(self, files):
        """
        Create index file with downloaded content information

        Args:
            files (list): List of file information dictionaries
        """
        index = {
            "identifier": self.reciter_name,
            "base_url": self.base_url,
            "download_url": self.download_url,
            "total_files": len(files),
            "files": files,
        }

        index_path = (
            Path(self.project_dir)
            / "downloads"
            / "recitation"
            / self.reciter_name
            / "index.json"
        )
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

        self.logger.info(f"Created index file: {index_path}")

    def download_all(self):
        """
        Download all files and create index
        """
        download_dir = self.create_directories()

        files = self.get_file_list()
        if not files:
            self.logger.error("No files found to download")
            return

        self.logger.info(f"Found {len(files)} files to download")

        # Download files using thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_file = {
                executor.submit(self.download_file, file_info, download_dir): file_info
                for file_info in files
            }

            downloaded_files = []
            for future in concurrent.futures.as_completed(future_to_file):
                result = future.result()
                downloaded_files.append(result)

        # Create index file
        self.create_index(downloaded_files)


def main(base_url: str):
    """
    Main function to download files from archive.org

    Args:
        base_url (str): The base URL of the archive.org content
    """
    project_dir = "."  # Current directory, modify as needed

    try:
        downloader = ArchiveDownloader(base_url, project_dir)
        downloader.download_all()
    except ValueError as ve:
        typer.echo(f"Error: {ve}")
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    typer.run(main)
