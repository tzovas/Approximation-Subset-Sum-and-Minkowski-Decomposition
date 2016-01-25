# Approximation-Subset-Sum-and-Minkowski-Decomposition

An algorithm for approximating the Multidimensional Subset Sum problem. 
Using this algorithm we can also solve the Minkowski Decomposition of 2-dimensional polygons.
The code is based on a paper under revision: "Approximating Multidimensional Subset Sum and the Minkowski Decomposition of Polygons" by Ioannis Z.Emiris, Anna Karasoulou and Charilaos Tzovas.

Multidimensional Subset Sum (kD-SS):
Input: A set of vectors S={v_i | v_i in Z^k}, a target vector t in Z^k and parameter 0<e<1.
Question: Find a subset S' of S that sums to z and z is close to t such that: dist(t,z)< e|t|.

Minkowski Decomposition:
Input: Polytope Q.
Question: Find two polytopes A,B such that A+B=Q where A+B is their Minkowski Sum.
(see https://en.wikipedia.org/wiki/Minkowski_addition)
