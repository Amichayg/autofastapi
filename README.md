# functionalapi

a tool used for auto deploying an api from a preexisting module.
this strips the need of tayloring for deployability, with the actual api being built automatically, with docs. 

This enables the user to write modules that expose databases or local system functions and then deploy them as api's. 

Usage currently is to place all files that will be imported as "*source.py" in the buildapi dir, then executing `uvicorn make_api:app` to deploy the app.
The next phases are to enable similar client for python, such as that a "virtual" module will be importable, creating functions with the exact signatures/docs as the deployed module, with function calls actually calling the apis. 

