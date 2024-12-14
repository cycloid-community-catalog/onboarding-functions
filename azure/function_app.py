import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
import os
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="ResourceGroups", auth_level=func.AuthLevel.ANONYMOUS)
def ResourceGroups(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('ResourceGroups function triggered and processing a request.')

    try:
        # Get the location from the query parameters or request body
        location = req.params.get('location')
        if not location:
            return func.HttpResponse(
                "Please pass the 'location' parameter in the query string or request body",
                status_code=400
            )
        
        # Acquire a credential object.
        credential = DefaultAzureCredential()

        # Retrieve subscription ID from environment variable.
        subscription_id = os.environ.get("SUBSCRIPTION_ID", None)

        # Obtain the management object for resources.
        resource_client = ResourceManagementClient(credential, subscription_id)

        # Retrieve the list of resource groups
        groups = resource_client.resource_groups.list($filter=f"location eq '{location}'")

        response = []
        for group in groups:
            response.append(json.loads('{"label": "'+group.name+' ('+group.location+')","value": "'+group.name+'"}'))

        return func.HttpResponse(
            body=json.dumps(response),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )

@app.route(route="VirtualNetworks", auth_level=func.AuthLevel.ANONYMOUS)
def VirtualNetworks(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('VirtualNetworks function triggered and processing a request.')

    try:
        # Get the location from the query parameters or request body
        location = req.params.get('location')
        if not location:
            return func.HttpResponse(
                "Please pass the 'location' parameter in the query string or request body",
                status_code=400
            )
        
        # Get the resource group from the query parameters or request body
        resource_group_name = req.params.get('resourceGroupName')
        if not resource_group_name:
            return func.HttpResponse(
                "Please pass the 'resourceGroupName' parameter in the query string or request body",
                status_code=400
            )
        
        # Initialize the Azure SDK client with DefaultAzureCredential (which supports managed identity, environment variables, etc.)
        credential = DefaultAzureCredential()

        # Retrieve subscription ID from environment variable.
        subscription_id = os.environ.get("SUBSCRIPTION_ID", None)
        
        # Obtain the management object for resources.
        network_client = NetworkManagementClient(credential, subscription_id)

        # List all VNets in the given resource group
        vnets = network_client.virtual_networks.list(resource_group_name, filter=f"location eq '{location}'")
        
        response = []
        for vnet in vnets:
            response.append(json.loads('{"label": "'+vnet.name+' ('+vnet.location+')","value": "'+vnet.name+'"}'))

        return func.HttpResponse(
            body=json.dumps(response),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )

@app.route(route="Subnets", auth_level=func.AuthLevel.ANONYMOUS)
def Subnets(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Subnets function triggered and processing a request.')

    try:
        # Get the resource group from the query parameters or request body
        resource_group_name = req.params.get('resourceGroupName')
        if not resource_group_name:
            return func.HttpResponse(
                "Please pass the 'resourceGroupName' parameter in the query string or request body",
                status_code=400
            )
        
        vnet_name = req.params.get('vnetName')
        if not vnet_name:
            return func.HttpResponse(
                "Please pass the 'vnetName' parameter in the query string or request body",
                status_code=400
            )
        
        # Initialize the Azure SDK client with DefaultAzureCredential (which supports managed identity, environment variables, etc.)
        credential = DefaultAzureCredential()

        # Retrieve subscription ID from environment variable.
        subscription_id = os.environ.get("SUBSCRIPTION_ID", None)
        
        # Obtain the management object for resources.
        network_client = NetworkManagementClient(credential, subscription_id)

        # List all VNets in the given resource group
        subnets = network_client.subnets.list(resource_group_name, vnet_name)
        
        response = []
        for subnet in subnets:
            response.append(json.loads('{"label": "'+subnet.name+' ('+subnet.address_prefix+')","value": "'+subnet.name+'"}'))

        return func.HttpResponse(
            body=json.dumps(response),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )
