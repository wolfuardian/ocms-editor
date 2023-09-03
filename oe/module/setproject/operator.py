import oe.tools as tools

from oe.refer import Registry as reg_


def op_initialize_project_dir(context):
    tools.Logging.parser_xml_logger().info("Initializing project directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_PROJ_DIR, ""
    )
    if _default_dir == "":
        _target_dir = tools.Registry.set_value(
            reg_.REG_KEY,
            reg_.REG_SUB,
            reg_.REG_PROJ_DIR,
            tools.Maya.browser(3, _default_dir),
        )
        context["txt_proj_dir"].lineedit.setText(_target_dir)
    else:
        context["txt_proj_dir"].lineedit.setText(_default_dir)
    context["btn_init_proj_dir"].set_force_visible(False)
    context["txt_proj_dir"].set_force_visible(True)
    context["txt_proj_dir"].lineedit.setCursorPosition(0)
    context["ui_btn_browser_proj_dir"].set_force_visible(True)
    tools.Logging.parser_xml_logger().info("Completed initializing project directory")


def op_browser_project_dir(context):
    tools.Logging.parser_xml_logger().info("Browsing project directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_PROJ_DIR, ""
    )
    _browser_dir = tools.Maya.browser(3, _default_dir)
    if _browser_dir == "":
        tools.Logging.parser_xml_logger().warning("User canceled the browser dialog.")
        return
    _target_dir = tools.Registry.set_value(
        reg_.REG_KEY,
        reg_.REG_SUB,
        reg_.REG_PROJ_DIR,
        _browser_dir,
    )
    context["txt_proj_dir"].lineedit.setText(_target_dir)
    context["txt_proj_dir"].lineedit.setCursorPosition(0)
    tools.Logging.parser_xml_logger().info("Completed browsing project directory")


def op_initialize_resources_source_dir(context):
    tools.Logging.parser_xml_logger().info("Initializing resources source directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_RES_SRC_DIR, ""
    )
    if _default_dir == "":
        _target_dir = tools.Registry.set_value(
            reg_.REG_KEY,
            reg_.REG_SUB,
            reg_.REG_RES_SRC_DIR,
            tools.Maya.browser(3, _default_dir),
        )
        context["txt_res_src_dir"].lineedit.setText(_target_dir)
    else:
        context["txt_res_src_dir"].lineedit.setText(_default_dir)
    context["btn_init_res_src_dir"].set_force_visible(False)
    context["txt_res_src_dir"].set_force_visible(True)
    context["txt_res_src_dir"].lineedit.setCursorPosition(0)
    context["ui_btn_browser_res_src_dir"].set_force_visible(True)
    tools.Logging.parser_xml_logger().info("Completed initializing resources source directory")

def op_browser_resources_source_dir(context):
    tools.Logging.parser_xml_logger().info("Browsing resources source directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_RES_SRC_DIR, ""
    )
    _browser_dir = tools.Maya.browser(3, _default_dir)
    if _browser_dir == "":
        tools.Logging.parser_xml_logger().warning("User canceled the browser dialog.")
        return
    _target_dir = tools.Registry.set_value(
        reg_.REG_KEY,
        reg_.REG_SUB,
        reg_.REG_RES_SRC_DIR,
        _browser_dir,
    )
    context["txt_res_src_dir"].lineedit.setText(_target_dir)
    context["txt_res_src_dir"].lineedit.setCursorPosition(0)
    tools.Logging.parser_xml_logger().info("Completed browsing resources source directory")

def op_initialize_resources_target_dir(context):
    tools.Logging.parser_xml_logger().info("Initializing resources target directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_RES_TAR_DIR, ""
    )
    if _default_dir == "":
        _target_dir = tools.Registry.set_value(
            reg_.REG_KEY,
            reg_.REG_SUB,
            reg_.REG_RES_TAR_DIR,
            tools.Maya.browser(3, _default_dir),
        )
        context["txt_res_tar_dir"].lineedit.setText(_target_dir)
    else:
        context["txt_res_tar_dir"].lineedit.setText(_default_dir)
    context["btn_init_res_tar_dir"].set_force_visible(False)
    context["txt_res_tar_dir"].set_force_visible(True)
    context["txt_res_tar_dir"].lineedit.setCursorPosition(0)
    context["ui_btn_browser_res_tar_dir"].set_force_visible(True)
    tools.Logging.parser_xml_logger().info("Completed initializing resources target directory")

def op_browser_resources_target_dir(context):
    tools.Logging.parser_xml_logger().info("Browsing resources source directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_RES_TAR_DIR, ""
    )
    _browser_dir = tools.Maya.browser(3, _default_dir)
    if _browser_dir == "":
        tools.Logging.parser_xml_logger().warning("User canceled the browser dialog.")
        return
    _target_dir = tools.Registry.set_value(
        reg_.REG_KEY,
        reg_.REG_SUB,
        reg_.REG_RES_TAR_DIR,
        _browser_dir,
    )
    context["txt_res_tar_dir"].lineedit.setText(_target_dir)
    context["txt_res_tar_dir"].lineedit.setCursorPosition(0)
    tools.Logging.parser_xml_logger().info("Completed browsing resources target directory")