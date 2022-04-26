# ReseauBus


This project is an implementation of the Sibra bus network featuring pathfinding algorithm to find the shortest path between two bus stops given a departure time.

Documentation for the project can be found in the `/docs` directory.

# How to use

Clone the directory and execute `reseau_bus.py`.

Choose between the weekends and holidays hours or the regular ones, and input the start station, end station, departure time and path option.

The program will print the shortest path given the path option.

Path options are as follow :
- `foremost` : arrive the earliest possible at the destination.
- `fastest` : fastest path between the two stations, not considering the possible wait for the next departures at the start station.
- `shortest` : the path with the least edges between the two stations.  
- `compare` : compare all three possible paths.  