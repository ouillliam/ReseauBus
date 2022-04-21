from datetime import time, timedelta
import util

class Graph:
    def __init__(self, vertices = [], labels = [], edges = []):
        self.vertices = vertices
        self.labels = labels
        self.edges = edges #(start, end, weight, route_label)

    def copy(self):
        return Graph(self.vertices, self.labels, self.edges)

    def get_vertices_from_route(self, route):
        for station in route.keys():
            for label in self.labels:
                if station == label[1]: 
                    break
            else:
                self.vertices.append(len(self.vertices))
                self.labels.append( ( self.vertices[-1], station ) )

    def get_value_from_label(self, label):
        for node_label_tuple in self.labels:
            if node_label_tuple[1] == label:
                return node_label_tuple[0]

    def get_label_from_value(self, value):
        for node_label_tuple in self.labels:
            if node_label_tuple[0] == value:
                return node_label_tuple[1]

    def get_edges_from_route(self, route, route_label):

        def get_travel_times_between(start, end):
            travel_times = []
            for i in range(len(route[start])):
                travel_time = None
                departure_time = route[start][i]
                arrival_time = route[end][i]
                if departure_time != '-' and arrival_time != "-":
                    diff = util.time_between(departure_time, arrival_time)
                    travel_time = diff.total_seconds() / 60
                #print(f"{start}->{end} {departure_time} {travel_time}")
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
        self.get_vertices_from_route(route)
        self.get_edges_from_route(route, route_label)
        

    def build_graph_from_routes(self, routes):
        self.build_graph_from_routes(routes)

    def get_departures(self, time, start):

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
        departures = self.get_departures(departure_time, station)
        start = self.get_value_from_label(station)

        return self.get_updated_edges_from_departures(departures[:], departures[:], [start])

    def get_updated_edges_from_departures(self, to_visit, departures, visited):
        departure = to_visit.pop(0)
        end = departure[1]
        departure_time, travel_time = departure[2][1], departure[2][2]

        arrival_station = self.get_label_from_value(end)
        arrival_time = util.add_travel_time(departure_time, travel_time)

        departures_from_next_station = [] 

        if end not in visited:
            departures_from_next_station = self.get_departures(arrival_time , arrival_station)
            departures.extend(departures_from_next_station)
            to_visit.extend(departures_from_next_station)
            visited.append(end)

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

            if not wait_departures and i > 0 and d[3] == departures[i - 1][3] : 
                minutes_between = 0

            weight = minutes_between + travel_time
            final_time = util.add_travel_time(departure_time, travel_time)
            edge = (d[0], d[1], weight, d[3], departure_time, final_time)
            weighted_edges.append(edge)
        
        self.edges = weighted_edges

    def __str__(self):
        string = ""
        for e in self.edges:
            final_time = e[4] if len(e) >= 5 else ""
            string = string + f"Ligne {e[3]} {self.get_label_from_value(e[0])} -> {self.get_label_from_value(e[1])} {e[2]} {final_time}\n"
        return string

    