class Personnel:
    def __init__(self, role, number, pay_rate, volunteer):
        self.role = role
        self.number = number
        self.pay_rate = pay_rate
        self.volunteer = volunteer

    def __repr__(self):
        return f"Personnel(role='{self.role}', number={self.number}, pay_rate={self.pay_rate}, volunteer={self.volunteer})"

    def to_dict(self):
        return {
            'role': self.role,
            'number': self.number,
            'pay_rate': self.pay_rate,
            'volunteer': self.volunteer
        }