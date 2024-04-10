from datetime import datetime

from pydantic import BaseModel


class ArticleModel(BaseModel):
    """Model representing a single article."""

    id: str
    url: str
    title: str
    author: str
    nsfw: bool
    spoiler: bool
    selftext: str
    score: int
    created_utc: datetime
    permalink: str
    subreddit: str
    stickied: bool
    media_url: str | None


class ArticleListModel(BaseModel):
    """Model representing list of articles."""

    count: int
    articles: list[ArticleModel]
