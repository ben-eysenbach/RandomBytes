wiki_race
=========

Treats wikipedia as a graph, and uses a BFS to find the shortest connection between two pages

Utilizes the Wikipedia API to get the links reference on any given article, and uses them to built the graph.
This project was sparked by a game I heard about where kids tried to get from one Wikipedia page to another faster than their friends.

Right now, the program starts at one link and works towards the endpoint. In the future, I will modify it so that it works from both ends and meets in the middle.  This will not find a more optimal solution, but it will find an equally optimal solution in significantly less time.  Also note that, as it stands right not, humans still beat the program, as the program doesn't have the intuition to guess what will likely be a good link.

wiki_race2.py is the most recent version

wiki_race.py is an older version

wiki_abstract_race.py uses a dump of wikipedia abstracts(the introductory section) instead of querying the website.  The dump file can be found on the wikipedia website
