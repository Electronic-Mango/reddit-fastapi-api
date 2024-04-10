"""
Module responsible for preparing responses with Reddit articles.
"""

from random import choice

from fastapi import HTTPException

from api.models import ArticleListModel, ArticleModel


def prepare_list_response_or_abort(articles: list[ArticleModel]) -> ArticleListModel:
    """Prepare API list response or abort with code 404 if no articles are present

    Args:
        articles (list[ArticleModel]): list of Reddit article models to send back

    Returns:
        ArticleListModel: Model representing list of articles, represents full input.
    """
    if not articles:
        raise HTTPException(404, "No entries found")
    return ArticleListModel(count=len(articles), articles=articles)


def prepare_random_response_or_abort(articles: list[ArticleModel]) -> ArticleModel:
    """Prepare API random, single response or abort with code 404 if no articles are present

    Args:
        articles (list[ArticleModel]): list of article models to pick one random from to send back

    Returns:
        ArticleModel: Model representing single article, selected randomly from input.
    """
    if not articles:
        raise HTTPException(404, "No entries found")
    return choice(articles)
