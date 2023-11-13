"""
Blueprint of API endpoint returning a random article from a subreddit.
"""

from typing import Any

from flask import Blueprint
from redditpythonapi import ArticlesSortType

from api.prepare_response import prepare_random_response_or_abort
from api.reddit_client import get_subreddit_articles
from settings import DEFAULT_LOAD_COUNT, DEFAULT_SUBREDDIT

blueprint = Blueprint("/subreddit/article/random", __name__)


@blueprint.route("/subreddit/article/random")
@blueprint.route("/subreddit/article/random/<subreddit>")
@blueprint.route("/subreddit/article/random/<subreddit>/<int:load_count>")
@blueprint.route("/subreddit/article/random/<subreddit>/<int:load_count>/<sort:sort>")
async def subreddit_random_article(
    subreddit: str = DEFAULT_SUBREDDIT,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: ArticlesSortType = ArticlesSortType.HOT,
) -> dict[str, Any]:
    """Endpoint returning a random article from the given subreddit

    Up to "load_count" articles are loaded from subreddit, then a random one is selected.
    Number of loaded articles can be lower if subreddit has fewer articles.

    Args:
        subreddit (str, optional): subreddit to load data from.
                                   Defaults to DEFAULT_SUBREDDIT from .env.
        load_count (int, optional): how many articles should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (ArticlesSortType, optional): "hot", "top", "new", "controversial".
                                   Defaults to "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random article from given subreddit.
    """
    articles = await get_subreddit_articles(subreddit, load_count, sort)
    return prepare_random_response_or_abort(articles)
