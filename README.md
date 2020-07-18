# Homework 1: Graph ADT & Traversals

Follow the instructions [here](https://make-school-courses.github.io/CS-2.2-Graphs-Recursion/#/Assignments/01-Graph-ADT) to complete this assignment.

## Discussion Questions

1. How is Breadth-first Search different in graphs than in trees? Describe the differences in your own words.

Breadth-first Search (BFS) in graphs may end up visiting the same node more than once. 

2. What is one application of Breadth-first Search (besides social networks)? Describe how BFS is used for that application. If you need some ideas, check out [this article](https://www.geeksforgeeks.org/applications-of-breadth-first-traversal/?ref=rp).

If you've ever used Microsoft Paint, you may remember the flood fill feature. Their implementation of may have involved the use of breadth-first search. A canvas can be represented as a graph of pixels. And when a node (pixel) is clicked, all the neighboring nodes are filled with the new, selected color.
