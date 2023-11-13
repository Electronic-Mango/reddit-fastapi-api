"""
Blueprint of API endpoint returning a random text article from a user.
"""

from typing import Any

from flask import Blueprint
from redditpythonapi import ArticlesSortType

from api.prepare_response import prepare_random_response_or_abort
from api.reddit_client import get_user_text_articles
from settings import DEFAULT_LOAD_COUNT

blueprint = Blueprint("user/text/random", __name__)


@blueprint.route("/user/text/random/<username>")
@blueprint.route("/user/text/random/<username>/<int:load_count>")
@blueprint.route("/user/text/random/<username>/<int:load_count>/<sort:sort>")
async def user_random_text_article(
    username: str,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: ArticlesSortType = ArticlesSortType.HOT,
) -> dict[str, Any]:
    """Endpoint returning a random text article from the given user

    Up to "load_count" text articles are loaded from user, then a random one is selected.
    Number of loaded articles can be lower if user has fewer articles and due to filtering
    only text articles from the loaded ones.
    Still, the higher the "load_count" the lower the chance of returning the same article
    on repeated calls.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many articles should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (ArticlesSortType, optional): "hot", "top", "new", "controversial".
                                   Defaults to "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random text article from given user.
    """
    articles = await get_user_text_articles(username, load_count, sort)
    return prepare_random_response_or_abort(articles)
