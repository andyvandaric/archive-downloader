
import typer # type: ignore
from app.article_generator_yt import ArticleGenerator

app = typer.Typer()

@app.command()
def generate_article(youtube_url: str, audience: str, location: str, language: str):
    generator = ArticleGenerator()
    generator.generate_article(youtube_url, audience, location, language)

if __name__ == "__main__":
    app()
