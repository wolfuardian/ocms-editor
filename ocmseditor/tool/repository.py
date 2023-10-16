from ocmseditor.oe.repository import RepositoryFacade

import ocmseditor.core.tool as core


class Repository(core.Repository):
    @classmethod
    def get(cls):
        return RepositoryFacade()

