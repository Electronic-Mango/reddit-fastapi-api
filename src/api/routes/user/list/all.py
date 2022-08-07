"""
Blueprint of API endpoint returning a list of submissions for a user.
"""

from typing import Any

from flask import Blueprint

from api.prepare_response import prepare_list_response
from reddit.client import get_user_submissions
from settings import DEFAULT_LOAD_COUNT

blueprint = Blueprint("/user/submission", __name__)


@blueprint.route("/user/submission/<username>")
@blueprint.route("/user/submission/<username>/<int:load_count>")
@blueprint.route("/user/submission/<username>/<int:load_count>/<sort>")
def user_submissions(
    username: str,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a list of submissions from the given user

    Argument "load_count" specifies only how many submissions are loaded from user.
    Final count of submissions can be lower than "load_count" argument if given user has fewer
    submissions.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many submissions should be loaded.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded submissions and total submission count
    """
    return prepare_list_response(username, load_count, sort, get_user_submissions)