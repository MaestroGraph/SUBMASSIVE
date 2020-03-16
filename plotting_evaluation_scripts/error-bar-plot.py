# this script is for the plotting of the errorbar
# reference :
# https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.07-Error-Bars/
import  numpy as np
import matplotlib.pyplot as plt


results_20 = np.array([174, 179, 144, 157, 162])

results_30 = np.array([157, 149, 152, 154, 158])

results_40 = np.array([147, 142, 144, 142, 142])

results_50 = np.array([134, 145, 140, 142, 149])

results_60 = np.array([138, 142, 142, 142, 139])

# results_70 = np.array([179, 144, 157, 162, 157])



# -rw-rw-r-- 1 finn finn       25392 Feb 19 00:13 final_removed_edges_50:1_134_00:22:19.12.csv
# -rw-rw-r-- 1 finn finn       27965 Feb 19 00:35 final_removed_edges_50:2_145_00:22:11.35.csv
# -rw-rw-r-- 1 finn finn       26660 Feb 19 03:46 final_removed_edges_50:3_140_00:22:13.34.csv
# -rw-rw-r-- 1 finn finn       27013 Feb 19 10:29 final_removed_edges_50:4_142_00:22:12.99.csv
# -rw-rw-r-- 1 finn finn       28375 Feb 18 23:30 final_removed_edges_50:5_149_00:24:38.77.csv

# -rw-rw-r-- 1 finn finn       26234 Feb 19 04:31 final_removed_edges_60:1_138_00:29:34.14.csv
# -rw-rw-r-- 1 finn finn       27402 Feb 19 09:49 final_removed_edges_60:2_142_00:21:34.17.csv
# -rw-rw-r-- 1 finn finn       27201 Feb 19 11:50 final_removed_edges_60:3_142_00:21:08.42.csv
# -rw-rw-r-- 1 finn finn       27241 Feb 19 10:38 final_removed_edges_60:4_142_00:20:18.01.csv
# -rw-rw-r-- 1 finn finn       26416 Feb 19 11:01 final_removed_edges_60:5_139_00:23:07.76.csv

# -rw-rw-r-- 1 finn finn       27481 Feb 19 10:54 final_removed_edges_70:1_142_00:49:57.68.csv

# Calculate the average
mean_20 = np.mean(results_20)
mean_30 = np.mean(results_30)
mean_40 = np.mean(results_40)
mean_50 = np.mean(results_50)
mean_60 = np.mean(results_60)


# Calculate the standard deviation
std_20 = np.std(results_20)
std_30 = np.std(results_30)
std_40 = np.std(results_40)
std_50 = np.std(results_50)
std_60 = np.std(results_60)

# Define labels, positions, bar heights and error bar heights
labels = ['20', '30', '40', '50', '60']
x_pos = np.arange(len(labels))
CTEs = [mean_20, mean_30, mean_40, mean_50, mean_60]
error = [std_20, std_30, std_40,std_50,std_60]


fig, ax = plt.subplots()
ax.bar(x_pos, CTEs,
       yerr=error,
       align='center',
       alpha=0.5,
       ecolor='black',
       capsize=10)
ax.set_ylabel('Number of Removed Edges')
ax.set_xlabel('Soft Bound on Subgraph Size (N)')

ax.set_xticks(x_pos)
ax.set_xticklabels(labels)
# ax.set_title('Number of Removed Edges to Achieve Acyclic Knowledge Graph')
ax.yaxis.grid(True)
plt.ylim(120, 180)
# Save the figure and show
plt.tight_layout()
plt.savefig('bar_plot_with_error_bars.png')
plt.show()
