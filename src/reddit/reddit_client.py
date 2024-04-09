"""
Module responsible for accessing Reddit API via PRAW.
"""

from enum import StrEnum

from redditpythonapi import Article, ArticlesSortTime, ArticlesSortType, Reddit

from reddit.article_parser import parse_article
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
) -> list[Article]:
    """Get a list of articles from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer articles.

    Args:
        subreddit (str): name of subreddit to get data from
        sort (ArticlesSortType | None): sort type to use when accessing articles
        time (ArticlesSortTime | None): time period in which articles will be searched for
        limit (int | None): how many articles should be loaded
        article_type (ArticleType): type of articles to filter out from Reddit API response

    Returns:
        list[Article]: list of all loaded articles from given subreddit.
    """
    articles = await _reddit.subreddit_articles(subreddit, sort, time, limit)
    return _parse_and_filter_articles(articles, article_type)


async def get_user_articles(
    username: str,
    sort: ArticlesSortType | None,
    time: ArticlesSortTime | None,
    limit: int | None,
    article_type: ArticleType = ArticleType.ALL,
) -> list[Article]:
    """Get a list of articles from user with the given username

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.

    Args:
        username (str): username of user to get data from
        sort (ArticlesSortType | None): sort type to use when accessing articles
        time (ArticlesSortTime | None): time period in which articles will be searched for
        limit (int | None): how many articles should be loaded
        article_type (ArticleType): type of articles to filter out from Reddit API response

    Returns:
        list[Article]: list of all loaded articles from given user.
    """
    articles = await _reddit.user_articles(username, sort, time, limit)
    return _parse_and_filter_articles(articles, article_type)


def _parse_and_filter_articles(articles: list[Article], article_type: ArticleType) -> list[Article]:
    parsed_articles = _parse_articles(articles)
    return _filter_articles(parsed_articles, article_type)


def _parse_articles(articles: list[Article]) -> list[Article]:
    return list(map(parse_article, articles))


def _filter_articles(articles: list[Article], article_type: ArticleType | None) -> list[Article]:
    match article_type:
        case ArticleType.MEDIA:
            return _filter_articles_by_key(articles, "media_url")
        case ArticleType.TEXT:
            return _filter_articles_by_key(articles, "selftext")
        case _:
            return articles


def _filter_articles_by_key(articles: list[Article], key: str) -> list[Article]:
    return list(filter(lambda article: article[key], articles))
