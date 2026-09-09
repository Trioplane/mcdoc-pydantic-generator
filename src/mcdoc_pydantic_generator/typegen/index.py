import ast
import logging
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict

from mcdoc_pydantic_generator.index import SymbolEntry, SymbolMap, SymbolTable
from mcdoc_pydantic_generator.typegen.export import (
    export_dispatchers,
    export_registry,
    export_registry_sets,
)
from mcdoc_pydantic_generator.typegen.mcdoc.index import (
    TypeHandlerResultImports,
)
from mcdoc_pydantic_generator.util.index import pluralize, prefix_name
from mcdoc_pydantic_generator import base_types

from .. import derived

logger = logging.getLogger("mcdoc-pydantic-generator")

class ResolvedSymbol(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    paths: set[str]
    imports: TypeHandlerResultImports
    exports: list[ast.AST]

class ResolvedRegistry(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    import_path: str
    registry: ast.AST

class ResolvedDispatcher(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    import_path: str
    type: ast.AST
    
    generic_count: int
    """Number of required generic parameters (excluding CASE)"""
    
    symbol_name: str
    """The symbol type name (e.g., "SymbolDataComponent")"""

class DispatcherInfo(BaseModel):
    """
        Pre-computed dispatcher info for use during type resolution.
        Maps dispatcher ID (e.g., 'minecraft:entity_effect') to symbol info.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
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
        
    def __resolve_registry_symbols(self, registries: SymbolTable, translation_keys: list[str]):
        for registry_name in derived.AllCategories:
            if registry_name in derived.McdocCategories:
                continue
            
            # Sorted - the symbol table's iteration order isn't stable between runs,
            # and this list is emitted verbatim as the registry's SET contents.
            registry = translation_keys if registry_name == 'translation_key' else sorted(registries[registry_name], key=str.casefold)
            
            if len(registry) == 0: continue
            
            type_name = pluralize("_".join(registry_name.split('/')).upper())
            symbol_path = f'::java::_registry::{type_name.lower()}'
            
            # `type_name` stays canonical - it spells the output file path and the
            # import path other modules look us up by. `emit_name` is what actually
            # gets declared.
            
            emit_name = prefix_name(type_name)
            set_name = f'{emit_name}_SET'
            
            is_sounds = registry_name == 'sound'
            literal_union_type = 'LiteralUnion' if is_sounds else 'NamespacedLiteralUnion'
            
            # export type EMIT_NAME = (literal_union_type<SetType<typeof set_name>> | `minecraft:${SetType<typeof set_name>}`)
            self.resolved_symbols[symbol_path] = ResolvedSymbol(
                paths=set(),
                imports={},
                exports=[
                    ast.ImportFrom(
                        module='typing',
                        names=[
                            ast.alias(name='Literal')
                        ],
                        level=0
                    ),
                    base_types.models._IMPORT_AST,
                    ast.TypeAlias(
                        name=ast.Name(id=emit_name, ctx=ast.Store()),
                        value=ast.Subscript(
                            value=ast.Name(id='NamespacedLiteralUnion', ctx=ast.Load()),
                            slice=ast.Name(id=set_name, ctx=ast.Load()),
                            ctx=ast.Load()
                        )
                    )
                ]
            )
            
    def __resolve_module_symbols(self, module_map: SymbolMap, symbols: SymbolTable):
        return NotImplemented
    
    def __resolve_dispatcher_symbols(self, dispatchers: SymbolMap, module_map: SymbolMap, symbols: SymbolTable):
        return NotImplemented