from mcdoc_pydantic_generator.typegen.export import export_registry, export_registry_sets, export_dispatchers
import logging
from mcdoc_pydantic_generator.index import SymbolTable, SymbolEntry, SymbolMap
from typing import Any, ClassVar
from pydantic import BaseModel


logger = logging.getLogger("mcdoc-pydantic-generator")

class ResolvedSymbol(BaseModel):
    paths: set[str]
    imports: Any # NotImplemented for now.
    exports: Any # NotImplemented for now.

class ResolvedRegistry(BaseModel):
    import_path: str
    registry: Any # NotImplemented for now.

class ResolvedDispatcher(BaseModel):
    import_path: str
    type: Any # NotImplemented for now.
    
    generic_count: int
    """Number of required generic parameters (excluding CASE)"""
    
    symbol_name: str
    """The symbol type name (e.g., "SymbolDataComponent")"""

class DispatcherInfo(BaseModel):
    """
        Pre-computed dispatcher info for use during type resolution.
        Maps dispatcher ID (e.g., 'minecraft:entity_effect') to symbol info.
    """
    
    symbol_name: str
    """The symbol type name (e.g., "SymbolEntityEffect")"""
    
    generic_count: int
    """Number of generic parameters (excluding CASE)"""
    
    has_fallback_type: bool
    """Whether this dispatcher has a %unknown member (exports FallbackType)"""
    
    supports_none: bool
    """Whether this dispatcher has a %none member"""

class TypesGenerator:
    
    def __init__(self):
        self.resolved_registries: dict[str, ResolvedRegistry] = {}
        
        self.resolved_symbols: dict[str, ResolvedSymbol] = {}
        
        self.resolved_dispatchers: dict[str, ResolvedDispatcher] = {}
        
        self.dispatcher_info: dict[str, DispatcherInfo] = {}
        """Pre-computed dispatcher info for use during type resolution"""
    
    def resolve_types(self, symbols: SymbolTable, translation_keys: list[str]):
        logger.debug('registries')
        self.__resolve_registry_symbols(symbols, translation_keys)
        registry_exports = export_registry(self.resolved_registries)
        self.resolved_symbols['::java::registry'] = registry_exports
        
        registry_sets_exports = export_registry_sets(self.resolved_registries)
        self.resolved_symbols['::java::registry-sets'] = registry_sets_exports
        
        dispatchers = symbols['mcdoc/dispatcher']
        
        # Pre-compute dispatcher info before resolving modules
        logger.debug('dispatcher info')
        self.__precompute_dispatcher_info(dispatchers)
        
        logger.debug('modules')
        module_map = symbols['mcdoc']
        self.__resolve_module_symbols(module_map, symbols)

        logger.debug('dispatchers')
        self.__resolve_dispatcher_symbols(dispatchers, module_map, symbols)

        # NotImplemented yet.
        #dispatcher_exports = export_dispatchers(dispatcher_symbol_paths)
        #self.resolved_symbols['::java::dispatcher'] = dispatcher_exports
        
    def __precompute_dispatcher_info(self, dispatchers: SymbolMap):
        return NotImplemented
        
    def __resolve_registry_symbols(self, symbols: SymbolTable, translation_keys: list[str]):
        return NotImplemented
    
    def __resolve_module_symbols(self, module_map: SymbolMap, symbols: SymbolTable):
        return NotImplemented
    
    def __resolve_dispatcher_symbols(self, dispatchers: SymbolMap, module_map: SymbolMap, symbols: SymbolTable):
        return NotImplemented