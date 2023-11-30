import re

def TransformGeoInvert():
    nodes = nuke.selectedNodes()
    knobs=["translate","rotate"]
    
    for knob in knobs:
        for node in nodes:
            if node.Class()=="TransformGeo" or node.Class()=="GeoTransform":
                #if node[knob].hasExpression():
                i=0
                for a in re.findall(r'\{(.*?)\}', node[knob].toScript()):
                
                    ##check if curve or expression linked
                    if "curve" in a:
                        b="curve"
                    else:
                        b=a
                    
                    ## check if already inverted
                    if "*-1" in a:
                        c= b.replace("*-1","")
                        node[knob].setExpression(c)
                    
                        node["xform_order"].setValue("SRT")
                        node["rot_order"].setValue("XYZ")
                    
                        node["label"].setValue("")
                    else:
                        node[knob].setExpression(b+"*-1")
                    
                        node["xform_order"].setValue("TRS")
                        node["rot_order"].setValue("ZYX")
                    
                        node["label"].setValue("INVERTED")
                    i+=1

TransformGeoInvert()
