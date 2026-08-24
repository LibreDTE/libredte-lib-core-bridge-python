"""
Tests reales, de punta a punta, para `Dispatcher`.

Cada test despacha a través de la cadena real de
`libredte-lib-core-dispatcher` vía `phpy` — sin mocks en ningún punto.
"""

import pytest

from libredte_lib_core_bridge import Dispatcher, LibredteLibCoreError

_EMISOR_RUT = '76192083-9'
_TIPO_DOCUMENTO = 33
_FOLIO_DESDE = 1
_FOLIO_HASTA = 100


def test_dispatch_creates_and_loads_a_real_caf(dispatcher):
    """
    Genera un CAF real y lo carga de vuelta.

    `caf_faker::create` + `caf_loader::load` — sin ningún fixture externo,
    ya que `caf_faker` es un servicio real y público de
    `libredte-lib-core`.
    """
    fake_caf_result = dispatcher.dispatch(
        'billing.identifier.caf_faker::create',
        emisor={'rut': _EMISOR_RUT},
        codigoDocumento=_TIPO_DOCUMENTO,
        folioDesde=_FOLIO_DESDE,
        folioHasta=_FOLIO_HASTA,
    )
    fake_caf = fake_caf_result.value

    assert fake_caf_result.metadata.real_time >= 0.0
    assert fake_caf_result.metadata.pid > 0

    caf = dispatcher.dispatch(
        'billing.identifier.caf_loader::load',
        xml=fake_caf['xml'],
    ).value

    assert caf['tipoDocumento'] == _TIPO_DOCUMENTO
    assert caf['folioDesde'] == _FOLIO_DESDE
    assert caf['folioHasta'] == _FOLIO_HASTA


def test_dispatch_raises_libredte_lib_core_error_for_a_domain_failure(
    dispatcher,
):
    """
    Un rechazo real por regla de negocio se agrupa bajo `LibredteLibCoreError`.

    El `bag` no trae ningún tipo de documento (ni `TipoDTE` en datos ya
    parseados/normalizados, ni un XML o `document` del que derivarlo) —
    `DocumentBagManagerWorker::ensureTipoDocumento()` no tiene de dónde
    sacarlo y `libredte-lib-core` rechaza el `DocumentBag` con su propio
    `DocumentException` ("Falta indicar el tipo de documento (TipoDTE) en
    los datos del DTE") — no un mock, la validación real de la biblioteca.
    """
    fake_caf = dispatcher.dispatch(
        'billing.identifier.caf_faker::create',
        emisor={'rut': _EMISOR_RUT},
        codigoDocumento=_TIPO_DOCUMENTO,
        folioDesde=_FOLIO_DESDE,
        folioHasta=_FOLIO_HASTA,
    ).value

    with pytest.raises(LibredteLibCoreError) as exc_info:
        dispatcher.dispatch(
            'billing.document.dispatcher::create',
            bag={
                'caf': fake_caf['xml'],
                'emisor': {'rut': _EMISOR_RUT, 'razon_social': 'SASCO SpA'},
                'receptor': {
                    'rut': '66666666-6',
                    'razon_social': 'Cliente de prueba',
                },
            },
        )

    assert 'DocumentException' in exc_info.value.php_class
    assert exc_info.value.metadata.real_time >= 0.0


def test_default_constructor_falls_back_to_the_env_var(
    monkeypatch,
    autoload_path,
):
    """`Dispatcher()` sin argumentos funciona vía la env var."""
    monkeypatch.setenv('BACKBONE_DISPATCHER_AUTOLOAD', autoload_path)
    dispatcher = Dispatcher()

    fake_caf = dispatcher.dispatch(
        'billing.identifier.caf_faker::create',
        emisor={'rut': _EMISOR_RUT},
        codigoDocumento=_TIPO_DOCUMENTO,
        folioDesde=_FOLIO_DESDE,
        folioHasta=_FOLIO_HASTA,
    ).value

    assert fake_caf['tipoDocumento'] == _TIPO_DOCUMENTO
