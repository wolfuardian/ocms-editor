class XMLData:
    props = {}

    path = None
    xmlstring = None
    root = None

    nodes_objects = None
    nodes_datasource = None

    data_objects = None
    data_datasource = None

    tags = None
    attrs = None
    types = None

    non_device_types = None

    @classmethod
    def purse(cls):
        cls.props = {}

        cls.path = None
        cls.xmlstring = None
        cls.root = None

        cls.nodes_objects = None
        cls.nodes_datasource = None

        cls.data_objects = None
        cls.data_datasource = None

        cls.tags = None
        cls.attrs = None
        cls.types = None

        cls.non_device_types = None

    @classmethod
    def update(cls, store):
        cls.props = store.props

        cls.path = store.path
        cls.xmlstring = store.xmlstring
        cls.root = store.root

        cls.nodes_objects = store.nodes_objects
        cls.nodes_datasource = store.nodes_datasource

        cls.data_objects = store.data_objects
        cls.data_datasource = store.data_datasource

        cls.tags = store.tags
        cls.attrs = store.attrs
        cls.types = store.types

        cls.non_device_types = store.non_device_types

class UIData:
    ui = {}