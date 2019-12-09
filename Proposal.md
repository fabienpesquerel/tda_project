# Scalable TDA and Visualization for model evaluation

Constraints : 10 min + 2 min questions

Here is a proposal for the skeleton of the presentation, with approximations
of the time budget spendable on each subsection. We should aim for ~ 1 slide/min.

| Section                                | Time estimate      |
|:---------------------------------------|-------------------:|
| Problem statement                      |              1 min |
| The Topological Lens                   |              1 min |
| Contribution : Handling the Lens       |              2 min |
| Topology-aware datacubes               |              1 min |
| Description of the panes               |              2 min |
| Application : model analysis           |              1 min |
| Application : sampling evaluation      |              1 min |
| Conclusion                             |              1 min |

## Problem Statement

Problems in high dimensions are increasingly common and hard to debug.

However, two central issues can be distinguished here :

1. We can't "see" in high dimensions. (no visualization of neighborhoods)
2. We don't know where to look. (volume of the space too large)

In most applications though, we are only interested in some regions of the space :
we could maybe tackle the second problem separately.

For physics models for instance, we are interested in regions of the space where the model
prediction does not match the experimental results, but not so much in regions where the
model is accurate enough.

> Note: the function being studied is not always the function indicating which regions
> to look at. For some applications, we are interested in regions where the prediction
> varies greatly, in which case we would draw information from the norm of the gradient
> rather than from the function itself.


## The Topological Lens

Topological information about a space is typically considered as a self-sufficient
entity to be studied separately, and giving information about the space.

This paper tries to use topology differently : not as a characterization of a space,
but as a lens, that indicates which regions of a space are interesting to look at,
guided by the topology defined by a function of this space.

Critical points of the function are linked to points of the space under study,
and indicate points of interest for debugging purposes for instance.

The paper introduces a visualization tool in two parts : an "overview" topological spine,
giving high-level information about which regions of the space are interesting, and a
"close-up" view with visualizations of the neighborhood of the point selected in the
overview panel. It introduces two forms of close-ups that will be discussed herefafter.


## Contribution : Handling the Lens

The major issue with this tool is it prohibitive computational complexity.

Study of high-dimensional spaces requires massive amounts of data, and
algorithms developed for topological study generally don't scale well to this
order of magnitude of data.

The main contribution of this paper is a scalable algorithm to build the "overview" pane
while maintaining ability to quickly display a close-up when a point is selected in the
said overview, making this tool usable in the context of deep neural networks or
high-dimensional sampling evaluation.

TODO: Present the said algorithm and explain its scalability


## Topology-aware datacubes

How to soundly discard information.

When using the topological lens, we now know not only where to look, but also where
*not* to look, because some regions do not contain extrema, or contain only extrema of
small persistence, which we can interpret as just noise. This means data concerning
those regions may safely be discarded, because fewer points are needed to
understand what happens in these regions.

The paper presents a quadtree-like structure able to box data points in data cubes
of varying volume, giving fine-grain details over regions of interest, and using
less storage for regions where more approximative information will suffice.

These topology-aware datacubes aggregate data under reasonable storage constraints,
while maintaining the topological feature hierarchy.


## Description of the panes

### The Overview : Topological Spines

TODO: 1-min presentation of the Topological Spines paper

### The Neighborhood : Density Scatterplots

When the number of samples increases significantly, standard scatterplots become harder
to read. Since this method is designed for large datasets, density plots are used instead.

The density of the data over two chosen dimensions is plotted in one of the panes.

Since only the density plots are displayed, it is not necessary to retain all the points
locations, but only the density grid for each datacube, up to a chosen resolution.
This can be nicely aggregated when datacubes are merged, without having to go through
the data all over again.

Density plots tend to shadow outliers, which is usually a critical drawback,
but is not so significant here because the resolution around outliers is much higher
thanks to the topology-aware datacubes that reliably identify significant outliers.

### The Neighborhood : Density Parallel Coordinates Plots

In parallel coordinate plots, each data point is plotted as the sequence of its
coordinates (i.e. a piecewise real-valued function) for a given ordering of the dimensions.
Lines representing all data points are stacked on the same plot.

Again a density plot is subsituted to deal with the large amount of data.
Since only the density plot up to a given resolution is needed, there is
as previously no need to store all the data, but only one histogram per dimension
(assuming the ordering of dimensions does not change), which is much more
computationally efficient.

Relations between adjacent coordinates are easier to see that between coordinates
farther apart, making the choice of the ordering more important than we would like,
particularly in the setting of high-dimensional analysis, where the number of such
orderings is unmanageable.


## Applications

### Deep Model Analysis : Inertial Confinement Fusion

See [Fabien's notes](README.md)

Conclusion: Overview brings some value, neighborhood visualization's value unclear.
Do the neighborhood visualizations mean anything ? Do they bring information about the network ?
Can we link information about the network with the plots we see ? Unclear.

### Distribution Comparison : Multiscale Simulation for Cancer Research

See [Fabien's notes](README.md)

Conclusion : Relevant samplings should produce roughly the same plots, regardless of
the projection chosen. Here the choice of visualization is not so critical because
all projections give relevant information if they don't match. Added value is observed.
No positive information on the match though : there can only be negative info in these plots.


## Conclusion

TODO: Maybe a note on the drawbacks of this method, and more specifically the choice of visualizations.

TODO: Wrap-up slide


# Resources

- [Scalable Topological Data Analysis and Visualization for Evaluating Data-Driven Models in Scientific Applications](http://www.sci.utah.edu/~shusenl/publications/VAST_19.pdf)
- [Topological spines : A structure-preserving visual representation of scalar fields](https://www.academia.edu/844244/Topological_Spines_A_Structure-preserving_Visual_Representation_of_Scalar_Fields)
