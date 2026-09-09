"""Data derived from @spyglassmc/java-edition"""

# == @spyglassmc/java-edition/src/dependency/mcmeta.ts > Fluids
type McmetaStates = dict[
    str, tuple[dict[str, list[str]], dict[str, str]]
]

Fluids: McmetaStates = {
	'flowing_lava': ({ 'falling': ['false', 'true'], 'level': ['1', '2', '3', '4', '5', '6', '7', '8'] }, {
		'falling': 'false',
		'level': '1',
	}),
	'flowing_water': (
		{ 'falling': ['false', 'true'], 'level': ['1', '2', '3', '4', '5', '6', '7', '8'] },
		{ 'falling': 'false', 'level': '1' },
    ),
	'lava': ({ 'falling': ['false', 'true'] }, { 'falling': 'false' }),
	'water': ({ 'falling': ['false', 'true'] }, { 'falling': 'false' }),
}

# == @spyglassmc/core/src/symbol/Symbols.ts > FileCategories

McdocCategories = ('mcdoc', 'mcdoc/dispatcher')

RegistryCategories = (
    'activity',
    'armor_material', # Removed
    'attribute',
    'attribute_type',
    'block',
    'block_entity_type',
    'block_predicate_type',
    'block_type', # Removed
    'chunk_status',
    'command_argument_type',
    'consume_effect_type',
    'context_float_provider_type',
    'context_int_provider_type',
    'creative_mode_tab',
    'custom_stat',
    'data_component_predicate_type',
    'data_component_type',
    'debug_subscription',
    'decorated_pot_pattern', # Removed as registry
    'decorated_pot_patterns', # Removed
    'dialog_action_type',
    'dialog_body_type',
    'dialog_type',
    'enchantment_effect_component_type',
    'enchantment_entity_effect_type',
    'enchantment_level_based_value_type',
    'enchantment_location_based_effect_type',
    'enchantment_provider_type',
    'enchantment_value_effect_type',
    'entity_sub_predicate_type',
    'entity_type',
    'environment_attribute',
    'float_provider_type',
    'fluid',
    'game_event',
    'game_rule',
    'height_provider_type',
    'incoming_rpc_methods',
    'input_control_type',
    'instrument',
    'int_provider_type',
    'item',
    'item_sub_predicate_type', # Removed
    'loot_condition_type',
    'loot_function_type',
    'loot_nbt_provider_type',
    'loot_number_provider_type', # Removed
    'loot_pool_entry_type',
    'loot_score_provider_type',
    'map_decoration_type',
    'memory_module_type',
    'menu',
    'mob_effect',
    'motive', # Removed
    'number_format_type',
    'outgoing_rpc_methods',
    'particle_type',
    'permission_check_type',
    'permission_type',
    'point_of_interest_type',
    'pos_rule_test',
    'position_source_type',
    'potion',
    'recipe_book_category',
    'recipe_display',
    'recipe_serializer',
    'recipe_type',
    'rule_block_entity_modifier',
    'rule_test',
    'schedule', # Removed
    'sensor_type',
    'slot_display',
    'slot_source_type',
    'sound_event',
    'spawn_condition_type',
    'stat_type',
    'test_environment_definition_type',
    'test_function',
    'test_instance_type',
    'trigger_type',
    'ticket_type',
    'villager_profession',
    'villager_type',
    'worldgen/biome_source',
    'worldgen/block_placer_type', # Removed
    'worldgen/block_state_provider_type',
    'worldgen/carver', # Removed as registry
    'worldgen/carver_type',
    'worldgen/chunk_generator',
    'worldgen/decorator', # Removed
    'worldgen/density_function_type',
    'worldgen/feature', # Removed as registry
    'worldgen/feature_size_type',
    'worldgen/feature_type',
    'worldgen/foliage_placer_type',
    'worldgen/material_condition', # Removed as registry
    'worldgen/material_condition_type',
    'worldgen/material_rule', # Removed as registry
    'worldgen/material_rule_type',
    'worldgen/placement_modifier_type',
    'worldgen/pool_alias_binding',
    'worldgen/root_placer_type',
    'worldgen/structure_feature', # Removed
    'worldgen/structure_piece',
    'worldgen/structure_placement',
    'worldgen/structure_pool_element',
    'worldgen/structure_processor',
    'worldgen/structure_type',
    'worldgen/surface_builder', # Removed
    'worldgen/tree_decorator_type',
    'worldgen/trunk_placer_type',
)

NormalFileCategories = (
    'advancement',
    'banner_pattern',
    'block_transformer',
    'cat_sound_variant',
    'cat_variant',
    'chat_type',
    'chicken_sound_variant',
    'chicken_variant',
    'context_float_provider',
    'context_int_provider',
    'cow_sound_variant',
    'cow_variant',
    'damage_type',
    'decorated_pot_pattern',
    'dialog',
    'dimension',
    'dimension_type',
    'enchantment',
    'enchantment_provider',
    'frog_variant',
    'function',
    'instrument',
    'item_modifier',
    'jukebox_song',
    'loot_table',
    'painting_variant',
    'pig_sound_variant',
    'pig_variant',
    'predicate',
    'recipe',
    'slot_source',
    'structure',
    'sulfur_cube_archetype',
    'test_environment',
    'test_instance',
    'timeline',
    'trade_set',
    'trial_spawner',
    'trim_material',
    'trim_pattern',
    'villager_trade',
    'wolf_sound_variant',
    'wolf_variant',
    'world_clock',
    'zombie_nautilus_variant',
)

WorldgenFileCategories = (
    'worldgen/biome',
    'worldgen/block_state_provider',
    'worldgen/carver',
    'worldgen/configured_carver', # Removed
    'worldgen/configured_feature', # Removed
    'worldgen/configured_structure_feature', # Removed
    'worldgen/configured_surface_builder', # Removed
    'worldgen/density_function',
    'worldgen/feature',
    'worldgen/flat_level_generator_preset',
    'worldgen/material_condition',
    'worldgen/material_rule',
    'worldgen/multi_noise_biome_source_parameter_list',
    'worldgen/noise',
    'worldgen/noise_settings',
    'worldgen/placed_feature',
    'worldgen/processor_list',
    'worldgen/structure',
    'worldgen/structure_set',
    'worldgen/template_pool',
    'worldgen/world_preset',
)

TaggableResourceLocationCategories = (*NormalFileCategories, *RegistryCategories, *WorldgenFileCategories)

TagFileCategories = tuple(f'tag/{key}' for key in TaggableResourceLocationCategories)

DataFileCategories = (*NormalFileCategories, *TagFileCategories, *WorldgenFileCategories)

DataMiscCategories = (
    'attribute_modifier',
	'bossbar',
	'jigsaw_block_name',
	'random_sequence',
	'storage',
	'stopwatch',
)

DatapackCategories = (
    'attribute_modifier_uuid',
	'objective',
	'player_uuid',
	'score_holder',
	'tag',
	'team',
    *DataFileCategories,
    *DataMiscCategories,
)

AssetsFileCategories = (
    'atlas',
    'block_definition', # blockstates
    'equipment',
    'font',
    'font/ttf',
    'font/otf',
    'font/unihex',
    'gpu_warnlist',
    'item_definition', # items
    'lang',
    'lang/deprecated',
    'model',
    'particle',
    'post_effect',
    'regional_compliancies',
    'shader',
    'shader/fragment',
    'shader/vertex',
    'sound',
    'sounds', # sounds.json
    'texture',
    'texture_meta', # *.png.mcmeta
    'waypoint_style',
)

AssetsMiscCategories = (
    'texture_slot',
	'shader_target',
	'translation_key',
)

ResourcepackCategories = (
    *AssetsMiscCategories,
    *AssetsFileCategories,
)

FileCategories = (*DataFileCategories, *AssetsFileCategories)

AllCategories = (
    *DatapackCategories,
    *ResourcepackCategories,
    *McdocCategories,
    *RegistryCategories
)

# == @spyglassmc/core/src/common/utils.ts > ResourceLocation#lengthen

NamespacePathSep = ':'

DefaultNamespace = 'minecraft'

def lengthen_resource_location(value: str) -> str:
    try:
        namespace_path_sep_index = value.index(NamespacePathSep)
        match namespace_path_sep_index:
            case 0:
                return f'{DefaultNamespace}{value}'
            case _:
                return value
    except ValueError:
        return f'{DefaultNamespace}{NamespacePathSep}{value}'