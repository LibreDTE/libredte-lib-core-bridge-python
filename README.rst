LibreDTE: Bridge Python para la Biblioteca PHP (Core)
======================================================

Bridge que expone, desde Python, las operaciones de
`libredte/libredte-lib-core`, a través de `libredte-lib-core-dispatcher`,
usando `derafu-backbone-bridge` como base.

Uso
---

.. code-block:: python

    from libredte_lib_core_bridge import Dispatcher

    dispatcher = Dispatcher()  # environment='prod', debug=False por defecto

    caf = dispatcher.dispatch(
        'billing.identifier.caf_loader:load',
        xml=xml_base64,
    )

``dispatch()`` nunca deja pasar un error de PHP sin tipar: lanza una excepción
Python (``derafu_backbone_bridge.BackboneBridgeError`` o una de sus
subclases) en vez de una excepción PHP cruda.

Arquitectura
------------

- ``Dispatcher`` es una subclase de
  ``derafu_backbone_bridge.GenericDispatcher``, pre-cableada con el
  ``Bootstrap::boot()`` de ``libredte-lib-core-dispatcher``.
- No sabe dónde vive el código PHP en disco: eso se resuelve vía la variable
  de entorno ``BACKBONE_DISPATCHER_AUTOLOAD`` (o pasando ``autoload_path``
  explícito al construir ``Dispatcher``).
- No importa ``phpy`` en ningún punto: todo el manejo de ``phpy`` vive dentro
  de ``derafu-backbone-bridge``.

Desarrollo
----------

.. code-block:: bash

    make install-dev
    make check   # ruff + tests

Los tests requieren ``phpy`` (solo disponible dentro del contenedor
``docker-python3.14-caddy-server`` construido con ``PHPY_ENABLED=true``) y
una instalación real de ``libredte-lib-core-dispatcher`` (con sus propias
dependencias de Composer) accesible en disco. No usan ningún fixture
externo: generan un CAF real y válido en memoria vía el propio
``caf_faker:create`` de ``libredte-lib-core``.

Términos y condiciones de uso
------------------------------

Este proyecto es software libre y puede ser redistribuido y/o modificado
bajo los términos de la Licencia Pública General Affero de GNU (AGPL),
versión 3 o (a elección) cualquier versión posterior. Ver
`COPYING <COPYING>`_.
