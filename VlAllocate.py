import pickle


class VLAllocate:
    def __init__(self, dc) -> None:
        self.dc = dc

    def get_bandwidth(self, path):
        weights = []
        for i in range(len(path) - 1):
            weights.append(self.dc.edge_weights[(path[i], path[i + 1])])
        return min(weights)

    def bandwidth(self, e):
        return e[1]

    def allocate(self, vdc_req, vm_allocation):
        allocation = dict()
        allocated = False
        for edge in vdc_req.__dict__["edge_weights"]:
            allocated = False
            weight = vdc_req.__dict__["edge_weights"][edge]
            paths = []
            self.dc.findPaths(
                str(vm_allocation[int(edge[0])]),
                str(vm_allocation[int(edge[1])]),
                [False] * self.dc.nodes,
                [],
                paths,
                weight,
            )

            paths_vdc = [
                [path, self.get_bandwidth(path)]
                for path in paths
                if self.dc.vl_allocated[tuple(path)]
            ]
            paths_vdc.sort(key=self.bandwidth)
            if len(paths_vdc) > 0:
                allocated = True
                allocation[edge] = paths_vdc[0][0]
                for i in range(len(paths_vdc[0][0]) - 1):
                    self.dc.edge_weights[
                        (paths_vdc[0][0][i], paths_vdc[0][0][i + 1])
                    ] -= weight

            if not allocated:
                paths_pp = [
                    [path, self.get_bandwidth(path)]
                    for path in paths
                    if not self.dc.vl_allocated[tuple(path)]
                ]
                paths_pp.sort(key=self.bandwidth)
                if len(paths_pp) > 0:
                    allocated = True
                    allocation[edge] = paths_pp[0][0]
                    for i in range(len(paths_pp[0][0]) - 1):
                        self.dc.edge_weights[
                            (paths_pp[0][0][i], paths_pp[0][0][i + 1])
                        ] -= weight

            if not allocated:
                return {"failure": True}
        return allocation
