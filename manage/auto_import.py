# coding: utf-8
import import_string
from six import exec_


def get_name(obj, default):
    default = default.split('.')[0]
    return getattr(obj, '__name__', default)


def import_objects(manage_dict):
    auto_import = {}
    auto_scripts = []
    import_dict = manage_dict.get('shell', {}).get('auto_import', {})
    object_list = import_dict.get('objects', [])
    if isinstance(object_list, dict):
        for name, spec in object_list.items():
            _obj = import_string(name)
            if spec:
                if 'init' in spec:
                    method_name = spec['init'].keys()[0]
                    args = spec['init'].get(method_name, {}).get('args', [])
                    kwargs = spec['init'].get(
                        method_name, {}).get('kwargs', {})
                    getattr(_obj, method_name)(*args, **kwargs)
                auto_import[spec.get('as', get_name(_obj, name))] = _obj
                if 'init_script' in spec:
                    auto_scripts.append(spec['init_script'])
            else:
                auto_import[get_name(_obj, name)] = _obj
    else:
        for name in object_list:
            _obj = import_string(name)
            auto_import[getattr(_obj, '__name__', name)] = _obj
    for script in auto_scripts:
        exec_(script, auto_import)
    return auto_import


def exec_init(manage_dict, context):
    for name, spec in manage_dict['shell'].get('init', {}).items():
        _obj = context.get(name, import_string(name))
        args = spec.get('args', []) if spec else []
        kwargs = spec.get('kwargs', {}) if spec else {}
        _obj(*args, **kwargs)


def exec_init_script(manage_dict, context):
    if 'init_script' in manage_dict['shell']:
        exec_(manage_dict['shell']['init_script'], context)
