from pydantic import BaseModel

from .index import ResolvedRegistry, ResolvedSymbol


class ExportDispatchersPathsArgument(BaseModel):
    symbol_name: str
    base_name: str
    has_fallback_type: str


def export_dispatchers(paths: dict[str, ExportDispatchersPathsArgument]) -> ResolvedSymbol:
    """
        Generates named export statements for all dispatcher symbols.
        ⚠ Exports `SymbolName` and optionally `NameFallbackType` when %unknown is present.
        (⚠ FROM MCDOC-TS-GENERATOR)
    """
    return NotImplemented

def export_registry_sets(resolved_registries: dict[str, ResolvedRegistry]) -> ResolvedSymbol:
    """
        Generates re-exports for all registry SET constants.
        ⚠ Creates: `export { BLOCKS_SET } from './_registry/blocks'` etc. 
        (⚠ FROM MCDOC-TS-GENERATOR)
    """
    return NotImplemented

def export_registry(resolved_registries: dict[str, ResolvedRegistry]):
    return NotImplemented
