import hashlib
import json
import logging
from pathlib import Path
from typing import TypedDict

import requests
from beet import Cache
from requests import Response

logger = logging.getLogger("mcdoc_pydantic_generator")

CachedResponseJSON = TypedDict('CachedResponseJSON', {
    "status_code": int,
    "_content": str,
    "headers": dict[str, str]
})

def fetch_one(input: str | Path, cache: Cache | None = None) -> Response:
    if isinstance(input, str):
        return fetch_http(input=input, cache=cache)
    elif isinstance(input, Path):
        return fetch_path(input)
    else:
        raise TypeError("fetch_one only supports http URLs and Paths.")
    
def fetch_path(path: Path) -> Response:
    if not path.exists():
        raise FileNotFoundError(f"File not found in {path.as_posix()}")
    
    response = Response()
    response.url = path.absolute().as_uri()
    response.status_code = 200
    response._content = path.read_bytes()
    
    # use sha1 as etag
    with path.open("rb") as file:
        sha1 = hashlib.file_digest(file, "sha1").hexdigest()
            
    response.headers = {"ETag": sha1}
    
    return response
    

def fetch_http(input: str, cache: Cache | None = None) -> Response:
    headers: dict[str, str] = {}
    
    _cache = cache or Cache(".mcdoc_pydantic_generator_cache")
    cache_path = _cache.get_path(input)
    
    # gitignore cache
    if not (_cache.directory / ".gitignore").exists():
        gitignore = _cache.directory / ".gitignore"
        gitignore.write_text(
            "# Automatically created by mcdoc-pydantic-generator\n"
            "*\n"
        )
    
    # Load the json representation of response and rebuild the response class
    cached_response_json: CachedResponseJSON = json.loads(cache_path.read_text()) if cache_path.exists() else None
    
    cached_response: Response = None
    
    if cached_response_json is not None:
        cached_response = Response()
        cached_response.url = input
        cached_response.status_code = cached_response_json["status_code"]
        cached_response.headers = cached_response_json["headers"]
        cached_response._content = cached_response_json["_content"].encode()
    
    cached_etag = cached_response.headers.get("ETag") if cached_response is not None else None

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

    # Build cached json representation of response
    response_to_cache: CachedResponseJSON = {
        "status_code": response.status_code,
        "headers": {"ETag": response.headers["ETag"]},
        "_content": json.dumps(response.json())
    }
    cache_path.write_text(json.dumps(response_to_cache))
    _cache.flush()
    
    return response