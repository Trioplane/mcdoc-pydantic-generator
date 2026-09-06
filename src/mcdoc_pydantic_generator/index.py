import logging
import re
import time
from pathlib import Path
from typing import Any, Literal, NotRequired
from typing_extensions import TypedDict

import requests
import rich
from beet import LATEST_MINECRAFT_VERSION
from pydantic import BaseModel, ConfigDict

from mcdoc_pydantic_generator import derived
from mcdoc_pydantic_generator.util.fetch import fetch_one
from mcdoc_pydantic_generator.util.version import VersionEntry, get_latest_snapshot

logger = logging.getLogger('mcdoc-pydantic-generator')

VANILLA_MCDOC_SOURCES = [
  'https://api.spyglassmc.com/vanilla-mcdoc/symbols',
  'https://raw.githubusercontent.com/SpyglassMC/vanilla-mcdoc/refs/heads/generated/symbols.json',
]
VANILLA_MCDOC_URI = 'mcdoc://vanilla-mcdoc/symbols.json'


class GeneratorOptions(BaseModel):
    mcdoc_symbols_src: str | Path | None = None
    minecraft_version: str = LATEST_MINECRAFT_VERSION
    out_dir: str | None = 'types'
    
McdocSymbols = TypedDict('McdocSymbols', {
    'ref': NotRequired[str],
    'mcdoc': dict[str, Any],
    'mcdoc/dispatcher': dict[str, dict[str, Any]]
}, extra_items=Any)

def fetch_mcdoc(mcdoc_symbols_src: str | Path) -> McdocSymbols:
    try:
        fetched_src = fetch_one(mcdoc_symbols_src)
        fetched_src.raise_for_status()
    
        return fetched_src.json()
    except Exception:
        logger.error('Error occured while fetching mcdoc')
        raise

def fetch_registries(version_id: str) -> tuple[dict[str, list[str]], str | None]:
    logger.debug(f"[fetch_registries] {version_id}")

    try:
        req = fetch_one(f'https://api.spyglassmc.com/mcje/versions/{version_id}/registries')
        etag = req.headers.get("ETag")
        
        data: dict[str, list[str]] = req.json()
        
        result = {}
        for id in data:  # noqa: PLC0206
            result[id] = [f"minecraft:{entry}" for entry in data[id]]
        
        return (result, etag)
    except Exception:
        logger.error('Error occured while fetching registries')
        raise

def fetch_block_states(version_id: str) -> tuple[derived.McmetaStates, str | None]:
    logger.debug(f'[fetch_block_states] {version_id}')

    try:
        req = fetch_one(f'https://api.spyglassmc.com/mcje/versions/{version_id}/block_states')
        etag = req.headers.get("ETag")
        
        data: derived.McmetaStates = req.json()
        
        result = data
        # Note. in mcdoc-ts-parser, this is a map which is why it had to do a for loop to copy data to result.
        #   Here, we just set result to data to be faithful to mcdoc-ts-generator on its var names, 
        #   even though this is redundant code.
        
        return (result, etag)
    except Exception:
        logger.error('Error occurred while fetching block states')
        raise

def fetch_translation_keys() -> list[str]:
    logger.debug('[fetch_translation_keys] latest from github')
    try:
        req = fetch_one('https://raw.githubusercontent.com/misode/mcmeta/refs/heads/assets-tiny/assets/minecraft/lang/en_us.json')
        data: dict[str, str] = req.json()
        return [f'minecraft:{key}' for key in data]
    except Exception:
        logger.error('Error occurred while fetching translation keys')
        raise

# Version logic inside initialize in mcdoc-ts-generator, simplified
# Can fix later to actually get the correct versions depending on the minor release.
def fetch_version(target_version: str) -> str:
    logger.debug(f'[fetch_version] {target_version}')
    
    try:
        req = fetch_one('https://api.spyglassmc.com/mcje/versions')
        versions: list[VersionEntry] = req.json()
    except Exception:
        logger.error('Error occurred while fetching versions')
        raise
    
    version = next((v for v in versions if v['id'] == target_version), None)
    
    if version is None:
        logger.warning(f'{target_version} has no exact release on Spyglass; falling back to latest snapshot.')
        version = get_latest_snapshot(versions)
        
    release = version["id"]
    
    return release
    
class SymbolEntry(BaseModel):
    source: str
    type_def: dict[str, Any]

class SymbolTable(BaseModel):
    model_config = ConfigDict(extra='allow')
    
    mcdoc: dict[str, SymbolEntry] = {}
    dispatchers: dict[str, dict[str, SymbolEntry]] = {}
    
class SymbolCollisionError(Exception):
    pass

def mcdoc_registrar(table: SymbolTable, source: str, symbols: McdocSymbols) -> None:
    """Push symbols to a shared table and tag them with source so we have verbose errors in case of collision."""
    start = time.perf_counter()
    
    for id, type_def in symbols["mcdoc"].items():
        if id in table.mcdoc:
            raise SymbolCollisionError(f'Ids collided on {id} from {table.mcdoc[id].source} and {source}')
        else:
            table.mcdoc[id] = SymbolEntry(source=source, type_def=type_def)

    for dispatcher, members in symbols["mcdoc/dispatcher"].items():
        table.dispatchers.setdefault(dispatcher, {})
        for member_id, type_def in members.items():
            if member_id in table.dispatchers[dispatcher]:
                raise SymbolCollisionError(f'Member ids collided on {member_id} from dispatchers {table.dispatchers[dispatcher][member_id].source} and input symbols {source}')
            else:
                table.dispatchers[dispatcher][member_id] = SymbolEntry(source=source, type_def=type_def)
                
    for resource_category, resource_category_entries in symbols.items():
        if resource_category in ('mcdoc', 'mcdoc/dispatcher', 'ref'):
            continue
        
        setattr(table, resource_category, [])
        for entry in resource_category_entries:
            if entry in table.__pydantic_extra__[resource_category]:  # ty: ignore[not-subscriptable]
                logger.debug(f'Re-entry of {entry} in {resource_category}.')
            
            table.__pydantic_extra__[resource_category].append(entry)  # ty: ignore[not-subscriptable]
        
        
                
    duration = (time.perf_counter() - start) * 1000
    logger.debug(f'[mcdoc_registrar] Done in {duration}ms')
    
# skip initialize, its spyglass stuff
    
def generate(options: GeneratorOptions):
    symbol_table = SymbolTable()
    
    # Fetch and register vanilla mcdoc to symbol table
    vanilla_mcdoc_data: tuple[McdocSymbols, str] | None = None
    
    for vanilla_mcdoc_source in VANILLA_MCDOC_SOURCES:
        try:
            fetched_mcdoc = fetch_mcdoc(vanilla_mcdoc_source)
            vanilla_mcdoc_data = (fetched_mcdoc, vanilla_mcdoc_source)
            break
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise
            
            logger.warning(e)
            continue
    
    if vanilla_mcdoc_data is None:
        raise requests.HTTPError("Could not fetch vanilla-mcdoc from Spyglass API and GitHub.")
    
    mcdoc_registrar(
        table=symbol_table,
        source=vanilla_mcdoc_data[1],
        symbols=vanilla_mcdoc_data[0]
    )
    
    # Add registries to the symbol table
    version = fetch_version(options.minecraft_version)
    
    registries, registries_etag = fetch_registries(version)
    block_states, block_states_etag = fetch_block_states(version)
    fluids: derived.McmetaStates = derived.Fluids
    translation_keys = fetch_translation_keys()
    
    # TODO: Transform all of that above into mcdoc symbols and register into symbol table
    
    # == @spyglassmc/java-edition/src/dependency/mcmeta.ts > symbolRegistrar > addStatesSymbols
    state_types = {'block': block_states, 'fluid': fluids}
    state_type_mcdoc_symbols: McdocSymbols = {
        'mcdoc': {},
        'mcdoc/dispatcher': {},
    }
    for _type, states in state_types.items():
        current_mcmeta_state = f'mcdoc:{_type}_states'
        current_mcmeta_state_keys = f'mcdoc:{_type}_state_keys'
        
        state_type_mcdoc_symbols['mcdoc/dispatcher'].setdefault(current_mcmeta_state, {})
        state_type_mcdoc_symbols['mcdoc/dispatcher'].setdefault(current_mcmeta_state_keys, {})
        
        for id, [properties, _]in states.items():
            state_type_def_symbol_data = {
                'kind': 'struct',
                'fields': [{
                    'kind': 'pair',
                    'key': prop_key,
                    'optional': True,
                    'type': {
                        'kind': 'union',
                        'members': [{
                            'kind': 'literal',
                            'value': { 'kind': 'string', value: value }
                        } for value in prop_value]
                    }
                } for prop_key, prop_value in properties.items()]
            }
            state_type_mcdoc_symbols['mcdoc/dispatcher'][current_mcmeta_state][id] = state_type_def_symbol_data
        
            state_keys_type_def_symbol_data = {
                'kind': 'union',
                'members': [{
                    'kind': 'literal',
                    'value': { 'kind': 'string', 'value': prop_key }
                } for prop_key in properties]
            }
            state_type_mcdoc_symbols['mcdoc/dispatcher'][current_mcmeta_state_keys][id] = state_keys_type_def_symbol_data
        
    mcdoc_registrar(
        table=symbol_table,
        source='MCMETA_STATES',
        symbols=state_type_mcdoc_symbols
    )
        
    # TODO: == @spyglassmc/java-edition/src/dependency/mcmeta.ts > symbolRegistrar > addRegistrySymbols
    registry_mcdoc_symbols: McdocSymbols = {
        'mcdoc': {},
        'mcdoc/dispatcher': {}
    }
    
    for registry_id, registry in registries.items():
        if registry_id in (*derived.FileCategories, *derived.RegistryCategories):
            for entry_id in registry:
                registry_mcdoc_symbols.setdefault(registry_id, [])  # ty: ignore[no-matching-overload]
                registry_mcdoc_symbols[registry_id].append(entry_id)  # ty: ignore[unresolved-attribute]
                
    mcdoc_registrar(
        table=symbol_table,
        source='MCMETA_REGISTRIES',
        symbols=registry_mcdoc_symbols
    )
    
    # TODO: == @spyglassmc/java-edition/src/dependency/mcmeta.ts > symbolRegistrar > addBuiltinSymbols 
            
        
    
    # TODO: register the input mcdoc symbols here?
    
    
    return symbol_table
    
if __name__ == '__main__':
    rich.print(generate(GeneratorOptions()).__pydantic_extra__['advancement'])