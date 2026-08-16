"""Bridge Python para la biblioteca real `libredte-lib-core`."""

from __future__ import annotations

from derafu_backbone_bridge import ExceptionRegistry, GenericDispatcher

from .exceptions import LibredteLibCoreError


class Dispatcher(GenericDispatcher):
    """
    Pre-cableado para levantar `libredte-lib-core` con su propio dispatcher.

    El propio `Bootstrap::boot()` (método estático) de
    `libredte-lib-core-dispatcher` ya cablea todo lo necesario —cada
    Deserializer y la cadena completa de `derafu/backbone-dispatcher`— de
    forma declarativa, en el `config/services.yaml` de ese paquete.

    Expone muchos paquetes/componentes/workers, así que acá solo se fija
    el paso de arranque: quien lo use sigue indicando paquete, componente,
    worker y operación a través del `dispatch()` heredado.
    """

    _BOOTSTRAP_CLASS = 'libredte\\lib\\CoreDispatcher\\Bootstrap'

    # Namespaces de PHP cuyas excepciones se agrupan bajo
    # `LibredteLibCoreError` — no solo las propias de `libredte-lib-core`,
    # también las de las bibliotecas Derafu que sus Deserializer envuelven
    # directamente sin atraparlas (ver docstring de `LibredteLibCoreError`).
    _DOMAIN_NAMESPACES = (
        'libredte\\lib\\Core\\',
        'Derafu\\Xml\\',
        'Derafu\\Certificate\\',
    )

    def __init__(
        self,
        environment: str = 'prod',
        debug: bool = False,
        autoload_path: str | None = None,
        exception_registry: ExceptionRegistry | None = None,
    ) -> None:
        """
        Levanta `libredte-lib-core` para `environment`, con/sin `debug`.

        `exception_registry` es opcional: si no se pasa, se crea uno
        nuevo. En cualquier caso, acá se registran los namespaces de
        `_DOMAIN_NAMESPACES` hacia `LibredteLibCoreError` sobre esa
        instancia antes de pasarla al dispatcher real — permite que un
        bridge que herede de este pase su propio `exception_registry` ya
        con namespaces adicionales registrados, sin perderlos.
        """
        registry = exception_registry or ExceptionRegistry()
        for namespace in self._DOMAIN_NAMESPACES:
            registry.register(namespace, LibredteLibCoreError)

        super().__init__(
            self._BOOTSTRAP_CLASS,
            bootstrap_args=(environment, debug),
            exception_registry=registry,
            autoload_path=autoload_path,
        )
