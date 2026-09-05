import logging

import requests
from beet import Cache
from requests import Response

cache = Cache("mcdoc_pydantic_generator")
logger = logging.getLogger("mcdoc_pydantic_generator")

def fetch_one(input: str) -> Response:
    headers: dict[str, str] = {}
    
    cached_response = cache.json.get(input)
    cached_etag = cached_response["headers"].get("ETag") if cached_response is not None else None

    if cached_etag is not None:
        headers['If-None-Match'] = cached_etag
        
    response: Response
    try:
        response = requests.get(input, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.warning(f"[fetch_with_cache] fetch {e}")
        
        if cached_response is not None:
            logger.info(f"[fetch_with_cache] falling back to cache for {input}")
            return cached_response
        
        raise
    
    if response.status_code == 304:
        logger.info(f"[fetch_with_cache] reusing cache for {input}")
        assert cached_response is not None
        return cached_response
    
    if response.status_code != 200:
        raise requests.HTTPError(f"fetch_with_cache: {input} returned {response.status_code}")

    cache.json[input] = response
    print(cache.json[input])
    return response