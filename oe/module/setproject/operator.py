import oe.tools as tools

from oe.refer import Registry as reg_


def op_initialize_project_dir(context):
    tools.Logging.operator_logger().info("Initializing project directory")

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


def op_browser_project_dir(context):
    tools.Logging.operator_logger().info("Browsing project directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_PROJ_DIR, ""
    )
    _target_dir = tools.Registry.set_value(
        reg_.REG_KEY,
        reg_.REG_SUB,
        reg_.REG_PROJ_DIR,
        tools.Maya.browser(3, _default_dir),
    )
    context["txt_proj_dir"].lineedit.setText(_target_dir)
    context["txt_proj_dir"].lineedit.setCursorPosition(0)


def op_initialize_resources_source_dir(context):
    tools.Logging.operator_logger().info("Initializing resources source directory")

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


def op_browser_resources_source_dir(context):
    tools.Logging.operator_logger().info("Browsing resources source directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_RES_SRC_DIR, ""
    )
    _target_dir = tools.Registry.set_value(
        reg_.REG_KEY,
        reg_.REG_SUB,
        reg_.REG_RES_SRC_DIR,
        tools.Maya.browser(3, _default_dir),
    )
    context["txt_res_src_dir"].lineedit.setText(_target_dir)
    context["txt_res_src_dir"].lineedit.setCursorPosition(0)


def op_initialize_resources_target_dir(context):
    tools.Logging.operator_logger().info("Initializing resources target directory")

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


def op_browser_resources_target_dir(context):
    tools.Logging.operator_logger().info("Browsing resources source directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_RES_TAR_DIR, ""
    )
    _target_dir = tools.Registry.set_value(
        reg_.REG_KEY,
        reg_.REG_SUB,
        reg_.REG_RES_TAR_DIR,
        tools.Maya.browser(3, _default_dir),
    )
    context["txt_res_tar_dir"].lineedit.setText(_target_dir)
    context["txt_res_tar_dir"].lineedit.setCursorPosition(0)
