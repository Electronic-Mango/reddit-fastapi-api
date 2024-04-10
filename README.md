# Reddit API API

[![CodeQL](https://github.com/Electronic-Mango/reddit-fastapi-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-fastapi-api/actions/workflows/codeql-analysis.yml)
[![Black](https://github.com/Electronic-Mango/reddit-fastapi-api/actions/workflows/black.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-fastapi-api/actions/workflows/black.yml)
[![Flake8](https://github.com/Electronic-Mango/reddit-fastapi-api/actions/workflows/flake8.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-fastapi-api/actions/workflows/flake8.yml)

A simple Reddit REST API allowing accessing both subreddit and user articles,
build with [`FastAPI`](https://fastapi.tiangolo.com/) and my [`Reddit Python API`](https://github.com/Electronic-Mango/reddit-python-api)!



## Table of contents

 - [Introduction and requirements](#introduction-and-requirements)
 - [Configuration](#configuration)
   - [API parameters](#api-parameters)
   - [Reddit app & required parameters](#reddit-app--required-parameters)
   - [Docker](#docker)
 - [Additional authorization](#additional-authorization)
 - [Running the API](#running-the-api)
   - [From source](#from-source)
   - [Docker](#docker-1)
 - [API endpoints](#api-endpoints)
   - [Get a list of articles from a subreddit](#get-a-list-of-articles-from-a-subreddit)
   - [Get one random article from a subreddit](#get-one-random-article-from-a-subreddit)
   - [Get a list of articles from a Reddit user](#get-a-list-of-articles-from-a-reddit-user)
   - [Get a random article from a Reddit user](#get-a-random-article-from-a-reddit-user)
 - [Filtering and article types](#filtering-and-article-types)
   - [Reddit galleries](#reddit-galleries)
 - [Load count](#load-count)
 - [Disclaimer](#disclaimer)



## Introduction and requirements

This REST API was built using [`FastAPI`](https://fastapi.tiangolo.com/), my [`Reddit Python API`](https://github.com/Electronic-Mango/reddit-python-api)  and `Python 3.11`.
Python version at least `3.11` is required.

Full list of Python requirements is in `requirements.txt` file.

Technically this API only *wraps* parts of official Reddit API, thus *Reddit API **API***.
However, accessing Reddit API itself through external services is quite cumbersome, due to necessary OAuth 2.0 authorization.
This API allows external services to access API through simple HTTP requests, without worrying about access tokens, Reddit app client, etc.
It also allows for simple access to specific services, like reading only one random article or reading only media or text articles, without any additional processing.

This API uses my simple [`Reddit Python API`](https://github.com/Electronic-Mango/reddit-python-api) to access official Reddit API.

No data is stored by the API.
Reddit is accessed in `read-only` mode.
API requests can optionally be authenticated based on request header.

You can check my other repository [Memes Discord bot Docker deployment](https://github.com/Electronic-Mango/memes-discord-bot-docker-deployment) for an example of how you can use this API in a Discord bot, deployed via Docker Compose.



## Configuration

### API parameters

API configuration can be done through a YAML configuration file.
By default `settings.yml` from the project root is used, which has some sensible defaults, other than [Reddit API client ID and secret](#reddit-app--required-parameters).

You can overwrite values from default `settings.yml` by providing a custom one under path from `CUSTOM_SETTINGS_PATH` environment variable.
In this custom YAML you can provide only parameters which you want to overwrite.
If parameter is absent in the custom one, then default value from `settings.yml` will be used.

Value for `CUSTOM_SETTINGS_PATH` can also be provided via `.env` file in the project root.


### Reddit app & required parameters

To run the API you need to first register a Reddit app at https://old.reddit.com/prefs/apps/.
There are two fields which need to be filled in `reddit` - `client` section in `settings.yml` based on your app - `id` and `secret`.
Those values will be used to acquire OAuth 2.0 token from Reddit API itself. 

No other data is necessary, since the API works in `read-only` mode.


### Docker

There's a `Dockerfile` in the repo, which will build a Docker image for the API using `python:3.12-alpine` as base.
You can set all configuration parameters using environment variables for Docker container, rather than modifying project files before building.

You can also use `docker-compose.yml` to build and start the container via:

```
docker compose up -d --build
```

Compose allows using `custom_settings.yml` in project root for custom configuration, like [Reddit app ID and secret](#reddit-app--required-parameters) without modifying project files.
By default, this file will be loaded into the image, along with all `.yml` files from the project root.

You can get around this by modifying value of `CUSTOM_SETTINGS_PATH` in `docker-compose.yml` to point to a file in a mounted volume.

Default port where API requests are handled is `8080`, which is mapped to local port `3001`.



## Additional authorization

Api has a basic authorization mechanism based on API key send as request header, separate from Reddit API OAuth 2.0.
You can set API key header name and expected value in `settings.yml` in `api` - `authorization_header` - `name` and `expected_value`.

If either of them is empty authorization will be disabled and all requests will be accepted.

If both fields are filled, then any request which doesn't have a header named `name` with value `expected_value` will be rejected with code `401`.

By default, without any changes to `settings.yml` authorization is disabled.



## Running the API

First you need to register a Reddit app and note its ID and secret.


###  From source

 1. Install all packages from `requirements.txt`
 2. Fill Reddit app ID and secret either in `settings.yml` or in a custom one
 3. Run `src/main.py` via Python


### Docker

 1. Fill Reddit app ID and secret in `settings.yml` or in `custom_settings.yml`
 2. Run `docker compose up -d --build`

You can skip `--build` flag on subsequent runs if you didn't change the source code, but keep in mind that by default `custom_settings.yml` is added to the docker image.
Any changes there will require image rebuild.

You can get around this by modifying value of `CUSTOM_SETTINGS_PATH` in `docker-compose.yml` to point to a file in a mounted volume.



## API endpoints

> [!NOTE]
> Description of all endpoint, schemas, etc. can be accessed through swagger (`/docs`), or redoc (`/redoc`).

All endpoints are accessible via `GET` requests.
If request authorization is configured incoming requests needs to have correct header and its value.

Each endpoint has a single path parameter and series of optional query parameters.
Query parameters are the same across all endpoints.

### Get a list of articles from a subreddit

```
/subreddit/list/{subreddit}
```

`subreddit` path parameter specifies which subreddit should be accessed.

Query parameters:
 * `sort` - Which Reddit sorting type to use when loading articles
 * `time` - Time period in which articles should be accessed
 * `count` - How many articles will be loaded, Reddit API uses 25 by default
 * `article_type` - Define whether to load all articles, only text or only images

`sort` can be one of the following:
 - `hot` - used by default
 - `new`
 - `rising`
 - `top`
 - `controversial`

`time` can be one of the following:
 - `hour`
 - `day`
 - `week`
 - `month`
 - `year`
 - `all`

`article_type` can be one of the following:
 - `all` - all articles
 - `media` - only media articles
 - `text` - only articles where `selftext` is not empty


Example request:
```
GET /subreddit/list/wholesomememes?count=3&sort=top
```

Example response:
```json
{
  "count": 3,
  "articles": [
    {
      "id": "1c0egcz",
      "url": "https://i.redd.it/29nc1eq3eltc1.jpeg",
      "title": "always true",
      "author": "jeremyvi",
      "nsfw": false,
      "spoiler": false,
      "selftext": "",
      "score": 18433,
      "created_utc": "2024-04-10T08:00:16",
      "permalink": "/r/wholesomememes/comments/1c0egcz/always_true/",
      "subreddit": "wholesomememes",
      "stickied": false,
      "media_url": "https://i.redd.it/29nc1eq3eltc1.jpeg"
    },
    {
      "id": "1c0kt45",
      "url": "https://i.redd.it/x16ms4i9fntc1.png",
      "title": "I wants to pet him",
      "author": "Puzzleheaded-Slip203",
      "nsfw": false,
      "spoiler": false,
      "selftext": "",
      "score": 12015,
      "created_utc": "2024-04-10T14:50:34",
      "permalink": "/r/wholesomememes/comments/1c0kt45/i_wants_to_pet_him/",
      "subreddit": "wholesomememes",
      "stickied": false,
      "media_url": "https://i.redd.it/x16ms4i9fntc1.png"
    },
    {
      "id": "1c0cv7h",
      "url": "https://i.redd.it/64qvbwu4xktc1.jpeg",
      "title": "I wanna be a weather reporter too",
      "author": "dyerama6",
      "nsfw": false,
      "spoiler": false,
      "selftext": "",
      "score": 7515,
      "created_utc": "2024-04-10T06:25:11",
      "permalink": "/r/wholesomememes/comments/1c0cv7h/i_wanna_be_a_weather_reporter_too/",
      "subreddit": "wholesomememes",
      "stickied": false,
      "media_url": "https://i.redd.it/64qvbwu4xktc1.jpeg"
    }
  ]
}
```


### Get one random article from a subreddit

```
/subreddit/random/{subreddit}
```

`subreddit` path parameter specifies which subreddit should be accessed.

All query query parameters are the same as for [loading a list of articles for a subreddit](#get-a-list-of-articles-from-a-subreddit).

`count` determines how many articles will be loaded, a random one will be selected from them.


Example request:
```
GET /subreddit/random/explainlikeimfive?count=100&sort=top&article_type=text
```

Example response:
```json
{
  "id": "1c05ako",
  "url": "https://www.reddit.com/r/explainlikeimfive/comments/1c05ako/eli5_why_was_purple_dye_so_rare_historically/",
  "title": "ELI5: Why was purple dye so rare historically?",
  "author": "Inside-Honeydew9785",
  "nsfw": false,
  "spoiler": false,
  "selftext": "I know natural purple itself was difficult to obtain, but why didn’t they just mix red and blue? Were those also rare? Did it just not work?",
  "score": 610,
  "created_utc": "2024-04-10T00:28:23",
  "permalink": "/r/explainlikeimfive/comments/1c05ako/eli5_why_was_purple_dye_so_rare_historically/",
  "subreddit": "explainlikeimfive",
  "stickied": false,
  "media_url": null
}
```


### Get a list of articles from a Reddit user

```
/user/list/{username}
```

`username` path parameter specifies which user's submissions should be accessed.

All query parameters are the same as for [loading a list of articles for a subreddit](#get-a-list-of-articles-from-a-subreddit).

Example request:
```
GET /user/list/cme_t?count=4&article_type=media&time=year
```

Example response:
```json
{
  "count": 2,
  "articles": [
    {
      "id": "1bwm2xo",
      "url": "https://i.redd.it/htb0twxhrosc1.jpeg",
      "title": "[OC][Art] The Weekly Roll Ch.150. ”One-Fifty, Baby!”",
      "author": "CME_T",
      "nsfw": false,
      "spoiler": false,
      "selftext": "",
      "score": 420,
      "created_utc": "2024-04-05T18:16:35",
      "permalink": "/r/DnD/comments/1bwm2xo/ocart_the_weekly_roll_ch150_onefifty_baby/",
      "subreddit": "DnD",
      "stickied": false,
      "media_url": "https://i.redd.it/htb0twxhrosc1.jpeg"
    },
    {
      "id": "1bviskx",
      "url": "https://i.redd.it/7v823myvkfsc1.jpeg",
      "title": "[OC] The Weekly Roll Ch. 150. \"One-Fifty, Baby!\"",
      "author": "CME_T",
      "nsfw": false,
      "spoiler": false,
      "selftext": "",
      "score": 4154,
      "created_utc": "2024-04-04T11:23:58",
      "permalink": "/r/dndmemes/comments/1bviskx/oc_the_weekly_roll_ch_150_onefifty_baby/",
      "subreddit": "dndmemes",
      "stickied": false,
      "media_url": "https://i.redd.it/7v823myvkfsc1.jpeg"
    }
  ]
}
```

Notice that 4 media articles were requested, but response only contains 2.
It's because out of 4 loaded articles only 2 were images.


### Get a random article from a Reddit user

Endpoint:
```
/user/random/{username}
```

`username` path parameter specifies which user's submissions should be accessed.

All query parameters are the same as for [loading a list of articles for a subreddit](#get-a-list-of-articles-from-a-subreddit).

`count` determines how many articles will be loaded, a random one will be selected from them.

Example request:
```
GET /user/random/cme_t?article_type=media
```

Example response:
```json
{
  "id": "1bk228v",
  "url": "https://i.redd.it/grjrcu98jnpc1.jpeg",
  "title": "The Weekly Roll Ch. 149. \"WHAT DAY IS IT?!\"",
  "author": "CME_T",
  "nsfw": false,
  "spoiler": false,
  "selftext": "",
  "score": 1529,
  "created_utc": "2024-03-21T09:56:03",
  "permalink": "/r/TheWeeklyRoll/comments/1bk228v/the_weekly_roll_ch_149_what_day_is_it/",
  "subreddit": "TheWeeklyRoll",
  "stickied": false,
  "media_url": "https://i.redd.it/grjrcu98jnpc1.jpeg"
}
```



## Filtering and article types

Other than all articles, API allows for filtering article types.
The two filters are `text` and `media`.

For `text` all articles where `selftext` is not empty are selected.

For `media` there are two cases, one for images and one for videos:

 - images are detected based on `i.redd.it` domain **OR** `post_hint` equal to `image`, since not all subreddits have `post_hint`
 - videos are detected based on `v.redd.it` domain **AND** `is_video` equal to `True`, there are some posts where domain is `v.redd.it`, but there are no necessary URLs

In case of videos, resulting `media_url` URL has `?source=fallback` trimmed out, so it ends with file extension.


### Reddit galleries

Currently, galleries won't be filtered into `media` category and their media URLs aren't easily accessible.



## Load count

When specifying how many articles should be loaded the final count can be lower.

For all articles this can occur if a given subreddit or user has fewer articles than specified.

For text and media articles the passed value only determines how many articles are loaded from Reddit overall.
This value can be later lowered as only specific type of articles are filtered from the list of all articles.
Not additional articles are loaded after filtering.

Load count also impacts retrieving one random article.
This one random article is picked from a loaded selection, instead of sending all of them.
Actual count of articles to pick from can be lowered due to additional filtering, as before.

Still, the higher the load count the lower the odds of selecting the same random article on subsequent API calls.



## Disclaimer

This bot is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with Reddit.
This is an independent and unofficial project.
Use at your own risk.
