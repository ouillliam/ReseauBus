from graph import Graph
import util

graph = Graph()

data_files = ["data/1_Poisy-ParcDesGlaisins.txt", "data/2_Piscine-Patinoire_Campus.txt"]

for i, f in enumerate(data_files):
    data = util.read_route_data(f)
    graph.build_graph_from_route(data["we_holidays_date_go"], i + 1)
    graph.build_graph_from_route(data["we_holidays_date_back"], i + 1)

t = "12:00"
start = "CAMPUS"
end = "LYCÉE_DE_POISY"

path1 = graph.get_path(start, end, t, "foremost")
path2 = graph.get_path(start, end, t, "fastest")
path3 = graph.get_path(start, end, t, "shortest")

print(path1)
print(path2)
print(path3)

# string = ""
# for node in path:
#     string += f"{graph.get_label_from_value(node)} -> "
# print(string)

(21, 9, 3.0, 2, '7:30', '7:33')
(9, 8, 4.0, 1, '7:35', '7:37')
(8, 7, 4.0, 1, '7:37', '7:41')
(7, 6, 8.0, 1, '7:41', '7:49')
(6, 5, 1.0, 1, '7:49', '7:50')
(5, 4, 4.0, 1, '7:50', '7:54')
(4, 3, 5.0, 1, '7:54', '7:59')
(3, 2, 3.0, 1, '7:59', '8:02')