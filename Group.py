class Group:
    def __init__(self, name, house_cost):
        self.name = name
        self.house_cost = house_cost
        
    def add_properties(self, properties):
        self.properties = properties
        for i in self.properties:
            i.add_to_group(self)
