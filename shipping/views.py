from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from accounts.views import admin_check
from shipping.models import Shipping
from  django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import admin
import json
import requests
from json.decoder import JSONDecodeError
from shoponline.settings import EASYPARCEL_API_KEY





import pandas as pd
import csv, io, xlsxwriter
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, FileResponse

def shipping_data_toexcel_working(request):
    products =  Shipping.objects.filter(is_ordered=True)
    df = pd.DataFrame(list(products.values()))
    excel_file = io.BytesIO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df.to_excel(xlwriter, 'shipping.xlsx')
    xlwriter.close()
    #xlwriter.close()
    excel_file.seek(0)

    response = HttpResponse(excel_file.read(), content_type='application/ms-excel vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # set the file name in the Content-Disposition header
    response['Content-Disposition'] = 'attachment; filename=myfile.xls'
    return response 




def shipping_data_toexcel(request):
    # API endpoint URL
    url = "http://demo.connect.easyparcel.sg/?apikey=EP-KYEocfDkd"

    # API key
    # api_key = EASYPARCEL_API_KEY
    # api_key = 'pqU9cnjZOI'

    # Request headers
    headers = {
        "Content-Type": "application/json"
    }

    # Request payload (example data)
    payload = {
        "bulkData": [
            {
                'pick_code': '059893',
                'pick_country': 'SG',
                'send_code': '059897',
                'send_country': 'SG',
                'weight': '10',
                'width': '0',
                'length': '0',
                'height': '0',
                'date_coll': '2023-08-10',
            },
            {
                'pick_code': '059893',
                'pick_country': 'SG',
                'send_code': '059897',
                'send_country': 'SG',
                'weight': '10',
                'width': '0',
                'length': '0',
                'height': '0',
                'date_coll': '2023-08-10',
            }
            # Add more parcels as needed
        ]
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print('response is :', response)
    data = ''
    # Parse and print the response
    if response.status_code == 200:
    # daya
        try:
           
            qUserData = json.loads(response).decode('utf-8')
            questionSubjs = qUserData["all"]["questions"]
        except JSONDecodeError as e:
            print(f'json decode error,{e}')
        except TypeError as e:
             print("json decode error")

    # daya

    # if response.status_code == 200:
    #     data = response.json()
    else:
        print("Error:", response.status_code, response.text)

    return JsonResponse(data,safe=False)


import requests

def get_easyparcel_rates(sender_postcode, receiver_postcode, weight):
    url = "https://connect.easyparcel.sg/?ac=MPRateCheckingBulk"

    payload = {
        "api_key": EASYPARCEL_API_KEY,
        "api_secret":  '' ,
        "sender_postcode": sender_postcode,
        "receiver_postcode": receiver_postcode,
        "weight": weight,
        # Add more parameters as needed
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
from django.http import JsonResponse

def check_easyparcel_rates(request):
    if request.method == 'POST':
        sender_postcode = request.POST.get('sender_postcode')
        receiver_postcode = request.POST.get('receiver_postcode')
        weight = request.POST.get('weight')

        rates = get_easyparcel_rates(sender_postcode, receiver_postcode, weight)

        if rates:
            return JsonResponse({"rates": rates})
        else:
            return JsonResponse({"error": "Failed to retrieve rates"})
    else:
        return JsonResponse({"error": "Invalid request method"})