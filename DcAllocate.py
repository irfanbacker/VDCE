import pickle


class DCAllocate:
    def __init__(self, dcs, vdc_reqs):
        self.dcs = dcs
        self.vdc_reqs = vdc_reqs

    def allocate(self):
        X = dict()
        for j in range(len(self.vdc_reqs)):
            X[j] = j%len(self.dcs)
        return X


if __name__ == "__main__":

    with open("graphs.pickle", "rb") as handle:
        b = pickle.load(handle)

    dcs = b.get("substrates")
    vdc_reqs = b.get("vne_list")
    Allocator = DCAllocate(dcs, vdc_reqs)
    allocation = Allocator.allocate()
    pickle_file = open("DcAllocation.pickle", "wb")
    pickle.dump(allocation, pickle_file)
