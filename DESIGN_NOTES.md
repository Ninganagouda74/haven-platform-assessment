# Design Notes

## B2 — idempotency key

State exactly what key your `cost_tag_check.py` uses to decide a plan has already been
checked/reported on. Use the word "idempotency" in your explanation.

<!-- Your answer here -->
Idempotency:
    The check gives the same result every time it runs on the same plan the idempotency key is the resources address for example aws_s3_bucket.listing_media and aws_lambda_function.mls_feed_sync results are sorted by this address and have no timestamps so two runs print exactly the same output i proved this by running it twice and comaparing the results with diff
## Any other decision with a non-obvious alternative

<!-- Your answer here -->
Decisions:
1. I check landlord_account_id not tanant_id the README says landlord_account_id is the billing unit
2. the access check says no if anything is missing so a private report is never shown by mistake
3. I check both tags and tags_all because default tags only apper in tags_all 

python3 scripts/cost_tag_check.py > run1.txt
python3 scripts/cost_tag_check.py > run2.txt
diff run1.txt run2.txt & echo IDENTICAL


exit codes: run1=1 run2=1
IDENTICAL