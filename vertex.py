class Vertex:

    def __init__(self, id_, k_="5001"):
        self.id = id_
        self.in_vertexes = []
        self.out_vertexes = []
        self.k = k_
        self.rc_id = (self.id // 4) * 4 + 3 - (self.id % 4)

    def __str__(self):
        return str(self.id)
        # return str(self.id) + " in: " +str(self.in_vertexes) + " out: " +str(self.out_vertexes)

    def __repr__(self):
        return str(self.id)

    def add_in(self, in_id):
        self.in_vertexes.add(in_id)

    def add_out(self, out_id):
        self.out_vertexes.add(out_id)
