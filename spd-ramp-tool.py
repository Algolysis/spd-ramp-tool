#!/usr/bin/env python3

#########################################################################################################################
#                                                                                                                       #
# Copyright (c) Algolysis Ltd                                                                                           #
# All rights reserved.                                                                                                  #
#                                                                                                                       #
#########################################################################################################################
#   Contact                                                                                                             #
# ---------------------------                                                                                           #
# This client is still under development and therefore we appreciate any feedback and bug reports.                      #
#                                                                                                                       #
#                   Contact: support@algolysis.com                                                                      #
#   Bugs & Feature requests: https://github.com/Algolysis/spd-ramp-tool/issues                                          #
#                                                                                                                       #
# You can always use our web form to contact us for any reason: https://www.algolysis.com/contact                       #
#                                                                                                                       #
# Thank you for using our tools!                                                                                        #
#                                                                                                                       #
#########################################################################################################################

import argparse
import os.path
import requests
import random
import string
import sys
import pprint
from urllib.parse import urlencode, quote_plus

######################################################################################################

DEBUG=False

######################################################################################################

def exception_handler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    if DEBUG:
        debug_hook(exception_type, exception, traceback)
    else:
        print("%s: %s" % (exception_type.__name__, exception))


if DEBUG:
    sys.tracebacklimit=0
    sys.excepthook = exception_handler

######################################################################################################

def upload_image(url, file_path, token):
    headers = {'Authorization': f'Bearer {token}'}
    with open(file_path, 'rb') as file:
        files = {'images[]': file}
        try:
            response = requests.post(url, files=files, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            print(f"\nError: Failed to connect to the URL '{url}': {str(e)}")
            return None
        
def upload_file(url, file_path, token):
    headers = {'Authorization': f'Bearer {token}'}
    with open(file_path, 'rb') as file:
        files = {'file': file}
        try:
            response = requests.post(url, files=files, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            print(f"\nError: Failed to connect to the URL '{url}': {str(e)}")
            return None
      

def register_model(url, model_path, token):
    # Check if the file exists
    if not os.path.isfile(model_path):
        print(f"\nError: Model File \"{model_path}\" not found.")
        return

    # Upload the file
    response = upload_file(url, model_path, token)

    if response:
        print(f"\n{response.json()}\n")
    else:
        print(f"\nError: Failed registering \"{model_path}\".")


def list_models(url, token):
    headers = {'Authorization': f'Bearer {token}'}
    # Upload the file[]
    try:
        response = requests.post(url, headers=headers)
        print('\n')
        print(response.json())
        print('\n')
    except requests.exceptions.RequestException as e:
        print(f"\nError: Failed to connect to the URL '{url}': {str(e)}")
        return None

    #if response:
    #    print(f"\n{response.json()}\n")
    #else:
    #    print(f"\nError: Failed registering \"{model_path}\".")
        

def predict(url, file_path, token, model):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"\nError: Input File \"{file_path}\" not found.")
        return

    payload = {
        'model': model, 
        'wait': "true"
    }
    
    url_with_args = url + "?" + urlencode(payload, quote_via=quote_plus)

    # Upload the file
    response = upload_image(url_with_args, file_path, token)

    if response:
        print(f"\n{response.json()}\n")
    else:
        print(f"\nError: Failed detecting for \"{file_path}\".")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SmartPartsDetector utility')
    parser.add_argument('--url', default='https://spd.algolysis.com:5000', help='URL of the SPD microservice.')
    parser.add_argument('--token', help='Bearer token for authentication.')
    parser.add_argument('--registerModel', help='Path to the model file to register in the SPD microservice.')
    parser.add_argument('--list-models', action='store_true', help='List available models for the specified token.')
    parser.add_argument('--predict', help='Object detection mode.')
    parser.add_argument('--model', help='Model to use for object detection')
    args = parser.parse_args()

    print("\nExecuting SPDML Tool in: " + os.getcwd())
    if args.url:
        print("   SPD Microservice URL: " + args.url)
    else:
        print("\nERROR: Please specify a valid SPD URL.")
        sys.exit()
    
    if args.token:
        print("           Bearer Token: " + args.token)
    else:
        print("\nERROR: Please specify a token.")
        sys.exit()

    if args.registerModel:
        print("             Model Path: " + args.registerModel)
        register_model(args.url + "/registerModel", args.registerModel, args.token)
    elif args.list_models:
        print("         Listing models: ")
        list_models(args.url + "/listModels", args.token)   
    elif args.predict:
        if args.model:
            print("   Detecting Objects in: " + args.predict)
            predict(args.url + "/detect", args.predict, args.token, args.model)
        else:
            print("\nERROR: Please specify a model for object detection.\nUse --list-models to see available models.")
            sys.exit()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

