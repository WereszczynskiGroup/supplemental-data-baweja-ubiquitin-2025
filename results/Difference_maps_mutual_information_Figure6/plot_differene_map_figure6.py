import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
freqMap = np.loadtxt(sys.argv[1])

#print freqMap[0:100, 0:100].shape

freqMap1 = np.loadtxt(sys.argv[2])


freq = freqMap1 - freqMap

print (freqMap.shape)

print (freqMap1.shape)


#np.fill_diagonal(freqMap, 0)

#freqMap[freqMap == 0] = 'nan'

cmap = mpl.cm.bwr

norm = mpl.colors.Normalize(vmin=-0.2, vmax=0.2)

#freqMap[0:, 45:90]

#ranges = [(0,135), (135, 237), (237, 365), (365, 441), (441, 566), (566, 701), (701, 803), (803, 930), (930, 1007),  (1007, 1132), (1132,1279), (1279,1426)]

#labels = ["H3", "H4", "H2A", "ub", "H2B", "H3", "H4", "H2A", "ub", "H2B", "DNA1", "DNA2"]

#label_positions = [(x + y) / 2 for x, y in ranges]

#tick_positions = list(set([item for sublist in ranges for item in sublist]))

#print (tick_positions)
#print (label_positions)
#tick_positions = [(range[0] + range[1]) / 2 for range in ranges]
#label_positions = [ranges[i][1] + ((ranges[i+1][0] - ranges[i][1]) / 2) for i in range(len(ranges)-1)]

ranges = [(0,135), (135, 237), (237, 365), (365, 490), (490, 625), (625, 727), (728, 855), (855, 980),  (980, 1127), (1128,1274)]

labels = ["H3", "H4", "H2A", "H2B", "H3", "H4", "H2A", "H2B", "DNA1", "DNA2"]

label_positions = [(x + y) / 2 for x, y in ranges]

tick_positions = list(set([item for sublist in ranges for item in sublist]))
fig,ax=plt.subplots(figsize=(8,6))
plt.imshow(freq,origin='lower',aspect='auto', cmap=cmap)
cb = plt.colorbar(norm=norm)
#ax.set_xlim(np.linspace(0, 1274, 20))
#ax.set_ylim(np.linspace(0, 1274, 20)
#plt.xticks([i for i in range(0, 140) if i%2 !=0])
#plt.yticks([i for i in range(0, 140) if i%2 !=0])

d = {
        'fontweight' : 'bold',
        'fontsize'   : 14}
ax.set_yticks(tick_positions, labels=None)
#ax.set_xticklabels(labels)
ax.set_yticklabels([])
# Set label positions
#ax.xaxis.set_tick_params(pad=10)  # Adjust padding if necessary
ax.set_yticks(label_positions, minor=True)
ax.set_yticklabels(labels, minor=True, **d)

ax.set_xticks(tick_positions, labels=None)
#ax.set_xticklabels(labels)
ax.set_xticklabels([])
# Set label positions
#ax.xaxis.set_tick_params(pad=10)  # Adjust padding if necessary
ax.set_xticks(label_positions, minor=True)
ax.set_xticklabels(labels, minor=True,rotation=90, **d)
# Set bold font and increased font size for both x and y-axis labels
#ax.tick_params(axis='x', labelsize=14, labelweight='bold')
#ax.tick_params(axis='y', labelsize=14, labelweight='bold')
# Create a font properties object with bold weight
bold_font = font_manager.FontProperties(weight='bold', size=12)

# Set font weight to bold for numerical tick labels
for label in cb.ax.get_yticklabels():
    label.set_fontproperties(bold_font)


cb.ax.tick_params(labelsize=12, labelcolor='black')
#cbar.ax.set_ylabel('Scale Label', fontsize=14, fontweight='bold')
#cb.set_label('Colorbar Label', fontsize=14, fontweight='bold')
#font = {'family' : 'normal',
#        'weight' : 'bold',
#        'size'   : 40}

#mpl.rc('font', **font)
plt.clim(-0.2,0.2)
#plt.xlabel('Residue No')
#plt.ylabel('Residue No')
#cb.set_label(r"kT")
#plt.title('Nucleosome-Tail1')
plt.tight_layout()
plt.savefig(sys.argv[3])
#plt.savefig('octa_Tail1.png')

