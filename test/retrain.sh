
# Train learning set (cv 1,2,3,4)
python3 trainAll.py learn_0

# Test out-of-sample
python3 testAll.py test_0 retrain_stats.txt test_0.pred.txt

# Test in-sample
python3 testAll.py learn_0 retrain_stats.txt learn_0.pred.txt
