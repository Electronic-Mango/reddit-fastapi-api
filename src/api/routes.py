from fastapi import APIRouter
from redditpythonapi import ArticlesSortTime, ArticlesSortType

from api.responses import prepare_list_response_or_abort, prepare_random_response_or_abort
from reddit.reddit_client import ArticleType, get_subreddit_articles, get_user_articles

subreddit_router = APIRouter(prefix="/subreddit")
user_router = APIRouter(prefix="/user")


@subreddit_router.get("/list/{subreddit}")
async def subreddit_list(
    subreddit: str,
    sort: ArticlesSortType = None,
    time: ArticlesSortTime = None,
    count: int = None,
    article_type: ArticleType = None,
):
    articles = await get_subreddit_articles(subreddit, sort, time, count, article_type)
    return prepare_list_response_or_abort(articles)


@subreddit_router.get("/random/{subreddit}")
async def subreddit_random(
    subreddit: str,
    sort: ArticlesSortType = None,
    time: ArticlesSortTime = None,
    count: int = None,
    article_type: ArticleType = None,
):
    articles = await get_subreddit_articles(subreddit, sort, time, count, article_type)
    return prepare_random_response_or_abort(articles)


@user_router.get("/list/{username}")
async def user_list(
    username: str,
    sort: ArticlesSortType = None,
    time: ArticlesSortTime = None,
    count: int = None,
    article_type: ArticleType = None,
):
    articles = await get_user_articles(username, sort, time, count, article_type)
    return prepare_list_response_or_abort(articles)


@user_router.get("/random/{username}")
async def user_random(
    username: str,
    sort: ArticlesSortType = None,
    time: ArticlesSortTime = None,
    count: int = None,
    article_type: ArticleType = None,
):
    articles = await get_user_articles(username, sort, time, count, article_type)
    return prepare_random_response_or_abort(articles)
