import adsk.core, adsk.fusion, adsk.cam, traceback
app = adsk.core.Application.get()
ui  = app.userInterface
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
        dist = user_input('Enter a distance', 'Distance')
        draw_rect(-2,-2,0,4,4,0, dist)
        prof = sketch.profiles.item(0)  
        ext = extrude(prof, dist)
        plane_value = user_input('Enter a positive value to split on the XZ plane, or a negative value for the YZ plane', 'Value')
        if plane_value > 0:
            planes = rootComp.xZConstructionPlane
        else:
            planes = rootComp.yZConstructionPlane
        planes = rootComp.constructionPlanes
        planeInput = planes.createInput()
        dist = user_input('Enter a distance like "5.0" or "3.0"', 'Distance')
        planeOne = offset(planes, planeInput, prof, dist)            
            
        split(ext, dist, plane_value, planeOne)
            
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
        ext = extrudes.add(extInput)
        return ext
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
      
#Splits a given body at a given distance
def split(ext, distance, plane_value, planeOne):
    ui = None
    try:
        body = ext.bodies.item(0)
        splitBodyFeats = rootComp.features.splitBodyFeatures            
        splitBodyInput = splitBodyFeats.createInput(body, planeOne, True)
        splitBodyFeats.add(splitBodyInput)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))            
            

#This function will create an offset plane (Goal is to use this as a helper method for the split function)
def offset(planes, planeInput, prof, dist):
    ui = None
    try:
        offsetDistance = float(dist)
        offsetValue = adsk.core.ValueInput.createByReal(offsetDistance)
        planeInput.setByOffset(prof, offsetValue)
        planeOne = planes.add(planeInput)        
        return planeOne
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))    

def user_input(prompt, value):
    ui = None
    try:
        '''
        #has an issue that the input value does not update between so that is something to look at (Just uses the initial value for the return)
        app = adsk.core.Application.get()
        ui  = app.userInterface
        input = '1'
        addCommandInput(prompt, value, input)
        #input = int(input)
        return input        
        '''
        #has an issue that the input value does not update between so that is something to look at (Just uses the initial value for the return)
        app = adsk.core.Application.get()
        ui  = app.userInterface
        inputValue = '4'
        output = ui.inputBox(prompt, value, inputValue)
        output_string = output[0]        
        return int(output_string)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            