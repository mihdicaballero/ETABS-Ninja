import comtypes.client
import comtypes.gen.ETABSv1
import sys


#create API helper object
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

def connect_to_etabs():
    """
    Return Values:
    SapModel (type cOAPI pointer)
    EtabsObject (type cOAPI pointer)
    """
    #attach to a running instance of ETABS
    try:
        #get the active ETABS object
        EtabsObject = helper.GetObject("CSI.ETABS.API.ETABSObject") 
    except (OSError, comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)
    #create SapModel object
    SapModel=EtabsObject.SapModel

    #setEtabsUnits()
    return SapModel,EtabsObject

def disconnect_from_etabs(etabs_object, sapmodel, close=False):
    if close:
        etabs_object.ApplicationExit(False)
    
    sapmodel = None
    etabs_object = None


def test_etabs_connection():
    try:
        # Connect to ETABS
        SapModel,etabsobject = connect_to_etabs()

        #refresh view, update (initialize) zoom
        ret = SapModel.View.RefreshView(0, False)

        print("ETABS connection test successful")

    except Exception as e:
        print(f"Error: {e}")
