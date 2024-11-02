import os
import subprocess
from pathlib import Path

# Gunakan direktori kerja saat ini sebagai base_dir
base_dir = Path.cwd()

# Struktur direktori yang ingin dibuat
structure = {
    "": ["README.md", ".gitignore", "pyproject.toml", "main.py"],
    "app": ["sample_app.py", "__init__.py", "article_generator_yt.py"],
    "assets": [],
    "config": [],
    "data/inputs": [],
    "data/outputs/logs": [],
    "data/outputs/transcripts": [],
    "database": ["clear_db.py", "connection.py", "models.py", "__init__.py"],
    "docs": [],
    "generated_images": [],
    "services": ["utils.py", "__init__.py"],
    "tests": ["local.py"],
}

# Isi dari file .gitignore
gitignore_content = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
*.pyc
*.pyo
*.pyd

# Poetry virtual environments
.venv/
poetry.lock

# PyInstaller
# Usually these files are generated when PyInstaller is run
/build/
dist/
*.spec

# PyArmor
*.pyarmor
.pyarmor_config/
pyarmor_output/

# Sphinx documentation
docs/_build/
docs/build/

# MacOS
.DS_Store

# Windows
Thumbs.db
ehthumbs.db

# VS Code
.vscode/

# Python eggs
*.egg
*.egg-info/

# Caches
*.log
*.cache
*.coverage
.cache/

# Distribution / packaging
.Python
env/
env.bak/
pip-wheel-metadata/
lib/

# Unit test / coverage reports
htmlcov/
.coverage
.tox/

# Generated files
*.bak

# har and cookies
config/har_and_cookies/

# Ignore output files
data/
dashboard/

# Database files
*.db
*.sqlite3

"""

# Isi dari file README.md
project_name = base_dir.name
readme_content = f"""
# {project_name}

A CLI application built in Python.
"""

# Isi dari file pyproject.toml
pyproject_content = f"""
[tool.poetry]
name = "{project_name}"
version = "0.1.0"
description = "A starter CLI app project in Python"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = ">=3.10,<3.14"
typer = "^0.12.5"
pyinstaller = "^6.10.0"
curl-cffi = "^0.7.1"
cloudscraper = "^1.2.71"
uvicorn = "^0.30.6"
fastapi = "^0.114.1"
g4f = "^0.3.2.8"
motor = "^3.5.1"
odmantic = "^1.0.2"
spacy = "^3.7.6"
scikit-learn = "^1.5.2"
gensim = "^4.3.3"
rich = "^13.8.1"
youtube-transcript-api = "^0.6.2"
yt-dlp = "^2024.9.27"

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""

# Isi dari file main.py
main_py_content = """
import typer
from app.article_generator_yt import ArticleGenerator

app = typer.Typer()

@app.command()
def generate_article(youtube_url: str, audience: str, location: str, language: str):
    generator = ArticleGenerator()
    generator.generate_article(youtube_url, audience, location, language)

if __name__ == "__main__":
    app()
"""

# Isi dari file article_generator_yt.py
article_generator_yt_content = """
import typer
import logging
import os
from rich.console import Console

# Typer instance for CLI
app = typer.Typer(add_completion=False)
console = Console()

class ArticleGenerator:
    def generate_article(self, youtube_url, audience, location, language):
        console.print(f"Generating article for [bold blue]{youtube_url}[/bold blue] aimed at {audience} in {location} and in {language}.")
        # Add actual article generation logic here

@app.command()
def main(youtube_url: str, audience: str, location: str, language: str):
    generator = ArticleGenerator()
    generator.generate_article(youtube_url, audience, location, language)

if __name__ == "__main__":
    app()
"""

# Fungsi untuk membuat file dengan konten
def create_file(path, content=""):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Buat struktur direktori dan file
for folder, files in structure.items():
    folder_path = base_dir / folder
    os.makedirs(folder_path, exist_ok=True)
    for file in files:
        file_path = folder_path / file
        content = ""
        if file == "README.md":
            content = readme_content
        elif file == ".gitignore":
            content = gitignore_content
        elif file == "pyproject.toml":
            content = pyproject_content
        elif file == "main.py":
            content = main_py_content
        elif file == "article_generator_yt.py":
            content = article_generator_yt_content
        create_file(file_path, content)

print(f"Project {project_name} structure has been created at {base_dir}")

# Inisialisasi Poetry dan instal dependensi
subprocess.run(["poetry", "install"], cwd=base_dir)
print("Dependencies installed using poetry.")
