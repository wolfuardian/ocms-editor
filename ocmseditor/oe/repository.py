class OCMSRepository:
    """
    Singleton (單例)
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCMSRepository, cls).__new__(cls)
            cls._instance.et = OCMSElementTree()
            cls._instance.rm = OCMSResourceModel()
            cls._instance.inf = OCMSInformation()
        return cls._instance


class OCMSElementTree:
    pass


class OCMSResourceModel:
    pass


class OCMSInformation:
    pass


class MayaSceneRepository:
    """
    Singleton (單例)
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MayaSceneRepository, cls).__new__(cls)
            cls._instance.ctx = MayaSceneContext()
        return cls._instance


class MayaSceneContext:
    pass
