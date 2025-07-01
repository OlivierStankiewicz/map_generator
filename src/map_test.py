from classes.Map import Map

map_instance: Map = Map.create_default()
print(map_instance)
map_representation = map_instance.to_dict()
print(map_representation)