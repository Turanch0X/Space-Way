import json

class JSON_Handler:
    def __init__(self, count):
        self.record = 0

    def read_json(self):
        with open('data.json', 'r') as file:
            data = json.load(file)
            self.record = data.get("Your record", 0)

    def write_json(self, count):
        if count > self.record:
            self.record = count
            with open('data.json', 'w') as file:
                json.dump({'Your record': self.record}, file)