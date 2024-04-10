"""
Module storing all available routes in the API.
"""

from typing import Annotated

from fastapi import APIRouter, Path, Query
from redditpythonapi import ArticlesSortTime, ArticlesSortType

from api.models import ArticleListModel, ArticleModel
from api.reddit import ArticleType, get_subreddit_articles, get_user_articles
from api.responses import prepare_list_response_or_abort, prepare_random_response_or_abort

router = APIRouter()


@router.get("/subreddit/list/{subreddit}")
async def subreddit_list(
    subreddit: Annotated[str, Path(description="Subreddit to load data from.")],
    sort: Annotated[ArticlesSortType, Query(description="Articles sort type.")] = None,
    time: Annotated[ArticlesSortTime, Query(description="Time period of posted articles.")] = None,
    count: Annotated[int, Query(description="How many articles should be loaded.", gt=0)] = None,
    article_type: Annotated[ArticleType, Query(description="Type of articles to return.")] = None,
) -> ArticleListModel:
    """Endpoint returning a list of articles from the given subreddit.

    Argument `count` specifies only how many articles are loaded from subreddit.
    Number of articles can be lower than `count` if given subreddit has fewer articles.
    """
    articles = await get_subreddit_articles(subreddit, sort, time, count, article_type)
    return prepare_list_response_or_abort(articles)


@router.get("/subreddit/random/{subreddit}")
async def subreddit_random(
    subreddit: Annotated[str, Path(description="Subreddit to load data from.")],
    sort: Annotated[ArticlesSortType, Query(description="Articles sort type.")] = None,
    time: Annotated[ArticlesSortTime, Query(description="Time period of posted articles.")] = None,
    count: Annotated[int, Query(description="How many articles should be loaded.", gt=0)] = None,
    article_type: Annotated[ArticleType, Query(description="Type of articles to return.")] = None,
) -> ArticleModel:
    """Endpoint returning a single random article from the given subreddit.

    Up to `count` articles are loaded, then a random one is selected
    Number of loaded articles can be lower than `count` if given subreddit has fewer articles.
    """
    articles = await get_subreddit_articles(subreddit, sort, time, count, article_type)
    return prepare_random_response_or_abort(articles)


@router.get("/user/list/{username}")
async def user_list(
    username: Annotated[str, Path(description="Username to load data from.")],
    sort: Annotated[ArticlesSortType, Query(description="Articles sort type.")] = None,
    time: Annotated[ArticlesSortTime, Query(description="Time period of posted articles.")] = None,
    count: Annotated[int, Query(description="How many articles should be loaded.", gt=0)] = None,
    article_type: Annotated[ArticleType, Query(description="Type of articles to return.")] = None,
) -> ArticleListModel:
    """Endpoint returning a list of articles from the given user.

    Argument `count` specifies only how many articles are loaded from user.
    Number of articles can be lower than `count` if given user has submitted fewer articles.
    """
    articles = await get_user_articles(username, sort, time, count, article_type)
    return prepare_list_response_or_abort(articles)


@router.get("/user/random/{username}")
async def user_random(
    username: Annotated[str, Path(description="Username to load data from.")],
    sort: Annotated[ArticlesSortType, Query(description="Articles sort type.")] = None,
    time: Annotated[ArticlesSortTime, Query(description="Time period of posted articles.")] = None,
    count: Annotated[int, Query(description="How many articles should be loaded.", gt=0)] = None,
    article_type: Annotated[ArticleType, Query(description="Type of articles to return.")] = None,
) -> ArticleModel:
    """Endpoint returning a single random article from the given user.

    Up to `count` articles are loaded, then a random one is selected
    Number of loaded articles can be lower than `count` if given user has submitted fewer articles.
    """
    articles = await get_user_articles(username, sort, time, count, article_type)
    return prepare_random_response_or_abort(articles)
