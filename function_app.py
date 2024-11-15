import azure.functions as func
# from azure.identity import DefaultAzureCredential
# from azure.mgmt.resource import ResourceManagementClient
# import os
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="HttpExample", auth_level=func.AuthLevel.ANONYMOUS)
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

# @app.route(route="ResourceGroups", auth_level=func.AuthLevel.ANONYMOUS)
# def ResourceGroups(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     # Acquire a credential object.
#     credential = DefaultAzureCredential()

#     # Retrieve subscription ID from environment variable.
#     subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

#     # Obtain the management object for resources.
#     resource_client = ResourceManagementClient(credential, subscription_id)

#     # Retrieve the list of resource groups
#     group_list = resource_client.resource_groups.list()

#     # Show the groups in formatted output
#     column_width = 40

#     body = ""
#     for group in list(group_list):
#         body += f"{group.name:<{column_width}}{group.location}"

#     if group_list:
#         return func.HttpResponse(body)
#     else:
#         return func.HttpResponse(
#              "None",
#              status_code=404
#         )

# @app.route(route="VirtualNetworks", auth_level=func.AuthLevel.ANONYMOUS)
# def VirtualNetworks(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     try:
#         # Get the resource group from the query parameters or request body
#         resource_group_name = req.params.get('resourceGroup')
#         if not resource_group_name:
#             return func.HttpResponse(
#                 "Please pass the 'resourceGroup' parameter in the query string or request body",
#                 status_code=400
#             )
        
#         # Initialize the Azure SDK client with DefaultAzureCredential (which supports managed identity, environment variables, etc.)
#         credential = DefaultAzureCredential()
#         subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]  # Replace with your Azure Subscription ID
#         network_client = NetworkManagementClient(credential, subscription_id)

#         # List all VNets in the given resource group
#         vnets = network_client.virtual_networks.list(resource_group_name)
        
#         # Prepare the response data (list of VNets)
#         vnet_names = [vnet.name for vnet in vnets]

#         # Return the list of VNets as a JSON response
#         return func.HttpResponse(
#             body=str(vnet_names),
#             status_code=200,
#             mimetype="application/json"
#         )

#     except Exception as e:
#         logging.error(f"Error occurred: {str(e)}")
#         return func.HttpResponse(
#             f"An error occurred: {str(e)}",
#             status_code=500
#         )