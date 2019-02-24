from .base import *

DEBUG = False
SECRET_KEY = '^7nk)wiwyd3fq0i%xs7xj&vm&f@=4qu)4ow@t60gw)0h#*jv^o'

try:
    from .local import *
except ImportError:
    pass
