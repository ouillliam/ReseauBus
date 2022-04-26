from graph import Graph
import util

graph = Graph()

data_files = ["data/1_Poisy-ParcDesGlaisins.txt", "data/2_Piscine-Patinoire_Campus.txt"]

for i, f in enumerate(data_files):
    data = util.read_route_data(f)
    graph.build_graph_from_route(data["we_holidays_date_go"], i + 1)
    graph.build_graph_from_route(data["we_holidays_date_back"], i + 1)

t = "6:20"
start = "GARE"
end = "Pommaries"

path1 = graph.get_path(start, end, t, "foremost")
path2 = graph.get_path(start, end, t, "fastest")
path3 = graph.get_path(start, end, t, "shortest")

print(path1)
print(path2)
print(path3)

departures = graph.get_departures(t, start)
print(departures)

# string = ""
# for node in path:
#     string += f"{graph.get_label_from_value(node)} -> "
# print(string)

