import maya.cmds as cmds

mainWindow = None


def CreateWindow(windowName):
    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName)

    global mainWindow
    mainWindow = cmds.window(windowName, title=windowName)

    cmds.showWindow(mainWindow)
    return mainWindow


def getType():
    selection = cmds.ls(selection=True)
    typeSelection = []

    for i in selection:

        nodes = cmds.listRelatives(i, children=True, fullPath=True) or []

        if len(nodes) == 1:
            nodeType = nodes[0]
            typeObj = cmds.objectType(nodeType)
        else:
            typeObj = cmds.objectType(i)

        typeSelection.append(typeObj)

    return typeSelection


def getShape():
    selection = cmds.ls(selection=True, s=True, tr=True)
    shape = []
    for i in selection:
        shapeNode = cmds.listRelatives(i, children=True) or []
        shape.append(shapeNode[0])

    return shape


def scriptUI():
    editedWindow = CreateWindow("ScriptUI")
    cmds.window(editedWindow, edit=True, title="ScriptUI", widthHeight=(850, 250))
    intro = cmds.rowColumnLayout(nc=1, rs=[(1, 10), (2, 10)], rat=[(1, "top", 10), (2, "top", 10)], ro=[(1, "top", 20)],
                                 cal=[(1, "center")], columnWidth=[(1, 800)], cat=[(1, "both", 10)])
    cmds.text(label="Use the command CHANGE COLOR to change the color of the selected curve.")
    cmds.text(
        label="Use the command CHANGE CONTROL to change the shape of the selected control. \n \n IMPORTANT: DON'T FREEZE transformations of new object!!!")
    cmds.rowColumnLayout(p=intro, nc=3,
                         cal=[(1, "center"), (2, "left"), (3, "left")],
                         columnWidth=[(1, 140), (2, 450), (3, 1)],
                         co=[(1, "both", 1), (2, "both", 50), (3, "left", 1)],
                         cat=[(1, "both", 1), (2, "right", 10), (3, "left", 1)],
                         rs=[(1, 10), (2, 20)],
                         rat=[(1, "top", 30), (2, "top", 10)])

    cmds.textField('textField', tx="SELECT CONTROL CURVE", ed=False)

    def changeColor(*args):

        valueColorSlider = cmds.colorIndexSliderGrp(colorSlider, q=True, v=True)
        selection = cmds.ls(selection=True, s=True, tr=True)

        if len(selection) == 0 or len(selection) > 1:
            raise Exception("You must select 1 control curve")

        print selection[0]

        nodes = cmds.listRelatives(selection[0], children=True, fullPath=True) or []

        if len(nodes) == 1:
            nodeType = nodes[0]
            typeObj = cmds.objectType(nodeType)
        else:
            typeObj = cmds.objectType(selection[0])

        print typeObj
        print nodes

        if typeObj != "nurbsCurve":
            raise Exception("You must select A CURVE")

        cmds.setAttr(nodes[0] + ".overrideEnabled", 1)
        cmds.setAttr(nodes[0] + ".overrideColor", (valueColorSlider - 1))

    def changeShape(*args):

        selection = cmds.ls(selection=True)

        if len(selection) == 0 or len(selection) == 1 or len(selection) > 2:
            raise Exception("You must select 1 control curve and 1 new object")

        type = getType()
        typeCrv = type[0]
        typeObj = type[1]
        shape = getShape()
        shapeCrv = shape[0]
        shapeObj = shape[1]

        if typeCrv != "nurbsCurve" and typeObj != "mesh":
            raise Exception("You must select first a CONTROL CURVE")

        if typeObj != "mesh" and typeObj != "nurbsCurve":
            raise Exception("You must select a MESH or CURVE as new control")
            
        #'xform' to get the world space translate values
        
        positionAbsolute = cmds.xform(selection[0], q=True, rp=True)
        print positionAbsolute
        cmds.move(positionAbsolute[0], positionAbsolute[1], positionAbsolute[2], shapeObj, a=True)
        cmds.makeIdentity(selection[1], apply=True)
        cmds.parent(shapeObj, selection[0], s=True, r=True)
        cmds.parent(shapeCrv, s=True, rm=True)
        cmds.delete(selection[1])

    colorSlider = cmds.colorIndexSliderGrp(label='Select Color', min=0, max=32, v=0)

    cmds.button(label="Change color", width=220, c=changeColor)
    cmds.textField('textField2', tx="SELECT CONTROL", ed=False)
    cmds.textField('textField3', w=200, tx="SELECT A NEW OBJECT AS CONTROL", ed=False)
    cmds.button(label="Change control", width=220, c=changeShape)


scriptUI()
