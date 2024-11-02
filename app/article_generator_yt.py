import asyncio
import logging
import sys
import os
import time
import random
import re
import typer # type: ignore
import json
from datetime import datetime
from rich import print
from rich.console import Console
from rich.logging import RichHandler
import subprocess
import glob

# Set WindowsSelectorEventLoopPolicy to avoid warnings on Windows
if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import GPT4oClient
from services.gpt4o_wrapper import GPT4oClient # type: ignore

# Typer instance for CLI
app = typer.Typer(add_completion=False)

console = Console()

# Function to set up logging
def setup_logging(video_title):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", video_title)  # Sanitize the title for filename
    log_dir = "data/outputs/logs"
    
    os.makedirs(log_dir, exist_ok=True)  # Ensure log directory exists
    log_file = f"{log_dir}/article_generator_log__{sanitized_title}__{timestamp}.log"

    # Set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Rich handler for console logging
    console_handler = RichHandler(console=console, show_time=False, show_path=False)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return log_file

class ArticleGenerator:
    def __init__(self):
        self.gpt_client = GPT4oClient()
        self.model_used = None  # Store the current model being used

    def load_cache(self, cache_file):
        """
        Load cache from the specified file, or return a default structure if the file doesn't exist.
        """
        # Create the cache directory if it doesn't exist
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)

        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"last_processed_idx": 0}

    def save_cache(self, cache_file, last_processed_idx):
        """
        Save the current progress into a cache file.
        """
        cache_data = {"last_processed_idx": last_processed_idx}
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f)
        logging.info(f"Saved cache for last processed index: {last_processed_idx}")

    def generate_article_from_transcript(self, transcript, audience, location, language, cache_file):
        logging.info("Splitting transcript into 500-word sections...")
        transcript_parts = self.split_transcript_by_words(transcript, 500)

        full_article = ""
        models = ["gpt-4o", "gpt-4-turbo", "gpt-4o-mini"]
        max_retries = 5
        retry_delay = random.uniform(2, 5)

        # Load cache to check for the last processed index
        cache_data = self.load_cache(cache_file)
        last_processed_idx = cache_data.get("last_processed_idx", 0)

        # Pastikan untuk memulai dari bagian yang belum diproses
        for idx, part in enumerate(transcript_parts):
            if idx < last_processed_idx:
                logging.info(f"Skipping part {idx + 1}, already processed.")
                continue

            # Menentukan prompt untuk bagian artikel: awal, tengah, akhir
            if idx == 0:
                prompt = f"""
You are an experienced content strategist and SEO expert.
Your task is to write the **first part of an article** based on the following transcript section for the audience {audience}, located in {location}, and in the {language} language.
The article should be engaging, informative, and relevant. Start with an attractive H1 title, create an engaging introduction, and begin the content with H2 headings.
Here is the first transcript part:

{part}

Ensure the content is SEO-friendly, with relevant keyword placement. Do not include a conclusion yet.
"""
            elif idx == len(transcript_parts) - 1:
                prompt = f"""
You are an experienced content strategist and SEO expert.
Your task is to write the **concluding part of an article** based on the following transcript section for the audience {audience}, located in {location}, and in the {language} language.
The article should be engaging, informative, and relevant. Continue the content with H2 headings and finish with a comprehensive conclusion that summarizes the entire article.
Here is the concluding transcript part:

{part}

Ensure the content is SEO-friendly, with relevant keyword placement.
"""
            else:
                prompt = f"""
You are an experienced content strategist and SEO expert.
Your task is to write the **next section** of an ongoing article based on the following transcript section for the audience {audience}, located in {location}, and in the {language} language.
Do not include an H1 title or introduction, just continue the article using H2 headings. Do not include a conclusion yet.
Here is the transcript part:

{part}

Ensure the content is SEO-friendly, with relevant keyword placement.
"""

            provider_error = None

            if self.model_used:
                logging.info(f"Continuing with model {self.model_used}...")
                model = self.model_used
            else:
                model = models[0]

            retries = 0
            while retries < max_retries:
                logging.info(f"Attempt {retries + 1} of {max_retries} for model {model}...")
                try:
                    article_part = self.gpt_client.send_request(prompt, model=model)
                    if self.is_valid_result(article_part):
                        full_article += f"\n{article_part.strip()}\n"
                        # Save progress to cache
                        self.save_cache(cache_file, idx + 1)
                        logging.info(f"Successfully processed part {idx + 1} with model {model}.")
                        self.model_used = model  # Set the model for future parts
                        break
                    else:
                        retries += 1
                        logging.warning(f"Attempt {retries} failed for model {model}. Retrying in {retry_delay:.2f} seconds...")
                        time.sleep(retry_delay)
                except Exception as e:
                    logging.error(f"Error using model {model}: {str(e)}")
                    retries += 1

                if retries == max_retries and model in models:
                    next_model_index = models.index(model) + 1
                    if next_model_index < len(models):
                        logging.info(f"Switching to model {models[next_model_index]}...")
                        model = models[next_model_index]
                    else:
                        logging.error(f"All models failed to generate the article for part {idx + 1}.")
                        break

        return full_article.strip()


    def split_transcript_by_words(self, transcript, words_per_section):
        logging.info("Splitting transcript into individual words...")
        lines = transcript.splitlines()
        sections = []
        current_section = []
        current_word_count = 0

        for line in lines:
            words_in_line = line.split()
            if current_word_count + len(words_in_line) > words_per_section:
                sections.append("\n".join(current_section))
                current_section = []
                current_word_count = 0
            current_section.append(line)
            current_word_count += len(words_in_line)

        if current_section:
            sections.append("\n".join(current_section))

        return sections

    def is_valid_result(self, result):
        if not result:
            return False
        return len(result.strip()) > 0

    def save_to_markdown(self, article, video_title):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", video_title)
        output_dir = os.path.join("data", "outputs", "articles")
        os.makedirs(output_dir, exist_ok=True)
        output_file = f"{output_dir}/article_{sanitized_title}_{timestamp}.md"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(article)

        logging.info(f"Article saved to: {output_file}")
        return output_file

    def call_get_transcript_script(self, youtube_url):
        """
        Call the external get_yt_transcript.py script to get the transcript file, then read and return its content.

        Args:
            youtube_url (str): The URL of the YouTube video.

        Returns:
            str: The transcript content, or None if there was an error.
        """
        try:
            # Call the script to generate the transcript file
            script_path = os.path.join(os.path.dirname(__file__), 'get_yt_transcript.py')
            command = [sys.executable, script_path, youtube_url]

            logging.info(f"Calling get_yt_transcript.py script for URL: {youtube_url}")
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0:
                logging.error(f"Error running get_yt_transcript.py: {result.stderr}")
                return None

            # Find the most recent transcript file in the transcripts directory
            transcripts_dir = os.path.join(os.getcwd(), 'data', 'outputs', 'transcripts')
            list_of_files = glob.glob(os.path.join(transcripts_dir, '*.txt'))
            if not list_of_files:
                logging.error("No transcript files found.")
                return None

            latest_file = max(list_of_files, key=os.path.getctime)
            logging.info(f"Reading transcript from file: {latest_file}")

            with open(latest_file, 'r', encoding='utf-8') as f:
                transcript = f.read()

            return transcript

        except Exception as e:
            logging.error(f"An error occurred while calling get_yt_transcript.py: {e}")
            return None

@app.command()
def main(
    youtube_url: str = typer.Option(..., help="URL of the YouTube video"),
    audience: str = typer.Option(..., help="Target audience (e.g., bloggers, content creators)"),
    location: str = typer.Option(..., help="Target location (e.g., Indonesia, USA)"),
    language: str = typer.Option(..., help="Language to use in the article (e.g., English, Bahasa Indonesia)"),
    ignore_cache: bool = typer.Option(False, "--ignore-cache", help="Ignore existing cache and regenerate article from scratch.")
):
    article_gen = ArticleGenerator()

    log_file = setup_logging(youtube_url)
    logging.info(f"Log file created: {log_file}")

    transcript = article_gen.call_get_transcript_script(youtube_url)

    if not transcript:
        logging.error("[red]Failed to retrieve transcript.[/red]")
        sys.exit(1)

    cache_file = os.path.join("data", "outputs", "cache", f"cache_{re.sub(r'[\\/*?:"<>|]', '_', youtube_url)}.json")
    if not ignore_cache and os.path.exists(cache_file):
        logging.info(f"Loading cache from {cache_file}.")
    else:
        logging.info("No cache found or ignore_cache is set. Starting fresh.")

    article = article_gen.generate_article_from_transcript(transcript, audience, location, language, cache_file)
    article_gen.save_to_markdown(article, youtube_url)
    logging.info("Program finished.")

if __name__ == "__main__":
    app()
