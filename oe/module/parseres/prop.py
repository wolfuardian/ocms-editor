from . import store


def set_prop_models_names_mapping_by_type(models):
    store.ParseResourcesData.props["models_names_mapping_by_type"] = models


def set_prop_models_paths_mapping_by_type(models):
    store.ParseResourcesData.props["models_paths_mapping_by_type"] = models
