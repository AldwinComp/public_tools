all_dependencies=[]
end_message="Nothing to Clean"
### Selection Mode Checker #####

if len(nuke.selectedNodes()) >1:
    Check = True
    nodes = nuke.selectedNodes()
else:
    nodes=nuke.allNodes()
    Check = False
    
##List of usefull Nodes ####

if not nuke.thisNode()["sources"].value():
    exeption=["Write","Read", "StickyNote", "ReadGeo2", "Camera2", "Group", "BackdropNode"]
else:
    exeption=["Write","BackdropNode"]




##Delete all the Disable nodes  #####

if nuke.thisNode()["Disable"].value():
    for i in nodes:
        try:
            if i["disable"].value():
                if i.Class() =="Write" and i.dependencies():
                    None
                else:
                    nuke.delete(i)
                    end_message="Clean!"
                        

            if i.Class()=="Read" and i.error():
                nuke.delete(i)
                end_message="Clean!"
        except:
            None
            
            
##List of usefull alone Nodes ####

if len(nuke.selectedNodes()) >1:
    Check = True
    nodes = nuke.selectedNodes()
else:
    nodes=nuke.allNodes()
    Check = False
    
    


alone_node_protection=[]

for i in nodes:
    for j in i.dependencies():
        all_dependencies.append(j)
for i in nodes:
    if not i.dependencies() and i not in all_dependencies:
        if i.Class() in exeption:
            alone_node_protection.append(i)

            
##Delete viewer nodes inside of groups  #####

for i in nuke.allNodes():
    if i.Class() == "Group":
        for j in nuke.allNodes(group = i):
            if j.Class() == "Viewer":
                nuke.delete(j)
                end_message="Clean!"
    if nuke.thisNode()["viewers"].value() == True and i.Class() == "Viewer":
        nuke.delete(i)
        end_message="Clean!"


## Variable prep   

if nuke.thisNode()["unusefull"].value():
    bad_nodes=[0]
else:
    bad_nodes=[]
    
selected_nodes=nuke.selectedNodes()




##Main code #########

while bad_nodes:
    working_nodes=[nuke.thisNode()]
    all_nodes=[]
    bad_nodes=[]

    for i in nuke.allNodes():
        all_nodes.append(i)
        for j in i.dependencies(): ## make a list of node in use by other nodes
            if j not in working_nodes:
                working_nodes.append(j)
        if i.Class() == "Write" or i.Class() == "Viewer" or i in alone_node_protection: ## check if the "unused" node is either a Write or in the protected list - if YES count as a usefull node
            working_nodes.append(i)
        
    ## Substract all the (selected) nodes by the nodes in use by other node to fid the node that are not used anywhere
    if Check == True:
        bad_nodes = (set(all_nodes) - set(working_nodes))-(set(all_nodes) - set(selected_nodes))
    else:
        bad_nodes = (set(all_nodes) - set(working_nodes))
        
    ## delete the none usefull nodes
    if bad_nodes:
        for i in bad_nodes:
            nuke.delete(i)
            end_message="Clean!"


if len(nuke.selectedNodes()) >1:
    nodes = nuke.selectedNodes()
else:
    nodes=nuke.allNodes()


for a in nodes:
    if a.Class()== "BackdropNode":
        check = True
        for j in a.getNodes():
            if j.Class() != "Dot":
                check = False
        if check:
            nuke.delete(a)
            end_message="Clean!"
            
            
print (end_message)
