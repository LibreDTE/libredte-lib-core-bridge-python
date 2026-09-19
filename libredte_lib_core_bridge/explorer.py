"""Bridge Python para explorar el árbol de paquetes de `libredte-lib-core`."""

from __future__ import annotations

from derafu_backbone_bridge import ExceptionRegistry, GenericExplorer


class Explorer(GenericExplorer):
    """
    Pre-cableado para explorar `libredte-lib-core` con su propio Explorer.

    El propio `Bootstrap::bootExplorer()` (método estático) de
    `libredte-lib-core-dispatcher` ya cablea todo lo necesario — el mismo
    `PackageRegistryInterface`/`InspectorInterface` que ya usa
    `Dispatcher` — de forma declarativa, en el `config/services.yaml` de
    ese paquete.

    A diferencia de `Dispatcher`, no registra ningún namespace de dominio
    propio: explorar el árbol nunca invoca una operación real, así que
    nunca puede surgir una excepción de `libredte-lib-core` (o de las
    bibliotecas Derafu que sus Deserializer envuelven) — solo las de
    `derafu/backbone`/`derafu/backbone-dispatcher`, que
    `ExceptionRegistry` ya cubre por default.
    """

    # Leído vía `self._BOOTSTRAP_CLASS` (no `Explorer._BOOTSTRAP_CLASS`) a
    # propósito: una subclase lo extiende reasignando este mismo nombre de
    # atributo, sin tocar `__init__` (ver `Dispatcher._BOOTSTRAP_CLASS`).
    _BOOTSTRAP_CLASS = 'libredte\\lib\\CoreDispatcher\\Bootstrap'

    def __init__(
        self,
        environment: str = 'prod',
        debug: bool = False,
        autoload_path: str | None = None,
        exception_registry: ExceptionRegistry | None = None,
    ) -> None:
        """Levanta el explorador de `libredte-lib-core` para `environment`."""
        super().__init__(
            self._BOOTSTRAP_CLASS,
            bootstrap_method='bootExplorer',
            bootstrap_args=(environment, debug),
            exception_registry=exception_registry,
            autoload_path=autoload_path,
        )
