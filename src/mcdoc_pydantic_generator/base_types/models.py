import ast
from typing import Annotated

from pydantic import Field

__all__ = [
    "LiteralUnion",
    "NamespacedLiteralUnion"
]

ResourceLocationRegex = r'^[a-z\d_\-\.]*:[a-z\d_\-\./]*$'

NonEmptyString = Annotated[str, Field(min_length=1)]
NamespacedString = Annotated[str, Field(pattern=ResourceLocationRegex)]

type LiteralUnion[T] = T | NonEmptyString
type NamespacedLiteralUnion[T] = T | NamespacedString

_IMPORT_AST = ast.ImportFrom(
    module='mcdoc_pydantic_generator.base_types.models',
    names=[
        ast.alias(name='*')
    ],
    level=0
)