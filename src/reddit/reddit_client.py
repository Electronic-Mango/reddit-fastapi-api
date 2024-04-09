"""
Module responsible for accessing Reddit API via PRAW.
"""

from redditpythonapi import Article, ArticlesSortTime, ArticlesSortType, Reddit

from reddit.article_parser import parse_article
from settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_CLIENT_USER_AGENT

_reddit = Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_CLIENT_USER_AGENT,
)


async def get_subreddit_articles(
    subreddit: str, sort: ArticlesSortType | None, time: ArticlesSortTime | None, limit: int | None
) -> list[Article]:
    """Get a list of articles from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer articles.

    Args:
        subreddit (str): name of subreddit to get data from
        sort (ArticlesSortType | None): sort type to use when accessing articles
        time (ArticlesSortTime | None): time period in which articles will be searched for
        limit (int | None): how many articles should be loaded

    Returns:
        list[Article]: list of all loaded articles from given subreddit.
    """
    articles = await _reddit.subreddit_articles(subreddit, sort, time, limit)
    return list(map(parse_article, articles))


async def get_user_articles(
    username: str, sort: ArticlesSortType | None, time: ArticlesSortTime | None, limit: int | None
) -> list[Article]:
    """Get a list of articles from user with the given username

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.

    Args:
        username (str): username of user to get data from
        sort (ArticlesSortType | None): sort type to use when accessing articles
        time (ArticlesSortTime | None): time period in which articles will be searched for
        limit (int | None): how many articles should be loaded

    Returns:
        list[Article]: list of all loaded articles from given user.
    """
    articles = await _reddit.user_articles(username, sort, time, limit)
    return list(map(parse_article, articles))


def filter_media_articles(articles: list[Article]) -> list[Article]:
    """Filter only media articles from a given list of articles.
    Articles are classified as "media" based on present "media_url" key in parsed article.

    Args:
        articles (list[Article]): list of articles to filter

    Returns:
        list[Article]: list of all media articles from a given list
    """
    return list(filter(lambda article: article["media_url"], articles))


def filter_text_articles(articles: list[Article]) -> list[Article]:
    """Filter only text articles from a given list of articles.
    Articles are classified as "text" if their "selftext" field is not empty.

    Args:
        articles (list[Article]): list of articles to filter

    Returns:
        list[Article]: list of all text articles from a given list
    """
    return list(filter(lambda article: article["selftext"], articles))
