from . import store


def set_prop_s_filter_sel_mat_nm(s):
    store.SetProjectData.props["str.filter.select.material.name"] = s


def set_prop_s_filter_mat_nm(s):
    store.SetProjectData.props["str.filter.material.name"] = s


def set_prop_b_mat_nm(b):
    store.SetProjectData.props["bool.material.name"] = b


def set_prop_b_mat_at_clr(b):
    store.SetProjectData.props["bool.material.attribute.color"] = b


def set_prop_b_mat_at_amb_clr(b):
    store.SetProjectData.props["bool.material.attribute.ambientColor"] = b


def set_prop_b_mat_at_cos_pow(b):
    store.SetProjectData.props["bool.material.attribute.cosinePower"] = b


def get_prop_b_mat_nm():
    return store.SetProjectData.props.get("bool.material.name")
