from graph import Graph
import util

graph = Graph()

data_files = ["data/1_Poisy-ParcDesGlaisins.txt", "data/2_Piscine-Patinoire_Campus.txt"]

for i, f in enumerate(data_files):
    data = util.read_route_data(f)
    graph.build_graph_from_route(data["we_holidays_date_go"], i + 1)
    graph.build_graph_from_route(data["we_holidays_date_back"], i + 1)


g2 = graph.copy()
time = "6:30"
start = "Vernod"
departures = g2.get_departures(time , start)
print("-------DEPARTS-------------")
print(departures)
print("------------------------------")
d2 = g2.hours_from_station(time, start)
print(len(g2.edges))
print(len(d2))
g2.set_weights(d2, start, True)
print(g2)

