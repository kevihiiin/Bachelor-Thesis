from pathlib import Path

from matplotlib_venn import venn2, venn2_circles
from matplotlib_venn import venn3, venn3_circles
from matplotlib import pyplot as plt
import pandas as pd

set_1_path = Path('/home/kevin/tmp/DYNAMITE/L1_vs_p13-H3K4me3.txt')
set_2_path = Path('/home/kevin/tmp/DYNAMITE/L1_vs_p6-H3K4me3.txt')

set_1 = pd.read_table(set_1_path).sort_values('value')[:10]
set_2 = pd.read_table(set_2_path).sort_values('value')[:10]

lst1 = set_1['TF']
lst2 = set_2['TF']

print("Union")
print(set(lst1).intersection(set(lst2)))

venn2([set(lst1), set(lst2)],
      set_labels = (set_1_path.name, set_2_path.name))
plt.title('Comparison of Time Points\n')
plt.show()