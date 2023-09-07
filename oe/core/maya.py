def browser(storage, tools, directory, mode):
    _default = storage.Registry(directory).get()

    _browser = tools.Maya.browser(mode, _default)
    if _browser == "":
        tools.Log.warning(__name__, "User canceled the browser dialog.")
        return _default

    return storage.Registry(directory).set(_browser)
