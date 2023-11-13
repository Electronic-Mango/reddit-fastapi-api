"""
Blueprint of API endpoint returning a random text article from a subreddit.
"""

from typing import Any

from flask import Blueprint
from redditpythonapi import ArticlesSortType

from api.prepare_response import prepare_random_response_or_abort
from api.reddit_client import get_subreddit_text_articles
from settings import DEFAULT_LOAD_COUNT, DEFAULT_SUBREDDIT

blueprint = Blueprint("/subreddit/text/random", __name__)


@blueprint.route("/subreddit/text/random")
@blueprint.route("/subreddit/text/random/<subreddit>")
@blueprint.route("/subreddit/text/random/<subreddit>/<int:load_count>")
@blueprint.route("/subreddit/text/random/<subreddit>/<int:load_count>/<sort:sort>")
async def subreddit_random_text_article(
    subreddit: str = DEFAULT_SUBREDDIT,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: ArticlesSortType = ArticlesSortType.HOT,
) -> dict[str, Any]:
    """Endpoint returning a random text article from the given subreddit

    Up to "load_count" text articles are loaded from subreddit, then a random one is selected.
    Number of loaded articles can be lower if subreddit has fewer articles and due to
    filtering only text articles from the loaded ones.
    Still, the higher the "load_count" the lower the chance of returning the same article
    on repeated calls.

    Args:
        subreddit (str, optional): subreddit to load data from.
                                   Defaults to DEFAULT_SUBREDDIT from .env.
        load_count (int, optional): how many articles should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (ArticlesSortType, optional): "hot", "top", "new", "controversial".
                                   Defaults to "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random text article from given subreddit.
    """
    articles = await get_subreddit_text_articles(subreddit, load_count, sort)
    return prepare_random_response_or_abort(articles)
