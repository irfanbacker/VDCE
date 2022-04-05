import pickle


class VMAllocate:
    def __init__(self, dc):
        self.dc = dc
        self.pn = [[i, dc.node_weights[i]] for i in dc.node_weights]

    def get_pn_vdc(self):
        return [
            [i, self.dc.node_weights[i]] for i, j in self.pn if self.dc.vm_allocated[i]
        ]

    def get_pn_rack(self, node):
        return [
            [i, self.dc.node_weights[i]]
            for i in self.pn
            if self.dc.node_rack[i[0]] == self.dc.node_rack[node[0]]
        ]

    def get_pn_edge(self, node):
        return [
            [i, self.dc.node_weights[i]]
            for i in self.pn
            if self.dc.edge_group[i[0]] == self.dc.edge_group[node[0]]
        ]

    def resource_available(self, node):
        return node[-1]

    def allocate(self, vdc_req):
        allocation = dict()
        for i in range(len(vdc_req)):
            pn_vdc = self.get_pn_vdc(self.pn, self.dc)
            pn_vdc.sort(key=self.resource_available)

            for j in range(len(pn_vdc)):
                if pn_vdc[j][1] >= vdc_req[i][1]:
                    self.dc.vm_allocated[pn_vdc[j][0]] = True
                    self.dc.node_weights[pn_vdc[j][0]] -= vdc_req[i][1]
                    self.pn[j][1] -= vdc_req[i][1]
                    allocation[vdc_req[i][0]] = pn_vdc[j][0]
                    self.pn.remove(pn_vdc[j])
                    break

            for j in pn_vdc:
                self.pn.remove(j)

            pn_rack = []
            for j in pn_vdc:
                pn_rack += self.get_pn_rack(j)
            pn_rack.sort(key=self.resource_available)

            for j in range(len(pn_rack)):
                if pn_rack[j][1] >= vdc_req[i][1]:
                    self.dc.vm_allocated[pn_vdc[j][0]] = True
                    self.dc.node_weights[pn_rack[j][0]] -= vdc_req[i][1]
                    self.pn[j][1] -= vdc_req[i][1]
                    allocation[vdc_req[i][0]] = pn_rack[j][0]
                    self.pn.remove(pn_rack[j])
                    break

            for j in pn_rack:
                self.pn.remove(j)

            pn_edge = []
            for j in pn_vdc:
                pn_edge += self.get_pn_edge(j)
            pn_edge.sort(key=self.resource_available)

            for j in range(len(pn_edge)):
                if pn_edge[j][1] >= vdc_req[i][1]:
                    self.dc.vm_allocated[pn_edge[j][0]] = True
                    self.dc.node_weights[pn_edge[j][0]] -= vdc_req[i][1]
                    self.pn[j][1] -= vdc_req[i][1]
                    allocation[vdc_req[i][0]] = pn_edge[j][0]
                    self.pn.remove(pn_edge[j])
                    break

            for j in pn_edge:
                self.pn.remove(j)

            self.pn.sort(key=self.resource_available)

            for j in range(len(self.pn)):
                if self.pn[j][1] >= vdc_req[i][1]:
                    self.dc.vm_allocated[self.pn[j][0]] = True
                    self.dc.node_weights[self.pn[j][0]] -= vdc_req[i][1]
                    self.pn[j][1] -= vdc_req[i][1]
                    allocation[vdc_req[i][0]] = self.pn[j][0]
                    break

        return allocation


if __name__ == "__main__":
    with open("DcAllocation.pickle", "rb") as handle:
        X = pickle.load(handle)

    with open("graphs.pickle", "rb") as handle:
        c = pickle.load(handle)

    dcs = c.get("substrates")
    vdc_reqs = c.get("vne_list")
    allocation = dict()
    Allocators = [VMAllocate(dcs[i]) for i in range(len(dcs))]
    for j in range(len(vdc_reqs)):
        allocation[j] = Allocators[X[j]].allocate(vdc_reqs[j])
    pickle_file = open("VmAllocation.pickle", "wb")
    pickle.dump(allocation, pickle_file)
