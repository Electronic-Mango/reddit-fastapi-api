"""
Module responsible for accessing Reddit API via PRAW.
"""

from enum import StrEnum

from redditpythonapi import Article, ArticlesSortTime, ArticlesSortType, Reddit

from api.article_parser import ArticleModel, parse_article
from settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_CLIENT_USER_AGENT


class ArticleType(StrEnum):
    """Enum with all viable types of loaded articles"""

    ALL = "all"
    MEDIA = "media"
    TEXT = "text"


_reddit = Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_CLIENT_USER_AGENT,
)


async def get_subreddit_articles(
    subreddit: str,
    sort: ArticlesSortType | None,
    time: ArticlesSortTime | None,
    limit: int | None,
    article_type: ArticleType = ArticleType.ALL,
) -> list[ArticleModel]:
    """Get a list of articles from the given subreddit and parse it into appropriate models.

    Resulting list can be shorter than "limit" argument if given subreddit has fewer articles.

    Args:
        subreddit (str): name of subreddit to get data from
        sort (ArticlesSortType | None): sort type to use when accessing articles
        time (ArticlesSortTime | None): time period in which articles will be searched for
        limit (int | None): how many articles should be loaded
        article_type (ArticleType): type of articles to filter out from Reddit API response

    Returns:
        list[ArticleModel]: list of all loaded articles from given subreddit.
    """
    articles = await _reddit.subreddit_articles(subreddit, sort, time, limit)
    models = _parse_articles_to_models(articles)
    return _filter_articles(models, article_type)


async def get_user_articles(
    username: str,
    sort: ArticlesSortType | None,
    time: ArticlesSortTime | None,
    limit: int | None,
    article_type: ArticleType = ArticleType.ALL,
) -> list[ArticleModel]:
    """Get a list of articles from a given use and parse it into appropriate models.

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.

    Args:
        username (str): username of user to get data from
        sort (ArticlesSortType | None): sort type to use when accessing articles
        time (ArticlesSortTime | None): time period in which articles will be searched for
        limit (int | None): how many articles should be loaded
        article_type (ArticleType): type of articles to filter out from Reddit API response

    Returns:
        list[ArticleModel]: list of all loaded articles from given user.
    """
    articles = await _reddit.user_articles(username, sort, time, limit)
    models = _parse_articles_to_models(articles)
    return _filter_articles(models, article_type)


def _parse_articles_to_models(articles: list[Article]) -> list[ArticleModel]:
    return list(map(parse_article, articles))


def _filter_articles(
    articles: list[ArticleModel], article_type: ArticleType | None
) -> list[ArticleModel]:
    match article_type:
        case ArticleType.MEDIA:
            return list(filter(lambda article: article.media_url, articles))
        case ArticleType.TEXT:
            return list(filter(lambda article: article.selftext, articles))
        case _:
            return articles
