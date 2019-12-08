import numpy as np
import gudhi as gd
import matplotlib.pyplot as plt
import multiprocessing as mps

# Global - Moving them in a config.py ?

TOPOLOGICAL_COMPLEX = {
    'alpha' : gd.AlphaComplex,
    'rips' : gd.RipsComplex,
    }

COLOR_MAP = ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
             'Set1', 'Set2', 'Set3',
             'tab10', 'tab20', 'tab20b', 'tab20c']

# Useful functions for the pipeline described in the paper

def persistence_of_function(sampling, f, cplx='alpha', n_pts=2500,
                            persistence_dim_max=True, max_dimension=2):
    X = sampling(n_pts)
    Y = f(X)
    if cplx == 'rips':
        topological_complex = TOPOLOGICAL_COMPLEX[cplx](points=X, max_edge_length=1.7)
        simplex_tree = topological_complex.create_simplex_tree(max_dimension=max_dimension)
    elif cplx == 'alpha':
        topological_complex = TOPOLOGICAL_COMPLEX[cplx](points=X)
        simplex_tree = topological_complex.create_simplex_tree()
    filtration = simplex_tree.get_filtration()
    diagram_sampling = simplex_tree.persistence(persistence_dim_max=persistence_dim_max)
    for splx in filtration:
        simplex_tree.assign_filtration(splx[0], np.max(Y[splx[0]]))
    simplex_tree.initialize_filtration()
    simplex_tree.get_filtration()
    diagram_function = simplex_tree.persistence(persistence_dim_max=persistence_dim_max)

    return diagram_sampling, diagram_function

def denoise_diagram(dgm, sensitivity):
    diagrams = {}
    if type(sensitivity) == int:
        for elmt in dgm:
            if (elmt[1][1] - elmt[1][0] > sensitivity):
                try:
                    diagrams[f'{elmt[0]}'].append(elmt)
                except:
                    diagrams[f'{elmt[0]}'] = [elmt]
    else:
        max_dim = len(sensitivity)
        for elmt in dgm:
            if elmt[0] <= max_dim:
                if (elmt[1][1] - elmt[1][0] > sensitivity[elmt[0]]):
                    try:
                        diagrams[f'{elmt[0]}'].append(elmt)
                    except:
                        diagrams[f'{elmt[0]}'] = [elmt]
    return diagrams

def plot_diagram(dgm, show=True):
    if show:
        plt.figure(figsize=(15,8))
    gd.plot_persistence_diagram(dgm)
    if show:
        plt.show()

def parallel_coordinates(coordinates, values, labels, cmap=4):
    """Plot 2d array `values` using K parallel coordinates.
    Arguments:

        coordinates -- list or array of K elements containg coordinate
            names,
        values -- (K,N)-shaped array of N data points with K
            coordinates,
        labels -- list or array of one string per data point
            describing its class membership (category)
    """

    ax = plt.subplot(111)

    # find names and number of different classes
    ulabels = np.unique(labels)
    n_labels = len(ulabels)
    
    # for each select distinct colors from Accent pallette
    cmap = plt.get_cmap(COLOR_MAP[cmap])
    colors = cmap(np.arange(n_labels)*cmap.N/(n_labels+1))

    # change the label strings to indices into class names array
    class_id = np.searchsorted(ulabels, labels)
    lines = plt.plot(values[:,:], 'k')
    [ l.set_color(colors[c]) for c,l in zip(class_id, lines) ]

    # add grid, configure labels and axes
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_position(('outward', 5))
    ax.spines['bottom'].set_visible(False)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('none')
    
    plt.xticks(np.arange(len(coordinates)), coordinates)
    plt.grid(axis='x', ls='-')

    leg_handlers = [ lines[np.where(class_id==id)[0][0]] 
                    for id in range(n_labels)]
    ax.legend(leg_handlers, ulabels, frameon=False, loc='upper left',
            ncol=len(labels),
            bbox_to_anchor=(0, -0.03, 1, 0))


def histogram(sampling, bins):
    raise NotImplementedError

def histogram_adaptive():
    raise NotImplementedError


# Build things once, and then one can query visualization in a topologicaly aware fashion
class Visualize:
    def __init__():
        raise NotImplementedError




if __name__ == '__main__':

    # def foo(x, sigma=.125, p0=np.array([0.25,0.25]), p1=np.array([0.75,0.75]), noise=0.5):
    #     a = 0.5 * np.exp(-np.sum((x-p0)**2,1)/sigma)
    #     b = 3*np.abs(np.sin(-np.sum((x-p1),1)/sigma))
    #     epsilon = np.random.rand(len(x))
    #     return a + b + noise*epsilon

    # def sample(n_pts):
    #     return np.random.rand(n_pts, 2)

    # a, b, _ = persistence_of_function(sample, foo, plot=True)
    a = np.random.randn(10, 5)
    b = np.hstack((a, a[:,-1].reshape(10,-1)+2)).T
    print(b.shape)
    l = np.arange(6)
    ll = [0,1,1,1,0,0,1,1,1,0]
    parallel_coordinates(l,b,ll)
    plt.show()
