import os
import pickle
import sys
import graph
from vne import create_vne


class Extract:
    def get_graphs(
        self,
        scenarioFileName="senario_RedBestel.pickle",
        min_nodes=3,
        max_nodes=6,
        energy_price=100,
    ):
        current = os.path.join(
            os.getcwd(),
            "P3_ALIB_MASTER",
            "input",
            scenarioFileName,
        )
        with open(current, "rb") as f:
            data = pickle.load(f)
        para = graph.Parameters(
            10000, 500000, 10000, 500000, 0, 100, 0, 100, 1, 1
        )  # Parameters for subsrate graph BW ,CRB, Location,Delay
        substrate = graph.Graph(
            len(data.scenario_list[0].substrate.nodes),
            data.scenario_list[0].substrate.edges,
            energy_price,
            para,
        )
        vne_req = create_vne(min_nodes=min_nodes, max_nodes=max_nodes)
        return substrate, vne_req


if __name__ == "__main__":
    x = Extract()
    scenarios = [
        "senario_RedBestel.pickle",
        "senario_HurricaneElectric.pickle",
        "senario_Karen.pickle",
    ]
    substrates = []
    vne_list = []
    for scenario in scenarios:
        substrate, vne_req = x.get_graphs(scenario)
        substrates.append(substrate)
        vne_list.append(vne_req)
    output = {"substrate": substrates, "vne_list": vne_list}
    pickle_file = open("graphs.pickle", "wb")
    pickle.dump(output, pickle_file)
