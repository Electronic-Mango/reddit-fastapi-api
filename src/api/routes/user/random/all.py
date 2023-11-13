"""
Blueprint of API endpoint returning a random article from a user.
"""

from typing import Any

from flask import Blueprint
from redditpythonapi import ArticlesSortType

from api.prepare_response import prepare_random_response_or_abort
from api.reddit_client import get_user_articles
from settings import DEFAULT_LOAD_COUNT

blueprint = Blueprint("user/article/random", __name__)


@blueprint.route("/user/article/random/<username>")
@blueprint.route("/user/article/random/<username>/<int:load_count>")
@blueprint.route("/user/article/random/<username>/<int:load_count>/<sort:sort>")
async def user_random_article(
    username: str,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: ArticlesSortType = ArticlesSortType.HOT,
) -> dict[str, Any]:
    """Endpoint returning a random article from the given user

    Up to "load_count" articles are loaded from user, then a random one is selected.
    Number of loaded articles can be lower if user has fewer articles.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many articles should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (ArticlesSortType, optional): "hot", "top", "new", "controversial".
                                   Defaults to "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random article from given user.
    """
    articles = await get_user_articles(username, load_count, sort)
    return prepare_random_response_or_abort(articles)
