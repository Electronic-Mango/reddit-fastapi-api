"""
Custom converter used for converting string endpoint paramters to ArticlesSortType.
"""

from redditpythonapi import ArticlesSortType
from werkzeug.routing import BaseConverter


class SortTypeConverter(BaseConverter):
    def to_python(self, value: str) -> ArticlesSortType:
        return ArticlesSortType[value.upper()]

    def to_url(self, value: ArticlesSortType) -> str:
        return value.name.lower()
