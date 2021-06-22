import matplotlib.pyplot as plt

vs = [234,162,129,120,125,121,113,107,109,165,81,132,108,100,106,100,91,99,166,92,103,93,93,95,92,95,85,90,100,129,118,95,139,91,88,87,125,90,88,150,90,89,95,84,113,103,113,155,206,136,88,132,150,99,90,113,109,98,89,95,100,101,137,108,87,90,149,131,136,85,171,112,159,99,90,102,87,162,113,157,84,94,186,88,82,90,121,130,113,85,99,95,140,90,122,98,126,147,159,108]
netor=[207,214,184,187,212,151,189,197,187,154,345,194,211,201,181,185,187,176,211,211,172,177,212,191,205,176,208,173,147,214,177,166,174,229,152,214,181,213,135,196,191,202,189,208,191,204,208,171,202,198,198,215,183,168,196,158,190,197,188,183,191,181,208,182,188,188,157,201,190,155,214,167,197,205,217,203,160,152,189,192,189,168,193,184,200,183,186,154,193,187,199,222,159,221,226,191,185,191,210,179]

medianprops = dict(linestyle='solid', linewidth=2.5, color='black')

box_plot_data=[vs,netor]
box=plt.boxplot(box_plot_data,patch_artist=True,showfliers=False,labels=['5GR-VS','NetOr'], medianprops=medianprops)

for patch in box['boxes']:
    patch.set_facecolor('orange')

plt.title("System Instantiation Delay Comparison between 5GR-VS and NetOr")
plt.xlabel("System")
plt.ylabel("Delay(ms)")
plt.show()