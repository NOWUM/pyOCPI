# pyOCPI

Python Rest-Interface for OCPI built on Flask-RESTX, providing a OpenAPI interface


## install

`pip install -e .`

## configuration

the main.py is an example of how to use this project. The managers are meant to be understood as interfaces, which must be implemented according to the business logic which is not part of this module.

An example architecture would use a background job to schedule answers (for example for the commands module) while saving the data from the post/patch requests in a seperate database, which is used for communication between the background job and the Flask app.

## Roadmap

this should not be the last iteration of this concept. I think this could be a lot more user friendly and abstracted, so that the usage feels more like the communication of the ocpp python package, which does not need any knowledge of the underlying websockets at all.
