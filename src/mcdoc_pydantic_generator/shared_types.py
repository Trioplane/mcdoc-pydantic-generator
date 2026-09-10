from typing import Any
from typing_extensions import TypedDict

SymbolEntry = TypedDict('SymbolEntry', {
    'source': str,
    'type_def': dict[str, Any]
})

type SymbolMap = dict[str, SymbolEntry] | dict[str, dict[str, SymbolEntry]]

SymbolTable = TypedDict('SymbolTable', {
    'mcdoc': dict[str, SymbolEntry],
    'mcdoc/dispatcher': dict[str, dict[str, SymbolEntry]],
}, extra_items=Any)