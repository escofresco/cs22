# Homework 1: Graph ADT & Traversals

Follow the instructions [here](https://make-school-courses.github.io/CS-2.2-Graphs-Recursion/#/Assignments/01-Graph-ADT) to complete this assignment.

## Discussion Questions

1. How is Breadth-first Search different in graphs than in trees? Describe the differences in your own words.

Breadth-first Search (BFS) in graphs may end up visiting the same node more than once. 

2. What is one application of Breadth-first Search (besides social networks)? Describe how BFS is used for that application. If you need some ideas, check out [this article](https://www.geeksforgeeks.org/applications-of-breadth-first-traversal/?ref=rp).

If you've ever used Microsoft Paint, you may remember the flood fill feature. Their implementation of may have involved the use of breadth-first search. A canvas can be represented as a graph of pixels. And when a node (pixel) is clicked, all the neighboring nodes are filled with the new, selected color.

3. Compare and contrast Breadth-first Search and Depth-first Search by providing one similarity and one difference.

Breadth-first Search (BFS) and Depth-first Search (DFS) are both graph traversal methods. A difference between them is that BFS visits all nodes in order by DFS visits nodes in a sweeping fashion.

4. Explain why a Depth-first Search traversal does not necessarily find the shortest path between two vertices. What is one such example of a graph where a DFS search would not find the shortest path?

DFS exits when it finds the first correct path between two nodes. The reason this isn't guaranteed to find the shortest path is because the first correct path may not be the shortest path. An example is any graph where more than one path exists between two nodes and the shortest path isn't evaluated first.

5. Explain why we cannot perform a topological sort on a graph containing a cycle.
The topological invariant is that for any two directly connected nodes, there can only be one ordering. So even if there are multiple topological orderings, there can't be ambiguity about the relative ordering of a locally connected group of nodes.
