"""
Module responsible for accessing Reddit API via PRAW.
"""

from redditpythonapi import Article, ArticlesSortType, Reddit

from api.article_parser import parse_article
from settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_CLIENT_USER_AGENT

_reddit = Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_CLIENT_USER_AGENT,
)


async def get_subreddit_articles(
    subreddit: str, limit: int, sort: ArticlesSortType
) -> list[Article]:
    """Get a list of articles from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer articles.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many articles should be loaded
        sort (ArticlesSortType): sort type to use when accessing articles

    Returns:
        list[Article]: list of all loaded articles from given subreddit.
    """
    articles = await _reddit.subreddit_articles(subreddit, sort=sort, limit=limit)
    return list(map(parse_article, articles))


async def get_subreddit_media_articles(
    subreddit: str, limit: int, sort: ArticlesSortType
) -> list[Article]:
    """Get a list of media articles (images, GIFs, videos) from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer articles.
    Additionally, "limit" only defines how many articles are loaded from given subreddit,
    more articles will be dropped as part of "media" filtering.
    Articles are classified as "media" based on present "media_url" key in parsed article.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many articles should be loaded
        sort (ArticlesSortType): sort type to use when accessing articles

    Returns:
        list[Article]: list of all loaded media articles from given subreddit.
    """
    articles = await _reddit.subreddit_articles(subreddit, sort=sort, limit=limit)
    articles = map(parse_article, articles)
    return list(filter(lambda article: article["media_url"], articles))


async def get_subreddit_text_articles(
    subreddit: str, limit: int, sort: ArticlesSortType
) -> list[Article]:
    """Get a list of text articles from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer articles.
    Additionally, "limit" only defines how many articles are loaded from given subreddit,
    more articles will be dropped as part of "text" filtering.
    Articles are classified as "text" if their "selftext" field is not empty.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many articles should be loaded
        sort (ArticlesSortType): sort type to use when accessing articles

    Returns:
        list[Article]: list of all loaded text articles from given subreddit.
    """
    articles = await _reddit.subreddit_articles(subreddit, sort=sort, limit=limit)
    articles = map(parse_article, articles)
    return list(filter(lambda article: article["selftext"], articles))


async def get_user_articles(username: str, limit: int, sort: ArticlesSortType) -> list[Article]:
    """Get a list of articles from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer articles.

    Args:
        username (str): name of user to get data from
        limit (int): how many articles should be loaded
        sort (ArticlesSortType): sort type to use when accessing articles

    Returns:
        list[Article]: list of all loaded articles from given user.
    """
    articles = await _reddit.user_articles(username, sort=sort, limit=limit)
    return list(map(parse_article, articles))


async def get_user_image_articles(
    username: str, limit: int, sort: ArticlesSortType
) -> list[Article]:
    """Get a list of media articles (images, GIFs, videos) from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer articles.
    Additionally, "limit" only defines how many articles are loaded from given user,
    more articles will be dropped as part of "media" filtering.
    Articles are classified as "media" based on present "media_url" key in parsed article.

    Args:
        username (str): name of user to get data from
        limit (int): how many articles should be loaded
        sort (ArticlesSortType): sort type to use when accessing articles

    Returns:
        list[Article]: list of all loaded media articles from given user.
    """
    articles = await _reddit.user_articles(username, sort=sort, limit=limit)
    articles = map(parse_article, articles)
    return list(filter(lambda article: article["media_url"], articles))


async def get_user_text_articles(
    username: str, limit: int, sort: ArticlesSortType
) -> list[Article]:
    """Get a list of text articles from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer articles.
    Additionally, "limit" only defines how many articles are loaded from given user,
    more articles will be dropped as part of "text" filtering.
    Articles are classified as "text" if their "selftext" field is not empty.

    Args:
        username (str): name of user to get data from
        limit (int): how many articles should be loaded
        sort (ArticlesSortType): sort type to use when accessing articles

    Returns:
        list[Article]: list of all loaded text articles from given user.
    """
    articles = await _reddit.user_articles(username, sort=sort, limit=limit)
    articles = map(parse_article, articles)
    return list(filter(lambda article: article["selftext"], articles))
