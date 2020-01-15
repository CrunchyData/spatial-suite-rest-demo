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

## Geocoding an Address

Just tack a string for a fully qualified address on the end of 
URL/geocode/<address>

http://rest-services-scfire.openshift-pousty-apps.gce-containers.crunchydata.com/geocode/400%20glen%20canyon%20road,%20santa%20cruz,%20ca,%2095060

response:
The coords are in 4326 and the parcelid is the parcel identifier for the 
closest parcel to that lat (y), lon (x)

```
{
  "lat": 37.007599341936,
  "lon": -122.009281462818,
  "parcelid": 70193
}
```