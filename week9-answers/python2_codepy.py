import hifive
import numpy as np
import matplotlib.pyplot as plt


## Working with the HiC data

hic=hifive.HiC('porject_norm', 'r')
data = hic.cis_heatmap('chr13', 100000, datatype='fend', arraytype='full', diagonalincluded=True)
data[np.where(data[:,:,0] == 0)] = 1
data[np.where(data[:,:,1] == 0)] = 1
enrichment = data[:, :, 0] / data[:, :, 1]
enrichment = np.log2(enrichment)

plt.pcolor(enrichment)
plt.show()

## Compartment analysis

Comp = hifive.hic_domains.Compartment(hic, 100000, chroms=['chr13'], out_fname='tmp.hdf5')
Comp.write_eigen_scores('hic_comp.bed')

X = Comp.positions['chr13']
Y = Comp.eigenv['chr13']

## For continuation, I used the command line script:
#bedtools intersect -a data/WT_fpkm.bed -b hic_comp.bed -f 0.50 -wb > intersects.bed

# Please see ipython notebook for the rest