"""
B2, part 2 — implement the cost-tagging check.

Read fixtures/plan.json for the shape of a `terraform show -json` plan: a `resource_changes`
list, where each entry has a `type`, an `address`, and `change.after.tags`.

Implement check_plan() so it:
  - Looks at every resource being created or changed (skip anything not in
    change.actions, e.g. a pure "no-op" / "read" change).
  - Fails (returns a non-zero exit code) if the resource is missing the tag that identifies
    the real billing unit, per README.md's domain model — not whatever tag the resource
    happens to already carry.
  - Is idempotent: running this twice against the same plan file produces the same result,
    with no duplicate output and no flipped pass/fail.
  - Prints which specific resource address(es) are missing the tag.

Run manually: python scripts/cost_tag_check.py fixtures/plan.json
"""
import json
import sys


def check_plan(plan_path: str) -> int:
    """
    Returns an exit code: 0 if every taggable resource being created/changed has
    `landlord_account_id`, non-zero otherwise.
    """
    with open(plan_path, encoding="utf-8") as plan_file:
        plan = json.load(plan_file)

    missing_tags = []
    for resource in plan["resource_changes"]:
        change = resource["change"]
        actions = change["actions"]
        if not any(action in ("create", "update") for action in actions):
            continue

        after = change.get("after") or {}
        if any(
            "landlord_account_id" in (after.get(tag_set) or {})
            for tag_set in ("tags", "tags_all")
        ):
            continue

        missing_tags.append(resource["address"])

    for address in sorted(missing_tags):
        print(f"Missing landlord_account_id tag: {address}")

    return 1 if missing_tags else 0


if __name__ == "__main__":
    sys.exit(check_plan(sys.argv[1]))
