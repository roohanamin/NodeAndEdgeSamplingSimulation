import random
from treelib import Node, Tree

#NODE SAMPLING ALGORITHM
#Marking procedure at router R:
    #for each packet w
        #let x be a random number form [0..1)
        #if x < p then,
            # write R into w.node

#Path reconstruction procedure at victim v:
    #let NodeTbl be a table of tuples (node,count)
    #for each packet w from attacker
        #z := lookup w.node in NodeTbl
        #if z != NIL then
            #increment z.count
        #else
            #insert tuple (w.node, 1) in NodeTbl
    #sort NodeTbl by count
    #extract path(R_i..R_j) from ordered node fields in NodeTbl

def nodeSamplingMarking(packet_list, p):
    print("Performing Node Sampling")
    for w in packet_list:
        x = random.uniform(0, 1)
        if x < p:
            w["node"] = "R"

def nodeSamplingPath(attacker_packets):
    NodeTbl = []
    for w in attacker_packets:
        z = next((item for item in NodeTbl if item[0] == w["node"]), None)
        if z:
            z[1] += 1
        else:
            NodeTbl.append([w["node"], 1])
    NodeTbl = sorted(NodeTbl, key=lambda x: x[1], reverse=True)
    path = [item[0] for item in NodeTbl]
    return path

#EDGE SAMPLING ALGORITHM
#Marking procedure at router R:
    #for each packet w
        #let x be a random number from [0..1)
        #if x < p then
            #write R into w.start and 0 into w.distance
        #else
            #if w.distance = 0 then
                #write R into w.end
            #increment w.distance
#Path reconstruction procedure at victim v:
    #let G be a tree with root v
    #let edges in G be tuples (start,end,distance)
    #for each packet w from attacker
        #if w.distance = 0 then
            #insert edge(w.start,v,0) into G
        #else
            #insert edge (w.start,w.end,w.distance) into G
    #remove any edge (x,y,d) with d != distance from x to v in G
    #extract path (R_i..R_j) by enumerating acyclic paths in G

def edgeSamplingMarking(packet_list, p):
    print("Performing Edge Sampling")
    for w in packet_list:
        x = random.uniform(0, 1)
        if x < p:
            w["node"] = "R"
        else:
            if w["distance"] == 0:
                w["end"] = "R"
            w["distance"] += 1

def edgeSamplingPath(attacker_packets):
    G = Tree()
    copyG = Tree()
    edges = ("start", "end", "distance")
    G.create_node("V", "v") #root node
    copyG.create_node("Start", "start")
    copyG.create_node("End", "end", parent = "start")
    copyG.create_node("Distance", "distance", parent = "start")
    for w in attacker_packets:
        if w["distance"] == 0:
            G.paste('start', copyG)
        else:
            G.paste('end', copyG)
    if edges["distance"] != "distance" in G:
        G.remove_node("start")
    path = G.show()
    return path

# #SCENARIO
# def scenario(numRouters, numBranches, numHops):
#     print("Creating Scenario")
#     networkTree = Tree()
#     networkTree.create_node("Victim", 0)
#     networkTree.create_node("Attacker1", 1, parent = 0)
#     networkTree.create_node("Attacker2", 2, parent = 0)
#     networkTree.show()

#SCENARIO
def scenario(numRouters, numBranches, numHops, numAttackers):
    print("Creating DDoS Scenario")
    networkTree = Tree()
    routAndattk = ["Router", "Attacker"]
    routerStr = "Router"
    routerNumbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
    attackerStr = "Attacker"
    attackerNumbers = ["0", "1", "2", "3", "4", "5"]
    numRouters = int(numRouters)
    numAttackers = int(numAttackers)
    numBranches = int(numBranches)
    pNode = 0 #Call to parent node for leaf
    print("Generating {} Routers and {} Branches with {} Hops and {} Attacker(s)".format(numRouters, numBranches, numHops, numAttackers))

    count = 0
    count2 = 0
    branchID = 0
    uniqueIDs = set()
    actualVal = numRouters - numBranches
    networkTree.create_node("Victim", pNode) #root node
    
    # Create branches
    for i in range(numBranches):
        count += 1
        branchID = count
        networkTree.create_node("{}{}".format(routerStr, routerNumbers[branchID]), branchID, parent=pNode)
        uniqueIDs.add(branchID)
        # Create child routers for each branch
        for j in range(1, 4 + i):
            count += 1
            node_type = routerStr
            if numAttackers > 0:
                node_type = random.choice(routAndattk)
                if node_type == attackerStr:
                    numAttackers -= 1
            networkTree.create_node("{}{}".format(node_type, routerNumbers[count]), count, parent=branchID)

    networkTree.show()

def generatePacketList(numPackets, attackers, x):
    packetList = []
    for i in range(numPackets):
        packet = {
            "src": random.choice(attackers),
            "dst": x,
            "size": random.randint(1, 1000)
        }
        packetList.append(packet)
    return packetList


#MAIN
if __name__ == '__main__':
    routers = 20
    branches = 5
    hops = 15
    attackers = 0 #placeholder
    scenario(routers, branches, hops)
