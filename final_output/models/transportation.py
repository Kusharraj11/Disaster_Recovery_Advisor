class Transportation:
    def __init__(self, type, capacity, cost_per_km, availability):
        self.type = type
        self.capacity = capacity
        self.cost_per_km = cost_per_km
        self.availability = availability

    def __repr__(self):
        return f"Transportation(type='{self.type}', capacity={self.capacity}, cost_per_km={self.cost_per_km}, availability={self.availability})"

    def to_dict(self):
        return {
            'type': self.type,
            'capacity': self.capacity,
            'cost_per_km': self.cost_per_km,
            'availability': self.availability
        }