# coding: utf-8
import pkgutil
import sys
from importlib import import_module


def get_name(obj, default):
    default = default.split(".")[0]
    return getattr(obj, "__name__", default)


def import_submodules(name, submodules=None):
    """Import all submodules for a package/module name"""
    sys.path.insert(0, name)
    if submodules:
        for submodule in submodules:
            import_module("{0}.{1}".format(name, submodule))
    else:
        for item in pkgutil.walk_packages([name]):
            import_module("{0}.{1}".format(name, item[1]))


def import_objects(manage_dict):
    auto_import = {}
    auto_scripts = []
    import_dict = manage_dict.get("shell", {}).get("auto_import", {})
    object_list = import_dict.get("objects", [])
    if isinstance(object_list, dict):
        for name, spec in object_list.items():
            _obj = import_module(name)
            if spec:
                if "init" in spec:
                    init = spec["init"]
                    if isinstance(init, dict):
                        method_name = init.keys()[0]
                        args = (init[method_name] or {}).get("args", [])
                        kwargs = (init[method_name] or {}).get("kwargs", {})
                    else:
                        method_name = init
                        args = []
                        kwargs = {}
                    getattr(_obj, method_name)(*args, **kwargs)
                spec_as = spec.get("as", get_name(_obj, name))
                if not isinstance(spec_as, list):
                    spec_as = [spec_as]
                for as_name in spec_as:
                    auto_import[as_name] = _obj

                if "init_script" in spec:
                    auto_scripts.append(spec["init_script"])
                if "submodules" in spec:
                    submodules = spec["submodules"]
                    if isinstance(submodules, list):
                        import_submodules(name, submodules)
                    else:
                        import_submodules(name)
            else:
                auto_import[get_name(_obj, name)] = _obj
    else:
        for name in object_list:
            _obj = import_module(name)
            auto_import[getattr(_obj, "__name__", name)] = _obj
    for script in auto_scripts:
        exec(script, auto_import)
    return auto_import


def exec_init(manage_dict, context):
    for name, spec in manage_dict["shell"].get("init", {}).items():
        _obj = context.get(name, import_module(name))
        args = spec.get("args", []) if spec else []
        kwargs = spec.get("kwargs", {}) if spec else {}
        _obj(*args, **kwargs)


def exec_init_script(manage_dict, context):
    if "init_script" in manage_dict["shell"]:
        exec(manage_dict["shell"]["init_script"], context)
