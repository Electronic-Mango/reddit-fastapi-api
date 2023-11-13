"""
Blueprint of API endpoint returning a list of media articles for a subreddit.
"""

from typing import Any

from flask import Blueprint
from redditpythonapi import ArticlesSortType

from api.prepare_response import prepare_list_response_or_abort
from api.reddit_client import get_subreddit_media_articles
from settings import DEFAULT_LOAD_COUNT, DEFAULT_SUBREDDIT

blueprint = Blueprint("/subreddit/media", __name__)


@blueprint.route("/subreddit/media")
@blueprint.route("/subreddit/media/<subreddit>")
@blueprint.route("/subreddit/media/<subreddit>/<int:load_count>")
@blueprint.route("/subreddit/media/<subreddit>/<int:load_count>/<sort:sort>")
async def subreddit_image_articles(
    subreddit: str = DEFAULT_SUBREDDIT,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: ArticlesSortType = ArticlesSortType.HOT,
) -> dict[str, Any]:
    """Endpoint returning a list of media articles (images, GIFs) from the given subreddit

    Argument "load_count" specifies only how many articles are loaded from subreddit.
    Final count of articles can be lower than "load_count" argument if given subreddit has fewer
    articles and due to filtering only media articles.

    Args:
        subreddit (str, optional): subreddit to load data from.
                                   Defaults to DEFAULT_SUBREDDIT from .env.
        load_count (int, optional): how many articles should be loaded.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (ArticlesSortType, optional): "hot", "top", "new", "controversial".
                                   Defaults to "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded media articles and total article count.
    """
    articles = await get_subreddit_media_articles(subreddit, load_count, sort)
    return prepare_list_response_or_abort(articles)
