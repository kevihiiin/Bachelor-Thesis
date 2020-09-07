import numpy as np
from sklearn.metrics import roc_auc_score

y_true = np.array([0, 0, 1, 1])
y_scores = np.array([1, 1, 0.35, 0.8])

result = roc_auc_score(y_true, y_scores)
print(result)