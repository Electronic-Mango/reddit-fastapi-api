"""
Module responsible for preparing responses with Reddit articles.
"""

from random import choice
from typing import Any

from flask import abort

from api.reddit_client import Article


def prepare_list_response_or_abort(articles: list[Article]) -> dict[str, Any]:
    """Prepare API list response or abort with code 404 if no articles are present

    Args:
        articles (list[Article]): list of Reddit articles to send back

    Returns:
        dict[str, Any]: JSON containing list of generated articles and their count
    """
    if not articles:
        abort(404, "No entries found")
    return {"count": len(articles), "articles": articles}


def prepare_random_response_or_abort(articles: list[Article]) -> dict[str, Any]:
    """Prepare API random, single response or abort with code 404 if no articles are present

    Args:
        articles (list[Article]): list of articles to pick one random from to send back

    Returns:
        dict[str, Any]: JSON containing data of one random article
    """
    if not articles:
        abort(404, "No entries found")
    return choice(articles)
