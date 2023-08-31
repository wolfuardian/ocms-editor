def refresh():
    SetProjectData.is_loaded = False


class SetProjectData:
    widget = None
    props = {}
    is_loaded = False

    @classmethod
    def initiate(cls, widget):
        cls.widget = widget
        cls.load()

    @classmethod
    def load(cls):
        cls.props = {
            "str.filter.select.material.name": cls.get_str_filter_select_material_name(),
            "str.filter.material.name": cls.get_str_filter_material_name(),
            "bool.material.name": cls.get_bool_material_name(),
            "bool.material.attribute.color": cls.get_bool_material_attribute_color(),
            "bool.material.attribute.ambientColor": cls.get_bool_material_attribute_ambient_color(),
            "bool.material.attribute.cosinePower": cls.get_bool_material_attribute_cosine_power(),
        }
        cls.is_loaded = True

    @classmethod
    def get_str_filter_select_material_name(cls) -> str:
        return cls.widget.txl_filter_sel_mat_nm.lineedit.text()

    @classmethod
    def get_str_filter_material_name(cls) -> str:
        return cls.widget.txl_batch_merge_filter_mat_nm.lineedit.text()

    @classmethod
    def get_bool_material_name(cls) -> bool:
        return cls.widget.chk_batch_merge_filter_mat_nm.checkbox.isChecked()

    @classmethod
    def get_bool_material_attribute_color(cls) -> bool:
        return cls.widget.chk_batch_merge_filter_mat_at_clr.checkbox.isChecked()

    @classmethod
    def get_bool_material_attribute_ambient_color(cls) -> bool:
        return cls.widget.chk_batch_merge_filter_mat_at_amb_clr.checkbox.isChecked()

    @classmethod
    def get_bool_material_attribute_cosine_power(cls) -> bool:
        return cls.widget.chk_batch_merge_filter_mat_at_cos_pow.checkbox.isChecked()
