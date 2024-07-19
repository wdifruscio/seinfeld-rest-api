
# API Documentation

## Overview

This API provides access to quotes and utterances from the Seinfeld TV show. The endpoints support filtering, pagination, rate limiting, and caching. Below is the detailed documentation of the available endpoints.

## Endpoints

### `QuoteViewSet`

#### `GET /quotes/`

Retrieve a list of quotes.

- **Rate Limit**: 30 requests per hour per IP address.
- **Caching**: Enabled.
- **Pagination**: Supports page size and maximum page size.

**Example Request:**

```http
GET /quotes/ 

```

**Example Response:**

```json
{
    "count": 100,
    "next": "/quotes/?page=2",
    "previous": null,
    "results": [
        {
            "text": "(pointing at George's shirt) See, to me, that button is in the worst possible spot.",
            "info": {
                "speaker": "JERRY",
                "season_number": 1,
                "episode_number": 1,
                "title": "Good News, Bad News",
                "date": "July 5, 1989",
                "writer": "Larry David, Jerry Seinfeld",
                "director": "Art Wolff"
            }
        },
        ...
    ]
}
```

#### `GET /quotes/{id}/`

Retrieve a specific quote by ID.

- **Rate Limit**: 30 requests per hour per IP address.
- **Caching**: Enabled.

**Example Request:**

```http
GET /quotes/52627/ 
```

**Example Response:**

```json
        {
            "id": 52627,
            "text": "'These pretzels are making me thirsty!!'",
            "info": {
                "speaker": "GEORGE",
                "season_number": 3,
                "episode_number": 11,
                "title": "The Alternate Side",
                "date": "December 4, 1991",
                "writer": "Larry David and Bill Masters",
                "director": "Tom Cherones"
            }
        },
```

#### `GET /quotes/random/`

Retrieve a random quote.

- **Rate Limit**: 30 requests per hour per IP address.

**Example Request:**

```http
GET /quotes/random/ 
```

### `UtteranceViewSet`

#### `GET /utterances/`

Retrieve a list of utterances.

- **Rate Limit**: 30 requests per hour per IP address.
- **Caching**: Enabled.
- **Pagination**: Supports page size and maximum page size.

**Example Request:**

```http
GET /utterances/ 
```

**Example Response:**

```json
{
    "count": 200,
    "next": "/utterances/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "text": "(pointing at George's shirt) See, to me, that button is in the worst possible spot. The second button literally makes or breaks the shirt, look at it. It's too high! It's in no-man's-land. You look like you live with your mother.",
            "info": {
                "speaker": "JERRY",
                "season_number": 1,
                "episode_number": 1,
                "title": "Good News, Bad News",
                "date": "July 5, 1989",
                "writer": "Larry David, Jerry Seinfeld",
                "director": "Art Wolff"
            }
        },
        ...
    ]
}
```

#### `GET /utterances/{id}/`

Retrieve a specific utterance by ID.

- **Rate Limit**: 30 requests per hour per IP address.
- **Caching**: Enabled.

**Example Request:**

```http
GET /utterances/1/ 

```

**Example Response:**

```json
{
    "id": 1,
    "character": "Jerry",
    "text": "I don't want to be a pirate!"
}
```

## Filters

Both `QuoteViewSet` and `UtteranceViewSet` support filtering using `SentenceFilter`. You can filter by the following fields:

- `speaker`: Filter by the speaker of the utterance.
- `episode_id`: Filter by the episode ID.
- `season`: Filter by the season of the episode.
- `writer`: Filter by the writer of the episode.
- `director`: Filter by the director of the episode.
- `title`: Filter by the title of the episode.
- `length`: Filter by the length of the quote.
- `search`: Filter by a search term in the quote text.

**Filter by Speaker:**

```http
GET /quotes/?speaker=Jerry 
```