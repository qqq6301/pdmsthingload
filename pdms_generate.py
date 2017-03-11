# -*- coding: utf-8 -*-
import json

#Location Hierarchy 
PlantAHierarchy={'extid':'EXT-P1','complexs':['C4','C5','C6'],'units':['U1','U2','U3'],'assets':['A1'],'locations':['L1','L2','L3','L4','L5']}
PlantBHierarchy={'extid':'EXT-P2','complexs':['C1','C2','C3'],'units':['U4','U5','U6'],'assets':['A1'],'locations':['L1','L2','L3','L4','L5']}
PlantCHierarchy={'extid':'EXT-P3','complexs':['CA','CB','CC'],'units':['U4','U5','U6'],'assets':['A1'],'locations':['L1','L2','L3','L4','L5']}
PlantAHierarchyNames={'name':'Eagle Ford Field','complexs':['North Field','South Field','West Field'],'units':['Well Cluster 1','Well Cluster 2','Well Cluster 3'],'assets':['Centrifugal Pump'],'locations':['Location 1','Location 2','Location 3','Location 4','Location 5']}
PlantBHierarchyNames={'name':'New Orleans Refinery','complexs':['Complex 1','Complex 2','Complex 3'],'units':['Vacuum Distillatio','Hydrocracker','Coker'],'assets':['Centrifugal Pump'],'locations':['Location 1','Location 2','Location 3','Location 4','Location 5']}
PlantCHierarchyNames={'name':'Houston Refinery','complexs':['Complex A','Complex B','Complex C'],'units':['Vacuum Distillatio','Hydrocracker','Coker'],'assets':['Centrifugal Pump'],'locations':['Location 1','Location 2','Location 3','Location 4','Location 5']}
PlantHierarchy=[PlantAHierarchy,PlantBHierarchy,PlantCHierarchy]
PlantHierarchyNames=[PlantAHierarchyNames,PlantBHierarchyNames,PlantCHierarchyNames]

# description attrubite 
class Description:
    en=""
    def __init__(self,en):
        self.en=en
        
#thingtype mapping to get full name of thingtype
def thingTypeMapping(thingType):
    if thingType in ['Plant','Complex','Unit','AbstractAssetType','Location']:
        return "com.sap.pdms.assets.functionalLocations:"+thingType
    else:
        return "com.sap.pdms.assets.pumps:"+thingType
                            
#thingType attrubite        
def constructthingType(thingType):
    thingTypes=[]
    thingTypes.append(thingTypeMapping(thingType))
    return thingTypes   
                                                  
class Thing(object):  
    _externalId = ""
    _name=""
    _description=Description("")
    _thingType=constructthingType("")

    # The class "constructor" - It's actually an initializer 
    def __init__(self, _externalId,_name,_description,_thingType):
        self._externalId = _externalId
        self._name = _name
        self._description = Description(_description)
        self._thingType=constructthingType(_thingType)
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)    

def GetThing(_externalId,_name,_description,_thingType):
    thing01=Thing(_externalId,_name,_description,_thingType)
    return thing01
       
def getAllPlants():
    ThingType="Plant"
    plantsOut=[]
    numberOfPlants=len(PlantHierarchy)
    for i in range(0,numberOfPlants):
        plant=PlantHierarchy[i]
        plantNames=PlantHierarchyNames[i]
        plantsOut.append(GetThing(plant['extid'],plantNames['name'],plantNames['name']+" (TD-en)",ThingType))
    return plantsOut 
    
def getAllComplexs():
    ThingType="Complex"
    complexsOut=[]
    numberOfPlants=len(PlantHierarchy)
    for i in range(0,numberOfPlants):
        plant=PlantHierarchy[i]
        plantNames=PlantHierarchyNames[i]
        complexs=plant['complexs']
        complexsNames=plantNames['complexs']
        for j in range(0,len(complexs)):
            complexsOut.append(GetThing(plant['extid']+'-'+complexs[j],complexsNames[j],complexsNames[j]+" (TD-en)",ThingType))        
    return complexsOut
      
def getAllUnits():
    ThingType="Unit"
    unitsOut=[]
    numberOfPlants=len(PlantHierarchy)
    for i in range(0,numberOfPlants):
        plant=PlantHierarchy[i]
        plantNames=PlantHierarchyNames[i]
        complexs=plant['complexs']
        units=plant['units']
        unitNames=plantNames['units']
        for j in range(0,len(complexs)):
            for k in range(0,len(units)):
                unitsOut.append(GetThing(plant['extid']+'-'+complexs[j]+'-'+units[k],unitNames[j],unitNames[j]+" (TD-en)",ThingType))        
    return unitsOut
    
def getAllAbstrctAssets():
    ThingType="AbstractAssetType"
    AbstractAssetsOut=[]
    numberOfPlants=len(PlantHierarchy)
    for i in range(0,numberOfPlants):
        plant=PlantHierarchy[i]
        plantNames=PlantHierarchyNames[i]
        complexs=plant['complexs']
        units=plant['units']
        assets=plant['assets']
        assetNames=plantNames['assets']
        for j in range(0,len(complexs)):
            for k in range(0,len(units)):
                for m in range(0,len(assets)):
                    AbstractAssetsOut.append(GetThing(plant['extid']+'-'+complexs[j]+'-'+units[k]+'-'+assets[m],assetNames[m],assetNames[m]+" (TD-en)",ThingType))
    return AbstractAssetsOut
    
def getAllLocations():
    ThingType="Location"
    LocationsOut=[]
    numberOfPlants=len(PlantHierarchy)
    for i in range(0,numberOfPlants):
        plant=PlantHierarchy[i]
        plantNames=PlantHierarchyNames[i]
        complexs=plant['complexs']
        units=plant['units']
        assets=plant['assets']
        locations=plant['locations']
        locationNames=plantNames['locations']
        for j in range(0,len(complexs)):
            for k in range(0,len(units)):
                for m in range(0,len(assets)):
                    for p in range(0,len(locations)):
                        LocationsOut.append(GetThing(plant['extid']+'-'+complexs[j]+'-'+units[k]+'-'+assets[m]+'-'+locations[p],locationNames[p],locationNames[p]+" (TD-en)",ThingType))
    return LocationsOut
   
def getAllThings():
    result=[]
    result=result+getAllPlants()+getAllComplexs()+getAllUnits()+getAllAbstrctAssets()+getAllLocations()
    #convert class instance to json 
    result=[thing.toJSON() for thing in result]
    return result    