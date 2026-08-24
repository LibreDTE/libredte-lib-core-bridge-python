"""
Tests reales, de punta a punta, para `Explorer`.

Cada test explora el árbol real de `libredte-lib-core-dispatcher` vía
`phpy` — sin mocks en ningún punto.
"""

import pytest
from derafu_backbone_bridge import PackageNotFoundError


def test_get_packages_includes_the_real_billing_package(explorer):
    """El árbol real de paquetes incluye `billing`."""
    packages = explorer.get_packages()

    assert 'billing' in [p['id'] for p in packages]


def test_get_package_with_components_lists_identifier_and_document(
    explorer,
):
    """`billing` trae entre sus componentes `identifier`/`document`."""
    package = explorer.get_package('billing', with_components=True)

    component_ids = [c['id'] for c in package['components']]
    assert 'billing.identifier' in component_ids
    assert 'billing.document' in component_ids


def test_get_operation_returns_the_doc_of_a_real_operation(explorer):
    """`caf_faker::create` es una operación real, con su propio id."""
    operation = explorer.get_operation(
        'billing',
        'identifier',
        'caf_faker',
        'create',
    )

    assert operation['id'] == 'billing.identifier.caf_faker::create'


def test_tree_nests_operations_under_a_real_worker(explorer):
    """`tree()` sobre un worker real anida sus operaciones."""
    worker = explorer.tree('billing.identifier.caf_faker')

    names = [o['name'] for o in worker['operations']]
    assert 'create' in names


def test_get_components_raises_package_not_found_for_an_unknown_package(
    explorer,
):
    """Un paquete inexistente lanza `PackageNotFoundError`, no un crash."""
    with pytest.raises(PackageNotFoundError):
        explorer.get_components('unknown_package')
