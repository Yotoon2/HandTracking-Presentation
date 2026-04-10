class Parser:
    def __init__(self):
        self.acc = [0,0,0]
        self.gyro = [0,0,0]
        self.magneto = [0,0,0]
        self.flex = [0,0,0]
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.heading = 0

    def update(self, data):
        if "acc" in data:
            self.acc = data["acc"]
        if "gyro" in data:
            self.gyro = data["gyro"]
        if "magneto" in data:
            self.magneto = data["magneto"]
        if "flex" in data:
            self.flex = data["flex"]
        if "roll" in data:
            self.roll = data["roll"]
        if "pitch" in data:
            self.pitch = data["pitch"]
        if "yaw" in data:
            self.yaw = data["yaw"]
        if "heading" in data:
            self.heading = data["heading"]
