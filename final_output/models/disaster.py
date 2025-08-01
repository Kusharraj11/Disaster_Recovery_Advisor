from typing import List
from .resource import Resource
from .personnel import Personnel
from .transportation import Transportation

class Disaster:
    def __init__(self, type, location, affected_population, duration_days, 
                 resources: List[Resource], personnel: List[Personnel], 
                 transportation: List[Transportation]):
        self.type = type
        self.location = location
        self.affected_population = affected_population
        self.duration_days = duration_days
        self.resources = resources
        self.personnel = personnel
        self.transportation = transportation

    def __repr__(self):
        return (f"Disaster(type='{self.type}', location='{self.location}', "
                f"affected_population={self.affected_population}, "
                f"duration_days={self.duration_days}, "
                f"resources={self.resources}, personnel={self.personnel}, "
                f"transportation={self.transportation})")

    def to_dict(self):
        return {
            'type': self.type,
            'location': self.location,
            'affected_population': self.affected_population,
            'duration_days': self.duration_days,
            'resources': [r.to_dict() for r in self.resources],
            'personnel': [p.to_dict() for p in self.personnel],
            'transportation': [t.to_dict() for t in self.transportation]
        }