"""Excepción de dominio para `libredte-lib-core`."""

from derafu_backbone_bridge import BackboneBridgeError


class LibredteLibCoreError(BackboneBridgeError):
    r"""
    Cualquier error real de `libredte-lib-core`.

    También cubre `Derafu\Xml\Exception\*` y
    `Derafu\Certificate\Exception\*`: los Deserializer de
    `libredte-lib-core-dispatcher` que envuelven esos tipos (XML,
    certificados) no atrapan sus excepciones para volver a lanzarlas como
    algo propio de `libredte-lib-core` — se filtran tal cual.
    """
