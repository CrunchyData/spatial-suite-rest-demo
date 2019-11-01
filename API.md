#APIs


## Getting and Updating a firehazard value on a parcel

This is a very brittle service right now - there is no error checking or even exception handling

URL: /parcel/firehazard/<id>
Our URL right now:  http://rest-services-scfire.openshift-pousty-apps.gce-containers.crunchydata.com/parcel/firehazard/<id>

### Getting a value for a parcel
    HTTP Method: GET
    
    Expected Payload: NONE    
    
    Response on success:
    {
      "firehazard": "<current value>",
      "parcelid": <id of the parcel requested>
    }
    
    Response on anything else:
    an error as of now


### Updating a value for a parcel  
    HTTP Method: PUT

    Expected Payload:
    { "firehazard": "No"}
    
    Response on success:
    {"result":"success"}
    
    Response on anything else:
    an error as of now
    
