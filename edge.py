class Edge:
    from_v = ""
    to_v = ""
    id = ""

    def __init__(self, id_, from_, to_, seq_):
        self.id = id_
        self.from_v = from_
        self.to_v = to_
        self.seq = seq_
        self.reads = set()
        self.label = str(self.get_external_id()) + self.get_orientation()

    def get_orientation(self):
        if self.id % 2 == 0:
            return "+"
        else:
            return "-"

    def get_external_id(self):
        return self.id // 2

    def length(self):
        return len(self.seq)

    def get_rc_id(self):
        return (self.id // 2) * 2 + (self.id % 2 + 1) % 2

    def __str__(self):
        return "(" + str(self.from_v) + ", " + str(self.to_v) + ")"

    def __repr__(self):
        return "(" + str(self.from_v) + ", " + str(self.to_v) + ")"


