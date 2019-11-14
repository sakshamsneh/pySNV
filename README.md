# pySNV
## STEPS
1. Take n random users from twitter.
2. Make a dataset of all hashtags, along with the sentiment of each user, from their last 20 tweets.
3. Generate a network graph from that data (using NetworkX), and export the data to be usable in Gephi.

In Gephi, we generated the graph, where,
1. Edge exists between nodes u and v, if they have tweeted on any same hashtag in their last 20 tweets.
2. Color of node is based on modularity (community clustering).
3. Size of node is based on betweenness centrality(more influential node=>bigger size).
4. Color of edge is based on color of their source node.
5. Labels are username of each node on twitter.
6. Edge thickness is based on weight assigned to them, as in, how many hashtags node u and v had in common(more thick edge=>more hashtags were same).


# PROPERTIES
## 72 nodes, 450 edges  (compiledGraph2.pdf)
Average Clustering Coefficient: 0.660

Modularity: 0.111

Number of Communities: 7

Average Path length: 2.4889173060528558

Graph Density: 0.176

Number of Weakly Connected Components: 4

## 372 nodes, 21926 edges   (compiledGraph2_full.pdf)
Average Clustering Coefficient: 0.799

Modularity: 0.112

Number of Communities: 5

Average Path length: 1.9387914402273965

Graph Density: 0.318

Number of Weakly Connected Components: 2