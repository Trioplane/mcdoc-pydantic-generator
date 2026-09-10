import ast

from pydantic import BaseModel, ConfigDict

type TypeHandlerResultImports = set[tuple[str, str]]
class TypeHandlerResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    type: ast.AST
    imports: TypeHandlerResultImports

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