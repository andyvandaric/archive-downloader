import os
import json
import concurrent.futures  # Import langsung futures di sini
import requests
import subprocess
import psutil
from pathlib import Path
from urllib.parse import urljoin
import re
import logging
import typer
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup


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
                        url = urljoin(
                            self.download_url, f"{self.reciter_name}/{link.get('href')}"
                        )
                        files.append({"filename": filename, "url": url})
            return files
        except Exception as e:
            self.logger.error(f"Error getting file list: {e}")
            return []

    def get_optimal_threads(self, target_cpu_usage=90):
        cpu_usage = psutil.cpu_percent(interval=1)
        available_cpu = max(
            1, psutil.cpu_count() - int(cpu_usage * psutil.cpu_count() / 100)
        )
        return max(1, int((target_cpu_usage - cpu_usage) / 100 * available_cpu))

    def download_file_with_aria2(self, file_info, download_dir, max_connections=16):
        filename = file_info["filename"]
        url = file_info["url"]
        file_path = download_dir / filename

        if file_path.exists():
            self.logger.info(f"{filename} already exists. Skipping download.")
            return {"filename": filename, "status": "already_downloaded"}

        try:
            cmd = [
                "aria2c",
                "-x",
                str(max_connections),
                "-s",
                str(max_connections),
                "-d",
                str(download_dir),
                "-o",
                filename,
                url,
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                self.logger.info(f"Downloaded: {filename}")
                return {"filename": filename, "status": "downloaded"}
            else:
                error_msg = result.stderr.decode()
                self.logger.error(f"Error downloading {filename}: {error_msg}")
                return {"filename": filename, "status": "error", "error": error_msg}
        except Exception as e:
            self.logger.error(f"Error downloading {filename} with aria2: {e}")
            return {"filename": filename, "status": "error", "error": str(e)}

    def create_index(self, files):
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

        optimal_threads = self.get_optimal_threads()
        self.logger.info(f"Starting downloads with {optimal_threads} threads")

        downloaded_files = []
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=optimal_threads
        ) as executor:
            futures = [
                executor.submit(self.download_file_with_aria2, file_info, download_dir)
                for file_info in files
            ]
            for future in concurrent.futures.as_completed(futures):
                downloaded_files.append(future.result())

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
