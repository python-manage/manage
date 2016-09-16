# coding: utf-8

import IPython.core.error


def shutdown_hook(ipython):
    print('\nThis is an extension exit hook')
    raise IPython.core.error.TryNext


def load_ipython_extension(ipython):
    print('\nExtension is being loaded!')
    print(ipython)
    ipython.set_hook('shutdown_hook', shutdown_hook, _warn_deprecated=False)
