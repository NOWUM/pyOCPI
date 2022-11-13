# pyOCPI

Python Rest-Interface for OCPI (2.2) built on Flask-RESTX, providing a OpenAPI interface.

Talking about OCPI, many Charge Point Operators (CPO) and e-Mobility Service Providers (eMSP) implement their own code to integrate OCPI into their software.
This is a very tedious way, as the protocol is very complex it is not needed that every entity implements it on their own.

To reduce reimplementation, an academic implementation is provided here, which furthermore allows to integrate with a new RESERVATIONS endpoint, if needed.

Currently, the only other public Python Implementation can be found here:
https://github.com/TECHS-Technological-Solutions/ocpi/

The Documentation of OCPI can be found here:
https://github.com/ocpi/ocpi/

## Install Instructions

`pip install pyocpi`

or after cloning the repository, one can run `pip install -e .` to work locally with the package.

## Package information

```
pyocpi
├── exceptions.py
├── __init__.py
├── managers.py # <- contains stubs which have to be inherited and implemented
├── models      # <- contains JSON Schemas in Flask-RestX
└── namespaces  # <- contains REST Endpoint Descriptions
```

## Configuration

`main.py` contains an example of how to use this project.
The managers are meant to be understood as interfaces, which must be implemented according to the business logic which is not part of this communications module.

An example architecture would use a background job to schedule answers (for example for the commands module) while saving the data from the post/patch requests in a seperate database, which is used for communication between the background job and the Flask app.

## Roadmap

This will not be the last iteration of this concept.
I think this could be a lot more user friendly and abstracted, so that the usage feels more like the communication of the ocpp python package, which does not need any knowledge of the underlying websockets at all.
Yet it is a good approach and is already greatly configurable.

