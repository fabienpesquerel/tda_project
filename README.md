## What
scalable solution to explore and analyze high-dimensional functions often encountered in the scientific data analysis pipeline

## How
- new streaming neighborhood graph construction
- corresponding topology computation
- novel data aggregation scheme: topology aware datacubes

## Result
interactive exploration of both the topological and the geometric aspect of high-dimensional data

## Proof of concept
- high-energy-density (HED) physics
- computational biology


# Introduction
## Problems
They need tools that can discriminate between regions of parameter space where the model has errors small enough to make the model useful for design work. Likewise, they need to know where errors have grown large enough to make the model unreliable for predicting real-world conditions. Such requirement highlights the need in the scientific community to augment global loss functions and response metrics with methods that can steer the scientific user toward regions of high value and confidence.

many of the questions raised [by the scientific community] can be expressed as the analysis of a high-dimensional function.

In general, we are given a high-dimensional domain, i.e., a set of input parameters or a latent space, as well as a scalar function on that domain, to analyze.

## Tools
### Which
We propose to use topological techniques to address this challenge.

### Why
In general, computing the topology of a given function provides insights into both its global behavior and it local features, since the measure of importance is variation in its function value, i.e., persistence, rather than the size of a feature. Furthermore, topology provides a convenient abstraction for both analysis and visualization, whose complexity depends entirely on the function itself rather than the number of samples used to represent it.

### Problem (why nobody did that before)
However, topological information alone can provide only limited insight because, for example, knowing that there exist two significant modes is of little use without knowing where in the domain these modes exist and how much volume they account for.

### Solution
We, therefore, propose to augment the topological information with complementary geometric information by introducing the notion of topological datacubes.

## What they claims to have done
- identified the shared analysis challenges posed by many data-driven modeling applications
- developed a robust topological data analysis computation pipeline that scales to millions of samples
- developed an interactive visual analytics system that leverages both topological and geometric information for model analysis
- addressed the model analysis challenges of a data-driven inertial confinement fusion surrogate and solved the adaptive sampling evaluation problem for a large-scale biomedical simulation.


# Related works
- Scientific Machine Learning
- Deep Learning Model Interpretation: we can approach the interpretation challenge from a model agnostics perspective or not. -> build a general purpose neural-network-interpreting tool by exploiting high-dimensional visualization techniques.
- Topological Data Analysis
  - The topology of scalar valued function has been utilized for analyzing scientific data in previous works
  - The scalability challenge for handling functions defined on the large 3D volumetric domain has also been addressed in several previous works, e.g., parallel merge tree computation
  - However, in many scientific applications, scientists are also interested in studying the properties defined in a high-dimensional domain.
- Data Aggregation Visualization: As the number of samples increases
in a dataset, a visual analytics system not only needs to cope with the computational/rendering strain but also to handle the visual encoding challenges -> adopt a topology-aware datacube design for aggregating large data according to their topological partition

# Application Tasks Analysis
## Situs
There are analysis tasks shared by many data-driven applications.

Despite the disparate application domains, there are number of recurring analysis tasks, which often lie at the very heart of the scientific interpretation -> dedicated visual analysis tool to streamline the analysis process and accelerate discovery.

## Question
How we can solve these tasks by combining topological data analysis with interactive data visualization.

## processing pipeline
- sample acquisition
- sampling
- modeling
- analysis

The corresponding computational pipeline typically has three main stages:
- sampling: generation of samples in the input parameter space.
- simulation: run simulations on all input parameter combinations and gather the outputs to create the ensemble
- modeling: simulation results are used to train a cheaper surrogate for one or multiple of the output quantities to enable statistical inference, uncertainty quantification, or parameter calibration

Four generic tasks typically encountered (independent of the specific application):
- T1: Analyze the sampling pattern to ensure uniform coverage or verify a sampling objective -> How we sample the high-dimensional input space has a significant impact on the downstream analysis
- T2: Explore quantities of interest with respect to the input parameter space -> Given the simulation outputs, we then need to identify where we achieved or failed to achieve our objective
- T3: Verify model convergence, explore residual errors, and evaluate local and global reliability -> evaluate the model behavior and interpret the model’s internal representations
- T4: Explore the sensitivities of the model with respect to the input parameters

T2, T3: studying the behavior of functions in certain high-dimensional space
T4: understand the relationship between specific input parameters and model output

# Streaming Topological Data Analysis

## Morse Complex and Extremum Graphs

For dimensions beyond three, computing the entire Morse complex is infeasible [14], so we follow [7, 10] and concentrate on extremum graphs.

An **extremum graph** contains all local maxima of the function together with the saddles connecting them. To approximate the extremum graph for sampled functions, we define an undirected neighborhood graph on all input vertices to approximate the domain manifold M. Given a graph, we approximate the gradient as the steepest ascending edge incident to a given vertex and construct the ascending integral line by successively following steepest edges to a local maximum.

Implementation details: In practice, this traversal is implemented as a short-cut union-find at near linear complexity per vertex. In this process, each vertex is labeled by the index of its corresponding stable manifold, and saddles are identified as the highest vertex connecting two neighboring maxima.

Subsequently, we form the extremum graph by considering arcs between saddles and neighboring maxima.

## Streaming Extremum Graph
### Problem
As the dimension of M increases, more vertices are required to reliably approximate f: neighborhood graphs may require several magnitude more storage space than the vertex alone, which may quickly reach the memory limitation of most desktop systems.

### Solution
Two-pass streaming algorithm for constructing extremum graphs that store only the vertices and an appropriate neighborhood look-up structure to avoid keeping the massive neighborhood graph in memory. Streaming scheme to avoid storing the full graph in memory by doing neighborhood lookup and edge pruning for each point individually.
- A vertex always maintains its currently steepest neighbor, which is initialized to be the vertex itself: Store the steepest direction for topology computation
- Visit all edges
- Morse complex construction (sampled): near-linear union-find is used as a short-cut to the steepest neighbor link to point to the corresponding local maximum of each vertex
- Morse complex construction (assembling): reiterate the steaming graph in a second pass

### Computing the neighborhood graph
- β -skeletons and their relaxed variants provide significantly more stable results for computing topological structure: an approximated k-nearest neighbor graph of sufficiently large k is computed first and then pruned using the empty region test defined by β.
- Exploit the parallelism in the neighborhood query and the edge-pruning steps. Proof of concept: GPU version is approximately 70% faster than the CPU counterpart in one of their example.

### Chosing hyperparameters
- k: gradually increase k in the initial k-nearest neighborhood query stage and observe at which point the number of true edges of the empty region graph begins to stabilize.
- β: Nothing

# Data Aggregation and Visualization

**Fact 1:** Topological data analysis alone reveals little geometric information outside the location of critical points in parameter space: joint analysis of topological features and their corresponding geometric data as expressed through parallel coordinates and scatterplots.
**Fact 2:** When dealing with large datasets, visualization systems often need to address the scalability challenge from two aspects.
- On one hand, as the number of sample increases, the standard visual encodings, such as scatterplots and parallel coordinates, become increasingly ineffective due to overplotting and thus overwhelm users’ perceptual capacity.
- On the other hand, the increasing data size induces a heavy computational cost for processing and rendering, which may create latency that hinders the interactivity of the tool.
One strategy to address this problem is datacubes (OLAP-cubes) style aggregation techniques [19, 23], which provide summary information (i.e., density/histogram) to overcome the overplotting while preserving joint information to enable linked selection and interactive exploration. However, such aggregation techniques are not directly applicable here as they summarize the dataset’s entire domain without considering the topological segmentation.


**topology-aware datacubes** allows interactive linked view exploration:
- aggregate data to enable interactive visual exploration
- maintain the topological feature hierarchy

**Visualization tools:**
- **Topological Spine:** relative distance and size of the peaks in the function of interests
- **Density Scatterplots:** for any topological segment, query the datacube, obtain the 2D histogram and render the estimated joint distribution density to avoid the overplotting issue in the standard scatterplot (with gamma correction).
- **Density Parallel Coordinates:**
  - discretize each axis according to the resolution (r) of the datacube; thus, there would be r bins on each axis.
  - draw lines from each bin to every other bin on the adjacent axis; thus, there would be r 2 lines between every two adjacent axes.
  - To draw each line, we query the corresponding density from the 2D joint distribution of the neighboring axes and map the value to the opacity (with gamma correction).

**How?**
- The extremum graph can be simplified by merging extrema (each corresponding to a segment of the data) and removing less significant saddles based on the persistence value. One can presimplify the topological segmentation hierarchy and focus only on the top levels for our analysis. During the exploration, the user can explore different levels of granularity by altering the persistence threshold.
- precompute datacubes for samples in each leaf segment in the simplified topology hierarchy, where each datacube preserves the localized geometric features.



# Our ideas
- This could be great to implement the simple extremum graph algorithm and make, for a genric function, some plots. (number of points, time), (dimension, time), (number of points, flops), (dimension, flops)
- Extremum Graph: Limite de calcul et lien avec l'estimation de densité pour la méhode des kppv. Egalement en lien avec le théorème de Penrose qu'on a pu voir en cours de GraphsML.
- The space of NN is a functional space parametrized weights between layers. Maybe one can try to apply those methods to better understand the topology in this functional space.

# Libraries for the codebase (that might be useful)
- Gudhi (For easy TDA implementation)
- Faiss (knn and graph structure)
