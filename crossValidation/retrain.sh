# Train all learning sets
python3 trainAll.py learn_1
python3 trainAll.py learn_2
python3 trainAll.py learn_3
python3 trainAll.py learn_4

# Test out-of-sample
python3 testAll.py test_1 retrain_stats.txt test_1.pred.txt
python3 testAll.py test_2 retrain_stats.txt test_2.pred.txt
python3 testAll.py test_3 retrain_stats.txt test_3.pred.txt
python3 testAll.py test_4 retrain_stats.txt test_4.pred.txt

# Test in-sample
python3 testAll.py learn_1 retrain_stats.txt learn_1.pred.txt
python3 testAll.py learn_2 retrain_stats.txt learn_2.pred.txt
python3 testAll.py learn_3 retrain_stats.txt learn_3.pred.txt
python3 testAll.py learn_4 retrain_stats.txt learn_4.pred.txt