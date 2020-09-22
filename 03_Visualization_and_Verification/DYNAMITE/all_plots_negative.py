import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_context("notebook")

# H3K4me3
l1_p6 = pd.read_table('/home/kevin/tmp/DYNAMITE/L1_vs_p6/H3K4me3/Learning_Results/Regression_Coefficients_Entire_Data_Set_Integrated_Data_For_Classification.txt').sort_values(['value'], ascending=True)
l1_p13 = pd.read_table('/home/kevin/tmp/DYNAMITE/L1_vs_p13/H3K4me3/Learning_Results/Regression_Coefficients_Entire_Data_Set_Integrated_Data_For_Classification.txt').sort_values(['value'], ascending=True)
lactation_pregnancy = pd.read_table('/home/kevin/tmp/DYNAMITE/Lactation_vs_Pregnancy/H3K4me3/Learning_Results/Regression_Coefficients_Entire_Data_Set_Integrated_Data_For_Classification.txt').sort_values(['value'], ascending=True)

# Remove suffix
l1_p6['TF'] = l1_p6['TF'].str.split('_', expand=True)[0]
l1_p13['TF'] = l1_p13['TF'].str.split('_', expand=True)[0]
lactation_pregnancy['TF'] = lactation_pregnancy['TF'].str.split('_', expand=True)[0]
print(l1_p6)

# Sort and filter
l1_p6 = l1_p6[l1_p6['value'] < -0.1].set_index('TF')
l1_p6.columns = ['L1 vs p6']
l1_p13 = l1_p13[l1_p13['value'] < -0.1].set_index('TF')
l1_p13.columns = ['L1 vs p13']
lactation_pregnancy = lactation_pregnancy[lactation_pregnancy['value'] <- 0.1].set_index('TF')
lactation_pregnancy.columns = ['L vs P']

color = "#A6CEE3"

# Bar Plots
time = 'L1 vs p6'
ax = sns.barplot(x= l1_p6.index, y=time, data=l1_p6, color=color)
ax.set_title(time)
ax.set_ylabel('Normalized feature value')
ax.set_xlabel('')
plt.xticks(rotation=60)
plt.tight_layout()
plt.savefig(f"H3K4me3_{time}.pdf")

time = 'L1 vs p13'
ax = sns.barplot(x= l1_p13.index, y=time, data=l1_p13, color=color)
ax.set_title(time)
ax.set_ylabel('Normalized feature value')
ax.set_xlabel('')
ax.set_xticklabels(ax.get_xticklabels(), fontsize=10, rotation=60)
plt.tight_layout()
plt.savefig(f"H3K4me3_{time}.pdf")

time = 'L vs P'
ax = sns.barplot(x= lactation_pregnancy.index, y=time, data=lactation_pregnancy, color=color)
ax.set_title('Lactation vs Pregnancy')
ax.set_ylabel('Normalized feature value')
ax.set_xlabel('')
ax.set_xticklabels(ax.get_xticklabels(), fontsize=10, rotation=60)
plt.tight_layout()
plt.savefig(f"H3K4me3_{time}.pdf")

# Heatmap
join_df = pd.concat([l1_p6, l1_p13, lactation_pregnancy], axis=1)
plt.figure(figsize = (10,3))
plot = sns.heatmap(join_df.transpose(), cmap="Paired",  square=True, vmin=1, vmax=1, cbar=False, linewidths=0.5, linecolor='black', xticklabels=True)
plt.savefig("H3K4me3_heatmap.pdf")
