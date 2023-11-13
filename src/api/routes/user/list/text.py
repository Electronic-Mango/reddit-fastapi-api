"""
Blueprint of API endpoint returning a list of text articles for a user.
"""

from typing import Any

from flask import Blueprint
from redditpythonapi import ArticlesSortType

from api.prepare_response import prepare_list_response_or_abort
from api.reddit_client import get_user_text_articles
from settings import DEFAULT_LOAD_COUNT

blueprint = Blueprint("/user/text", __name__)


@blueprint.route("/user/text/<username>")
@blueprint.route("/user/text/<username>/<int:load_count>")
@blueprint.route("/user/text/<username>/<int:load_count>/<sort:sort>")
async def user_text_articles(
    username: str,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: ArticlesSortType = ArticlesSortType.HOT,
) -> dict[str, Any]:
    """Endpoint returning a list of text articles from the given user

    Argument "load_count" specifies only how many articles are loaded from user.
    Final count of articles can be lower than "load_count" argument if given user has fewer
    articles and due to filtering only text articles.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many articles should be loaded.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (ArticlesSortType, optional): "hot", "top", "new", "controversial".
                                   Defaults to "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded text articles and total article count.
    """
    articles = await get_user_text_articles(username, load_count, sort)
    return prepare_list_response_or_abort(articles)
