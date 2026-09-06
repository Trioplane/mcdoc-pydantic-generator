from pathlib import Path

import rich

from mcdoc_pydantic_generator.index import (
    fetch_block_states,
    fetch_mcdoc,
    fetch_registries,
    vanilla_mcdoc_src,
)


def test_fetch_mcdoc_from_url():
    fetch_mcdoc(vanilla_mcdoc_src[0])
    #print(mcdoc)
    
def test_fetch_mcdoc_from_local_file():
    fetch_mcdoc(Path("trp_local", "symbols.json"))
    
def test_fetch_registries():
    rich.inspect(fetch_registries("26.2"))
    #print(registries)
    
def test_fetch_block_states():
    rich.inspect(fetch_block_states("26.2"))
    #print(block_states)
    