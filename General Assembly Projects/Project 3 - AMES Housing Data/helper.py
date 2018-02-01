import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.model_selection import cross_val_score

def corr_heatmap(data, annot = True, method = "pearson"):

    mean_corr = data.corr(method = method)

    fig, ax = plt.subplots(figsize=(15,10))
    ax = sns.heatmap(mean_corr, ax=ax,  square = True, linecolor='white', annot = annot, cmap='RdBu', vmin=-1, vmax=1, fmt = '.2f')

    ax.set_xticklabels(ax.xaxis.get_ticklabels(), fontsize=14, rotation=90)
    ax.set_yticklabels(ax.yaxis.get_ticklabels(), fontsize=14, rotation=0)

    plt.show()

def currency(x, pos):
    return '${:1.0f}K'.format(x*1e-3)
