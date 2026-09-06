from pathlib import Path

import rich

from mcdoc_pydantic_generator.index import (
    VANILLA_MCDOC_SOURCES,
    fetch_block_states,
    fetch_mcdoc,
    fetch_registries,
    fetch_translation_keys,
    fetch_version,
)


def test_fetch_mcdoc_from_url():
    fetch_mcdoc(VANILLA_MCDOC_SOURCES[0])
    #print(mcdoc)
    
def test_fetch_mcdoc_from_local_file():
    fetch_mcdoc(Path("trp_local", "symbols.json"))
    
def test_fetch_registries():
    rich.inspect(fetch_registries("26.2"))
    #print(registries)
    
def test_fetch_block_states():
    rich.inspect(fetch_block_states("26.2"))
    #print(block_states)
    
def test_fetch_translation_keys():
    rich.inspect(fetch_translation_keys())
    
def test_fetch_version():
    assert fetch_version("24w46a") == "24w46a"
    assert fetch_version("1.21.1") == "1.21.1"
    assert fetch_version("1.21.1") == "1.21.1"
    assert fetch_version("26.1-snapshot-1") == "26.1-snapshot-1"
    assert fetch_version("26.2") == "26.2"
    assert fetch_version("26.3-pre-1") == "26.3-pre-1"
    
    invalid_version = "999.999"
    fetched_invalid_version = fetch_version(invalid_version)
    rich.print(fetched_invalid_version)
    assert fetched_invalid_version != invalid_version