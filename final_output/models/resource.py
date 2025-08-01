class Resource:
    def __init__(self, name, quantity, weight, perishability):
        self.name = name
        self.quantity = quantity
        self.weight = weight
        self.perishability = perishability

    def __repr__(self):
        return f"Resource(name='{self.name}', quantity={self.quantity}, weight={self.weight}, perishability={self.perishability})"

    def to_dict(self):
        return {
            'name': self.name,
            'quantity': self.quantity,
            'weight': self.weight,
            'perishability': self.perishability
        }