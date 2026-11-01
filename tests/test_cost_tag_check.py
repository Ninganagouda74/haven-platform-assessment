"""
Write tests here proving:
  1. Happy path: running the check against fixtures/plan.json correctly flags the resources
     missing `landlord_account_id` (listing_media, mls_feed_sync) and passes the ones that
     have it (landlord_media[0], screening_report_export).
  2. Idempotency: running the check twice against the same plan file produces the same
     result both times, with no duplicated output.

Use a test double / your own in-memory plan dict where you don't need a real file on disk —
you don't need to shell out to the real script for every case.
"""
import json
from pathlib import Path

from scripts.cost_tag_check import check_plan


PLAN_PATH = Path(__file__).parents[1] / "fixtures" / "plan.json"


def test_fixture_plan_reports_missing_landlord_account_tags(capsys):
    results = [check_plan(str(PLAN_PATH)) for _ in range(2)]

    expected_output = (
        "Missing landlord_account_id tag: aws_lambda_function.mls_feed_sync\n"
        "Missing landlord_account_id tag: aws_s3_bucket.listing_media\n"
    )
    assert results == [1, 1]
    assert capsys.readouterr().out == expected_output * 2


def test_tags_all_is_accepted_and_deleted_resources_are_skipped(tmp_path, capsys):
    plan = {
        "resource_changes": [
            {
                "address": "aws_example.deleted",
                "change": {"actions": ["delete"], "after": None},
            },
            {
                "address": "aws_example.tagged",
                "change": {
                    "actions": ["create"],
                    "after": {"tags_all": {"landlord_account_id": "la-001"}},
                },
            },
            {
                "address": "aws_example.untagged",
                "change": {"actions": ["update"], "after": {"tags": {}}},
            },
        ]
    }
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    assert check_plan(str(plan_path)) == 1
    assert capsys.readouterr().out == "Missing landlord_account_id tag: aws_example.untagged\n"


def test_check_passes_when_all_changed_resources_have_required_tag(tmp_path, capsys):
    plan = {
        "resource_changes": [
            {
                "address": "aws_example.tagged",
                "change": {
                    "actions": ["update"],
                    "after": {"tags": {"landlord_account_id": "la-001"}},
                },
            }
        ]
    }
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    assert check_plan(str(plan_path)) == 0
    assert capsys.readouterr().out == ""
