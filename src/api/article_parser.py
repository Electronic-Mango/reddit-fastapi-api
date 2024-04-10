"""
Module responsible for JSONifying Reddit articles.
"""

from datetime import datetime

from redditpythonapi import Article

from api.models import ArticleModel


def parse_article(article: Article) -> ArticleModel:
    """Change Reddit article to a JSON-like dict

    Only a selected values are present in resulting JSON:
     - id
     - url
     - title
     - author
     - nsfw
     - spoiler
     - selftext
     - score
     - created_utc - in human-readable format, not UNIX time
     - shortlink
     - subreddit
     - stickied
     - media_url - custom parameter storing URL for media articles

    Args:
        article (Article): Reddit article to parse

    Returns:
        ArticleModel: model containing parsed data
    """
    return ArticleModel(
        id=article.get("id"),
        url=article.get("url"),
        title=article.get("title"),
        author=article.get("author"),
        nsfw=article.get("over_18", False),
        spoiler=article.get("spoiler", False),
        selftext=article.get("selftext"),
        score=article.get("score", 0),
        created_utc=datetime.fromtimestamp(article.get("created_utc", 0)),
        permalink=article.get("permalink"),
        subreddit=article.get("subreddit"),
        stickied=article.get("stickied", False),
        media_url=_parse_media_url(article),
    )


def _parse_media_url(article: Article) -> str | None:
    if "i.redd.it" in article.get("domain", "") or "image" in article.get("post_hint", ""):
        return article.get("url")
    elif "v.redd.it" in article.get("domain", "") and article.get("is_video"):
        return article["media"]["reddit_video"]["fallback_url"].replace("?source=fallback", "")
    else:
        return None
