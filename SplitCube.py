import adsk.core, adsk.fusion, adsk.cam, traceback
app = adsk.core.Application.get()
ui  = app.userInterface
ui.messageBox('Split Cube')
objColl = adsk.core.ObjectCollection.create()
doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)        
design = app.activeProduct
rootComp = design.rootComponent
sketches = rootComp.sketches
xyPlane = rootComp.xYConstructionPlane
sketch = sketches.add(xyPlane)
circles = sketch.sketchCurves.sketchCircles
line = sketch.sketchCurves.sketchLines 

#Equivalent to a main method in java
def run(context):
    ui = None
    try:
        dist = 5
        draw_rect(-2,-2,0,4,4,0, dist)
        prof = sketch.profiles.item(0)       
        extrude(prof, dist)
        #biggest issue is with this line, maybe the split method is not being thought of in the right sense, like it should be something entirely different 
        #to make it work
        body = rootComp.features.extrudeFeatures.bodies.item(0)
        #ext = extrudes.add(extInput)
        #body = ext.bodies.item(0)
        split(body, dist)
            
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
                
# Draws the rectangle with the passed parameters
def draw_rect(x1, y1, z1, x2, y2, z2, dist):
    ui = None
    try:
        line.addTwoPointRectangle(adsk.core.Point3D.create(x1, y1, z1 + dist), adsk.core.Point3D.create(x2, y2, z2 + dist))      
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
#Extrudes the given profile to a given distance
def extrude(prof, dist):
    ui = None
    try:
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(dist)
        extInput.setDistanceExtent(True, distance)
        extrudes.add(extInput)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
      
#Splits a given body at a given distance
def split(body, distance):
    ui = None
    try:
        body = rootComp.features.extrudeFeatures.bodies(0)
        splitBodyFeats = rootComp.features.splitBodyFeatures            
        splitBodyInput = splitBodyFeats.createInput(body, rootComp.yZConstructionPlane, True)
        splitBodyInput2 = splitBodyFeats.createInput(body, rootComp.xZConstructionPlane, True)
        splitBodyFeats.add(splitBodyInput)
        splitBodyFeats.add(splitBodyInput2)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))            
            
            