from datetime import time, timedelta
import util
import math

class Graph:
    def __init__(self, vertices = [], labels = [], edges = []):
        self.vertices = vertices
        self.labels = labels
        self.edges = edges #(start, end, weight, route_label)

    def get_labels(self):
        return [self.get_label_from_value(v) for v in self.vertices]

    
    def copy(self):
        """
        Return a copy of  the graph
 
        Returns:
            A copy of the graph
        """
        return Graph(self.vertices, self.labels, self.edges)

    def build_vertices_from_route(self, route):
        """
        Extract the vertices corresponding to bus stops from a route and add them 
        to the graph vertices and labels
        
        a route is a dict of bus stops and their hours.
        
        Args:
            route (dict): The route to extract vertices from
    
        """
        for station in route.keys():
            for label in self.labels:
                if station == label[1]: 
                    break
            else:
                self.vertices.append(len(self.vertices))
                self.labels.append( ( self.vertices[-1], station ) )

    def get_value_from_label(self, label):
        """
        Get a vertex's value from its label
        
        Args:
            label (string): The vertex's label
        
        Returns:
            (int) The vertex's value
        """
        for node_label_tuple in self.labels:
            if node_label_tuple[1] == label:
                return node_label_tuple[0]

    def get_label_from_value(self, value):
        """
        Get a vertex's label from its value
        
        Args:
            value (int): The vertex's value
        
        Returns:
            (string) The vertex's label
        """
        for node_label_tuple in self.labels:
            if node_label_tuple[0] == value:
                return node_label_tuple[1]

    def build_edges_from_route(self, route, route_label):
        """
        Extract the edges corresponding to lines between bus stops from a route and add them 
        to the graph edges with the given label.

        The edge will be of the following form :
        [start_value, end_value, travel_times, route_label]
        
        a route is a dict of bus stops and their hours.
        
        Args:
            route (dict): The route
            route_label (string): The label used to identify different routes 
        

        Subfonctions :
            get_travel_times_between(start, end):
                Get all the possible travel times between two stations 
                from their hours.

                 Args:
                    start (string): The start station's label
                    route_label (string): The en station's label

                Returns:
                    travel_times (float[]) : all possible travel times between start and end

        """

        def get_travel_times_between(start, end):
            travel_times = []
            for i in range(len(route[start])):
                travel_time = None
                departure_time = route[start][i]
                arrival_time = route[end][i]
                if departure_time != '-' and arrival_time != "-":
                    diff = util.time_between(departure_time, arrival_time)
                    travel_time = diff.total_seconds() / 60
                travel_times.append((departure_time, travel_time)) 
            return travel_times

        for i, station in enumerate(route.keys()):
            if i < len(route.keys()) - 1:
                start_station = station
                end_station = list(route.keys())[ i + 1 ]
                start_value = self.get_value_from_label( start_station )
                end_value = self.get_value_from_label( end_station )
                travel_times = get_travel_times_between(start_station, end_station)
                no_station_found = False
                
                # Check if buses ever stop at the next station, otherwise look for a valid station
                while all([travel_time == None for (_, travel_time) in travel_times]) and not no_station_found: 
                    if i + 1 < len(route.keys()) - 1 :
                        i += 1
                        end_station = list(route.keys())[ i + 1]
                        end_value = self.get_value_from_label( end_station )
                        travel_times = get_travel_times_between(start_station, end_station)
                    else:
                        no_station_found = True  
                        break  

                if not no_station_found:
                    self.edges.append( [start_value, end_value, travel_times, route_label] )


    def build_graph_from_route(self, route, route_label):
        """
        Call the build_vertices and build_edges methods of the graph.
        
        Args:
            route (dict): The route
            route_label (string): The label used to identify different routes 
        """
        self.build_vertices_from_route(route)
        self.build_edges_from_route(route, route_label)


    def get_departures(self, time, start):
        """
        Return the earliest possible departures from a given station at the given time.
        
        Args:
            time (string): The time you arrived at the station at
            start (string): The station label 
        

        Returns :
           departures (edge[]): An array of edges corresponding to the possible departures.

           A departure is of the following form : [start_value, end_value, [time, departure_time, travel_time], route_label]

        """

        t1 = util.to_datetime(time)
        departures = []
        departures_no_hours_found = [] 
        for e in self.edges:
            station = self.get_label_from_value(e[0])
            if station == start:
                # make a copy and not a reference to avoid modifying the edges
                departures.append(e[:])
    
        for d in departures:
            for hours in d[2]:
                departure_time = hours[0]
                travel_time = hours[1]
                if departure_time == '-':
                    continue
                t2 = util.to_datetime(departure_time)
                
                if t2 >= t1 and travel_time != None:
                    d[2] = (time, departure_time, travel_time)
                    break
            else:
                departures_no_hours_found.append(d)

        # Remove departures where the bus did not stop after the given time
        departures = [d for d in departures if d not in departures_no_hours_found]

        return departures


    def hours_from_station(self, departure_time, station):
        """
        Return the earliest possible departures from a given station at the given time.
        
        Args:
            time (string): The time you arrived at the station at
            start (string): The station label 
        

        Returns :
           departures (edge[]): An array of edges corresponding to the possible departures.

           A departure is of the following form : [start_value, end_value, [time, departure_time, travel_time], route_label]

        """
        departures = self.get_departures(departure_time, station)
        start = self.get_value_from_label(station)

        return self.get_updated_edges_from_departures(departures[:], departures[:], [start])

    def get_updated_edges_from_departures(self, to_visit, departures, visited):
        """
        Return the graph edges with their departure time updated after the given departures.

        Before :
        Node_1, 7:30 -> Node_2, [...] -> Node_3, [...]

        After :
        Node_1, 7:30 -> Node_2, 7:35 -> Node_3, 7:40
        
        Args:
            to_visit (edge[]): edges to visit
            departures (edge[]): the constructed array
            visited (int[]) : the visited stations 
        

        Returns :
           departures (edge[]): An array of edges corresponding to the possible departures.

           A departure is of the following form : [start_value, end_value, [time, departure_time, travel_time], route_label]

        """
        departure = to_visit.pop(0)
        end = departure[1]
        departure_time, travel_time = departure[2][1], departure[2][2]

        arrival_station = self.get_label_from_value(end)
        arrival_time = util.add_travel_time(departure_time, travel_time)

        departures_from_next_station = [] 
        to_update = []

        if end not in visited:
            departures_from_next_station = self.get_departures(arrival_time , arrival_station)
            #departures = [*departures_from_next_station, *departures]

            # neaty hack to keep exploring from the current route first 
            departures_from_next_station.reverse()
            to_visit = [*departures_from_next_station, *to_visit]

            departures.extend(departures_from_next_station)
            #to_visit.extend(departures_from_next_station)
            visited.append(end)
        else:
            #departures_from_next_station = self.get_departures(arrival_time , arrival_station)
            to_remove = []
            for d in departures:
                if d[0] == end and util.to_datetime(arrival_time) < util.to_datetime(d[2][1]):
                    if end not in to_update:
                        to_remove.append(d)
                        departures_from_next_station = self.get_departures(arrival_time , arrival_station)
                        #departures = [*departures_from_next_station, *departures]

                        # neaty hack to keep exploring from the current route first 
                        departures_from_next_station.reverse()
                        #to_visit = [*departures_from_next_station, *to_visit]

                        departures.extend(departures_from_next_station)
                        to_visit.extend(departures_from_next_station)
                        visited.append(end)
                        to_update.append(end)
            departures = [d for d in departures if d not in to_remove]

        if not to_visit:
            return departures 
        
        return self.get_updated_edges_from_departures(to_visit, departures, visited)
        
    def set_weights(self, departures, start_station, wait_departures = True):
        weighted_edges = []

        for i, d in enumerate(departures):
            arrival_time = d[2][0]
            departure_time = d[2][1]   
            travel_time = d[2][2]

            diff = util.time_between(arrival_time, departure_time)
            minutes_between = diff.total_seconds() / 60

            if not wait_departures and d[0] == self.get_value_from_label(start_station): 
                minutes_between = 0

            weight = minutes_between + travel_time
            final_time = util.add_travel_time(departure_time, travel_time)
            edge = (d[0], d[1], weight, d[3], departure_time, (arrival_time, final_time))
            weighted_edges.append(edge)
        
        self.edges = weighted_edges

    def get_distances(self, start, shortest = False):
        # Remove unconnected nodes and init distances
        start = self.get_value_from_label(start)
        to_visit = []
        for e in self.edges:
            for node in e[0:2]:
                if node not in [ n[0] for n in to_visit]:
                    node_dist = [node, math.inf, None]
                    if node == start:
                        node_dist[1] = 0 
                    to_visit.append(node_dist)

        def min_dist(node, dist, last_node, nodes):
            for n in nodes:
                if n[0] == node and dist < n[1]:
                    n[1] = dist
                    n[2] = last_node

        def update_distances(node, visited, nodes):
            for e in self.edges:
                curr_dist = node[1]
                if e[0] == node[0] and e[1] not in visited:
                    if shortest:
                        curr_dist += 1
                    else:
                        curr_dist += e[2]
                    min_dist(e[1], curr_dist, e[0], nodes)
                               
        def dijkstra(visited, nodes):
            # Find node with the shortest current distance
            node = (None, math.inf)

            for n in nodes:
                if n[1] < node[1] and n[0] not in visited:
                    node = n

            visited.append(node[0])

            # Update distances
            update_distances(node, visited, nodes)

            if len(visited) == len(nodes):
                return nodes

            return dijkstra(visited, nodes)

        distances = dijkstra([], to_visit[:])

        return distances
           
    def get_path_from_distances(self, destination, distances):

        def construct_path(dest, dists, path):
            path.append(dest)
            last_node = None
            for d in dists:
                if d[0] == dest:
                    last_node = d[2]
                    break

            if last_node == None:
                return path
            
            return construct_path(last_node, dists, path)

        path = construct_path(destination, distances, [])
        path.reverse()

        return path

    def get_path(self, start_station, end_station, departure_time, option = "foremost"):
        bus_network = self.copy()
        departures = bus_network.hours_from_station(departure_time, start_station)

        # for d in departures:
        #     print(d)

        # Foremost : wait_departures = True, shortest = False
        # Shortest : wait_departures = False, shortest = True
        # Fastest  : wait_departures = False, shortest = False

        wait_departures = True
        shortest = False

        if option == "shortest" or option == "fastest":
            wait_departures = False

            if option == "shortest":
                shortest = True


        bus_network.set_weights(departures, start_station, wait_departures)

        distances = bus_network.get_distances(start_station, shortest)
        destination = bus_network.get_value_from_label( end_station )
        path = bus_network.get_path_from_distances( destination , distances)

        return path


    def __str__(self):
        string = ""
        for e in self.edges:
            final_time = e[4] if len(e) >= 5 else ""
            string = string + f"Ligne {e[3]} {self.get_label_from_value(e[0])} -> {self.get_label_from_value(e[1])} {e[2]} {final_time}\n"
        return string

    