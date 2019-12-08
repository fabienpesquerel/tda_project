import numpy as np
import gudhi as gd
import matplotlib.pyplot as plt
import multiprocessing as mps

TOPOLOGICAL_COMPLEX = {
    'alpha' : gd.AlphaComplex,
    }

def persistence_of_function(sampling, f, cplx='alpha', n_pts=2500, plot=False,
                            persistence_dim_max=True, dim=0, sensitivity=0.1):
    X = sampling(n_pts)
    Y = f(X)
    alpha_complex = TOPOLOGICAL_COMPLEX[cplx](points=X)
    simplex_tree = alpha_complex.create_simplex_tree()
    filtration = simplex_tree.get_filtration()
    diagram_sampling = simplex_tree.persistence(persistence_dim_max=persistence_dim_max)
    for splx in filtration:
        simplex_tree.assign_filtration(splx[0], np.max(Y[splx[0]]))
    simplex_tree.initialize_filtration()
    simplex_tree.get_filtration()
    diagram_function = simplex_tree.persistence(persistence_dim_max=persistence_dim_max)
    denoised_dgm = [elmt for elmt in diagram_function
                    if elmt[0]==dim and (elmt[1][1] - elmt[1][0] > sensitivity)]
    if plot:
        plt.figure(figsize=(15, 8))
        plt.subplot(1, 2, 1)
        plt.scatter(X[:, 0], X[:, 1], c=Y)
        plt.subplot(1, 2, 2)
        gd.plot_persistence_diagram(denoised_dgm).show()

    return diagram_sampling, diagram_function, denoised_dgm

def histogram(sampling, bins):
    raise NotImplementedError

def histogram_adaptive():
    raise NotImplementedError

def parallel_coordinates():
    raise NotImplementedError

# Build things once, and then one can query visualization in a topologicaly aware fashion
class Visualize:
    def __init__():
        raise NotImplementedError




if __name__ == '__main__':

    def foo(x, sigma=.125, p0=np.array([0.25,0.25]), p1=np.array([0.75,0.75]), noise=0.5):
        a = 0.5 * np.exp(-np.sum((x-p0)**2,1)/sigma)
        b = 3*np.abs(np.sin(-np.sum((x-p1),1)/sigma))
        epsilon = np.random.rand(len(x))
        return a + b + noise*epsilon

    def sample(n_pts):
        return np.random.rand(n_pts, 2)

    a, b, _ = persistence_of_function(sample, foo, plot=True)
