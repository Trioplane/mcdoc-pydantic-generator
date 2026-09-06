from typing import Literal, TypedDict

VersionEntry = TypedDict('VersionEntry', {
    # ReleaseVersion '{bigint}.{bigint}.{bigint}' | '{bigint}.{bigint}'
    'id': str,
    'type': Literal['release', 'snapshot']
})

def get_latest_release(versions_list: list[VersionEntry]) -> VersionEntry:
    return next(v for v in versions_list if v['type'] == 'release')

def get_latest_snapshot(versions_list: list[VersionEntry]) -> VersionEntry:
    return next(v for v in versions_list if v['type'] == 'snapshot')

def compare_versions(versions_list: list[VersionEntry], left, right):
    left_index = next((i for i, v in enumerate(versions_list) if v['id'] == left))    
    right_index = next((i for i, v in enumerate(versions_list) if v['id'] == right))
    
    if left_index == right_index:
        return 0
    elif left_index > right_index:
        return 1
    elif left_index < right_index:
        return -1