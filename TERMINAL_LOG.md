


B2 
Task 1:  Test result: python -m pytest tests\test_access_control.py -q — 4 passed.

Task 2:
python3 scripts/cost_tag_check.py > run1.txt
python3 scripts/cost_tag_check.py > run2.txt
diff run1.txt run2.txt & echo IDENTICAL

    exit codes: run1=1 run2=1
    IDENTICAL