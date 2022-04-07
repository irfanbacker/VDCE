import pickle
from VlAllocate import VLAllocate
from graph_extraction import Extract
from DcAllocate import DCAllocate
from VmAllocate import VMAllocate

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


print("Allocating DCs ...")
with open("graphs.pickle", "rb") as handle:
    b = pickle.load(handle)

dcs = b.get("substrate")
vdc_reqs = b.get("vne_list")
DCAllocator = DCAllocate(dcs, vdc_reqs)
dc_allocation = DCAllocator.allocate()
pickle_file = open("DcAllocation.pickle", "wb")
pickle.dump(dc_allocation, pickle_file)
print("DC allocation done.")


print("Allocating VMs ...")
X = dc_allocation
vm_allocation = dict()
VMAllocators = [VMAllocate(dcs[i]) for i in range(len(dcs))]
for j in range(len(vdc_reqs)):
    vm_allocation[j] = VMAllocators[X[j]].allocate(vdc_reqs[j])
pickle_file = open("VmAllocation.pickle", "wb")
pickle.dump(vm_allocation, pickle_file)
print("VM allocation done.")


print("Allocating VLs ...")
vl_allocation = dict()
VLAllocators = [VLAllocate(dcs[i]) for i in range(len(dcs))]
for j in range(len(vdc_reqs)):
    if "failure" not in vm_allocation[j]:
        vl_allocation[j] = VLAllocators[X[j]].allocate(vdc_reqs[j], vm_allocation[j])
    else:
        vl_allocation[j] = {"failure": True}
print("VL Allocation done.")

print()
print("DC Allocation :")
for i in dc_allocation:
    print("VDC {} : DC {}".format(i, dc_allocation[i]))

print()
for i in range(len(vdc_reqs)):
    print("VDCE request", i + 1)
    print()
    print("VM Allocation :")
    for j in vm_allocation[i]:
        print(j, vm_allocation[i][j])

    print()
    print("VL Allocation :")
    for j in vl_allocation[i]:
        print(j, vl_allocation[i][j])
    print()
    print()
