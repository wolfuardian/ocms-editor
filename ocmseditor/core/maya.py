def browser(ocms, tool, reg_key, file_mode, file_filter="All Files (*.*)"):
    default_dir = ocms.RegistryStore(reg_key).get()

    browser_path = tool.Maya.browser(
        file_mode=file_mode, default_dir=default_dir, file_filter=file_filter
    )
    if browser_path == "":
        tool.Log.warning(__name__, "User canceled the browser dialog.")
        return default_dir

    return ocms.RegistryStore(reg_key).set(browser_path)
