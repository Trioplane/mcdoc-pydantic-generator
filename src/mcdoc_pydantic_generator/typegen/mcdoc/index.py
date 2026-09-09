import ast

from pydantic import BaseModel, ConfigDict

type TypeHandlerResultImports = dict[str, set[str]]
class TypeHandlerResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    type: ast.AST
    imports: TypeHandlerResultImports