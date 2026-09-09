import os
import re

TYPE_PREFIX = os.getenv('MCDOC_TYPE_PREFIX', '')

has_lowercase = r'[a-z]'

def prefix_name(name: str) -> str:
    if TYPE_PREFIX == '':
        return name
    
    if re.search(has_lowercase, name):
        return f'{TYPE_PREFIX}{name}'
    
    return f'{TYPE_PREFIX.upper()}{name}'

def pluralize(name: str) -> str:
    # Words ending in vowel + y get 's' (e.g., display -> displays, key -> keys)
    if re.search(r'(?i)[aeiou]y$', name):
        return f'{name}s'
    
    # Words ending in consonant + y get 'ies' (e.g., entity -> entities)
    if name.endswith('y'):
        return f'{name[0:-1]}ies'
    
    # Words ending in common plural consonant + s are likely already plural
    # e.g., methods (ds), patterns (ns), events (ts), fonts (ts), items (ms)
    # Excludes ss, which needs -es (boss -> bosses)
    if re.search(r'(?i)[bdfgklmnprtvw]s$', name):
        return name
    
    # Words ending in s, ch, sh, x, z get 'es'
    if name.endswith(('s', 'ch', 'sh', 'x', 'z')):
        return f'{name}es'
    
    return f'{name}s'