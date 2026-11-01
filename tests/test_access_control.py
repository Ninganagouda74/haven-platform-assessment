"""
Write tests here proving:
  1. A PropertyManager scoped to la-001 (pm-001) is DENIED access to la-002's tenant's
     screening report (rep-002).
  2. The same PropertyManager (pm-001) IS allowed access to their own account's screening
     report (rep-001).

Use the `property_managers`, `properties`, `tenants`, and `screening_reports` fixtures from
conftest.py — don't re-invent the seed data here.
"""
from app.access_control import can_access_screening_report


def test_manager_can_access_screening_report_for_tenant_under_own_account(
    property_managers, properties, tenants, screening_reports
):
    assert can_access_screening_report(
        property_managers[0],
        screening_reports[0],
        properties=properties,
        tenants=tenants,
    )


def test_manager_cannot_access_screening_report_for_tenant_under_another_account(
    property_managers, properties, tenants, screening_reports
):
    assert not can_access_screening_report(
        property_managers[0],
        screening_reports[1],
        properties=properties,
        tenants=tenants,
    )


def test_access_is_denied_when_report_tenant_is_missing(
    property_managers, properties, screening_reports
):
    assert not can_access_screening_report(
        property_managers[0],
        screening_reports[0],
        properties=properties,
        tenants=[],
    )


def test_access_is_denied_when_tenant_property_is_missing(
    property_managers, tenants, screening_reports
):
    assert not can_access_screening_report(
        property_managers[0],
        screening_reports[0],
        properties=[],
        tenants=tenants,
    )
