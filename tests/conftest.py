"""
Fixtures de pytest compartidas.

Levanta la cadena real de `libredte-lib-core-dispatcher`. Requiere `phpy`
(solo disponible dentro del contenedor `docker-python3.14-caddy-server`
construido con `PHPY_ENABLED=true`) y un checkout real, instalado vía
Composer, de `libredte-lib-core-dispatcher` como directorio hermano — los
tests de este paquete no traen ningún fixture propio, corren contra la
biblioteca real.
"""

import os

import pytest

from libredte_lib_core_bridge import Dispatcher, Explorer

_AUTOLOAD_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    '..',
    'libredte-lib-core-dispatcher',
    'vendor',
    'autoload.php',
)


@pytest.fixture
def autoload_path():
    """Expone la ruta de autoload del hermano `core-dispatcher`."""
    return _AUTOLOAD_PATH


@pytest.fixture
def dispatcher(autoload_path):
    """Construye un `Dispatcher` nuevo contra el checkout real hermano."""
    return Dispatcher(autoload_path=autoload_path)


@pytest.fixture
def explorer(autoload_path):
    """Construye un `Explorer` nuevo contra el checkout real hermano."""
    return Explorer(autoload_path=autoload_path)
