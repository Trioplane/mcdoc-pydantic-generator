from typing import Literal

from mcdoc_pydantic_generator.base_types.models import *

type BLOCKS = NamespacedLiteralUnion[BLOCKS_SET]

type BLOCKS_SET = NO_NAMESPACE_BLOCKS_SET | MINECRAFT_NAMESPACED_BLOCKS_SET

type NO_NAMESPACE_BLOCKS_SET = Literal[
    'block1',
    'block2',
    'block3'
]

type MINECRAFT_NAMESPACED_BLOCKS_SET = Literal[
    'minecraft:block1',
    'minecraft:block2',
    'minecraft:block3'
]