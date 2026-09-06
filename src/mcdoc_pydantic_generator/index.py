import logging
from pathlib import Path
from typing import Any, TypedDict

import requests
from pydantic import BaseModel

from mcdoc_pydantic_generator.util.fetch import fetch_one

logger = logging.getLogger("mcdoc-pydantic-generator")

vanilla_mcdoc_src = [
  'https://api.spyglassmc.com/vanilla-mcdoc/symbols',
  'https://raw.githubusercontent.com/SpyglassMC/vanilla-mcdoc/refs/heads/generated/symbols.json',
]

class GeneratorOptions(BaseModel):
    mcdoc_symbols_src: str | None = vanilla_mcdoc_src[0]
    out_dir: str | None = "types"
    
McdocSymbols = TypedDict('McdocSymbols', {
    "ref": str,
    "mcdoc": dict[str, Any],
    "mcdoc/dispatcher": dict[str, dict[str, Any]]
})
    
def fetch_mcdoc(mcdoc_symbols_src: str | Path) -> McdocSymbols:
    try:
        fetched_src = fetch_one(mcdoc_symbols_src)
        fetched_src.raise_for_status()
    
        return fetched_src.json()
    except requests.RequestException:
        logger.error("Error occured while fetching mcdoc")
        raise

def fetch_registries(version_id: str):
    logger.debug(f"[fetch_registries] {version_id}")

    try:
        req = fetch_one(f"https://api.spyglassmc.com/mcje/versions/{version_id}/registries")
        etag = req.headers["ETag"]
        
        data: McdocSymbols = req.json()
        
        result = {}
        for id in data:
            result[id] = [f"minecraft:{e}" for e in data[id]]  # ty: ignore[invalid-key]
        
        return [result, etag]
    except requests.RequestException:
        logger.error("Error occured while fetching registries")
        raise
    
type BlockStateData = tuple[dict[str, list[str]], dict[str, str]]

def fetch_block_states(version_id: str):
    logger.debug(f"[fetch_block_states] {version_id}")

    try:
        req = fetch_one(f"https://api.spyglassmc.com/mcje/versions/{version_id}/block_states")
        etag = req.headers["ETag"]
        
        data: dict[str, BlockStateData] = req.json()
        
        result = {}
        
        for id in data:  # noqa: PLC0206
            result[id] = data[id]
            
        return [result, etag]
    except requests.RequestException as e:
        logger.warning(f"Error occurred while fetching block states: {e!r}")
    
