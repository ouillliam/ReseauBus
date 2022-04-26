
from graph import Graph
import util

data_files = ["data/1_Poisy-ParcDesGlaisins.txt", "data/2_Piscine-Patinoire_Campus.txt"]
bus_network = Graph()

if __name__ == "__main__":
    
    print("---------------------------------------\nRéseau bus\n---------------------------------------")
    
    user_input = input("WE/Vacances ? (y/n)\n")

    while user_input not in ("y", "n"):
        print("Erreur.")
        user_input = input("WE/Vacances ? (y/n)\n")
    
    we_holiday = True if user_input == "y" else False

    for i, f in enumerate(data_files):
        data = util.read_route_data(f)
        if we_holiday:
            bus_network.build_graph_from_route(data["we_holidays_date_go"], i + 1)
            bus_network.build_graph_from_route(data["we_holidays_date_back"], i + 1)
        else:
            bus_network.build_graph_from_route(data["regular_date_go"], i + 1)
            bus_network.build_graph_from_route(data["regular_date_back"], i + 1)

    print("---------------------------------------\nArrêts\n---------------------------------------\n")
    for stop in bus_network.get_labels():
        print(stop)
    print("---------------------------------------\n")

    while True:
        start = input("Choix départ : ")
        while start not in bus_network.get_labels():
            print("Erreur.")
            start = input("Choix départ : ")

        end = input("Choix arrivée : ")
        while start not in bus_network.get_labels():
            print("Erreur.")
            end= input("Choix arrivée : ")

        time = input("Heure de départ (HH:MM) : ")
        while start not in bus_network.get_labels():
            print("Erreur.")
            time = input("Heure de départ (HH:MM) : ")

        mode = input("option de trajet (foremost/fastest/shortest/compare) : ")
        while mode not in ("foremost", "fastest", "shortest", "compare"):
            print("Erreur.")
            mode = input("option de trajet (foremost/fastest/shortest/compare) : ")

        print("---------------------------------------\n")

        if mode == "compare":
            for m in ("foremost", "fastest", "shortest"):
                path = bus_network.get_path(start, end, time, m)

                path_str = ""
                for i in range(len(path)):
                    path_str += bus_network.get_label_from_value(path[i])
                    if i < len(path) - 1:
                        path_str += " -> "
                print(f"Trajet {m} :")
                print(path_str)
        else:
            path = bus_network.get_path(start, end, time, mode)
            path_str = ""
            for i in range(len(path)):
                path_str += bus_network.get_label_from_value(path[i])
                if i < len(path) - 1:
                    path_str += " -> "
            print("Trajet :")
            print(path_str)
    
        print("---------------------------------------\n")
    
