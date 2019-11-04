# APIs

These are very brittle service right now - there is no error checking or even exception handling

## Getting and Updating a firehazard value on a parcel

URL:  /parcel/firehazard/<id>

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
    
    
## Generating a Fire notify list

URL:  /notify/parcel-and-distance?parcelid=<parcelid>&dist=<integer distance in meters>

Response on success:
A JSON Array of Parcel Objects
A Parcel Object is a JSON Object, containing:
* parcelid
* any attributes we want to put in the table
* a WKT representation of the polygon geometry in EPSG 3857  
