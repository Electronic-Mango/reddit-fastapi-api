from enum import Enum, auto

from fastapi import APIRouter
from redditpythonapi import Article, ArticlesSortTime, ArticlesSortType

from reddit.prepare_response import prepare_list_response_or_abort, prepare_random_response_or_abort
from reddit.reddit_client import (
    filter_media_articles,
    filter_text_articles,
    get_subreddit_articles,
    get_user_articles,
)

subreddit_router = APIRouter(prefix="/subreddit")
user_router = APIRouter(prefix="/user")


class ArticleType(Enum):
    """Enum with all viable types of loaded articles"""

    ALL = auto()
    MEDIA = auto()
    TEXT = auto()


@subreddit_router.get("/list/{subreddit}")
async def subreddit_list(
    subreddit: str,
    sort: ArticlesSortType | None = None,
    time: ArticlesSortTime | None = None,
    count: int | None = None,
    article_type: ArticleType = ArticleType.ALL,
):
    articles = await get_subreddit_articles(subreddit, sort, time, count)
    filtered_articles = _filter_articles(articles, article_type)
    return prepare_list_response_or_abort(filtered_articles)


@subreddit_router.get("/random/{subreddit}")
async def subreddit_random(
    subreddit: str,
    sort: ArticlesSortType | None = None,
    time: ArticlesSortTime | None = None,
    count: int | None = None,
    article_type: ArticleType = ArticleType.ALL,
):
    articles = await get_subreddit_articles(subreddit, sort, time, count)
    filtered_articles = _filter_articles(articles, article_type)
    return prepare_random_response_or_abort(filtered_articles)


@user_router.get("/list/{username}")
async def user_list(
    username: str,
    sort: ArticlesSortType | None = None,
    time: ArticlesSortTime | None = None,
    count: int | None = None,
    article_type: ArticleType = ArticleType.ALL,
):
    articles = await get_user_articles(username, sort, time, count)
    filtered_articles = _filter_articles(articles, article_type)
    return prepare_list_response_or_abort(filtered_articles)


@user_router.get("/random/{username}")
async def user_random(
    username: str,
    sort: ArticlesSortType | None = None,
    time: ArticlesSortTime | None = None,
    count: int | None = None,
    article_type: ArticleType = ArticleType.ALL,
):
    articles = await get_user_articles(username, sort, time, count)
    filtered_articles = _filter_articles(articles, article_type)
    return prepare_random_response_or_abort(filtered_articles)


def _filter_articles(articles: list[Article], article_type: ArticleType) -> list[Article]:
    match article_type:
        case ArticleType.MEDIA:
            return filter_media_articles(articles)
        case ArticleType.TEXT:
            return filter_text_articles(articles)
        case _:
            return articles
