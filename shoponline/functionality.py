
free delivery details for every brand

7 days return to seller

base_shipping_rate = 3

base_shipping_cost = book_quantity * base_shipping_rate

#apply shipping rate based on total no of books
if book_count >= 16:
    discount_multiplier = 0
elif book_count in range(11,16):
    discount_multiplier = 0.25
elif book_count in range(5,11):
    discount_multiplier = 0.5
elif book_count in range(2,5):
    discount_multiplier = 0.75
else:
    discount_multiplier = 1

discounted_shipping_cost = base_shipping_cost * discount_multiplier


add shipping_cose field in orders

weight


8************************************************************************************************************

"{\"is_invoice_created\":true,
\"invoice_url\":\"https:\/\/s3-ap-south-1.amazonaws.com\/kr-shipmultichannel-mum\/3116291\/invoices\/Retail000058ba9b309-c4bd-4c06-ba15-2cc76b7c5d1f.pdf\",
\"not_created\":[],\"irn_no\":\"\"}"
when I try to access above URL get - Access-Denied

This XML file does not appear to have any style information associated with it. The document tree is shown below.
<Error>
<Code>AccessDenied</Code>
<Message>Access Denied</Message>
<RequestId>94ARWRYHGSBEZEH1</RequestId>
<HostId>j32LvksmWatylm3TdFGYuJ1qvBwJ39Lj+qIbbQ3CC7AEcrgHnOYGd9fDocMeEwDD4GpzjXQLQhg=</HostId>
</Error>
This is the way I want the url to be

https://s3-ap-south-1.amazonaws.com/kr-shipmultichannel-mum/3116291/invoices/Retail000058ba9b309-c4bd-4c06-ba15-2cc76b7c5d1f.pdf
When I remove the slashed I get in Response I'm able to download the PDF and that's done manually. So how do I get working URL.

#Views.py

class GenerateInvoice(APIView):lfkioooooooooooooooooooooooooooooppppppppppppppppppppppppppp[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

    def post(self, request):
        order_id = request.query_params.get("ids", None)
        print(order_id)
        data = json.dumps({"ids": [order_id]})
        headers = {
            "Content-Type": "application/json",
            "Authorization": settings.SHIPROCKET_TOKEN,
        }
        url = "https://apiv2.shiprocket.in/v1/external/orders/print/invoice"

        response = requests.post(url=url, data=data, headers=headers)

        return Response(response)

#**************************************************** get data from other api and save in django

from django.shortcuts import  render
from meal_app.models import Meal
import requests

def get_meals(request):
    all_meals = {}
    if 'name' in request.GET:
        name = request.GET['name']
        url = 'https://www.themealdb.com/api/json/v1/1/search.php?s=%s' % name
        response = requests.get(url)
        data = response.json()
        meals = data['meals']

        for i in meals:
            meal_data = Meal(
                name = i['strMeal'],
                category = i['strCategory'],
                instructions = i['strInstructions'],
                region = i['strArea'],
                slug = i['idMeal'],
                image_url = i['strMealThumb']
            )
            meal_data.save()
            all_meals = Meal.objects.all().order_by('-id')

    return render (request, 'meals/meal.html', { "all_meals": 
    all_meals} )

    #populate in template

    {% extends 'meals/base.html'%}
{% load static %}
{% block content %}
  <div class = "container">
    <div class = "text-center container">
      <br>
      <h2 class = "text-center">Search for your favorite Meals</h2> 
      <br>
      <form method="GET">
        <input type = "text" name = "name" placeholder="Search..." class = "text-center">
        <button type = "submit" class = "btn-danger btn-sm">SEARCH MEAL</button>
      </form> 
    </div> 
    <br><br>
    <div class="row">
      {% for meal in all_meals %}
        <div class="col-md-4 col-sm-6 col-lg-3">
          <div class="card">
            <img class="card-img-top" src="{{ meal.image_url }}" alt="Card image cap">
            <div class="card-body text-center">
              <p class="card-title">{{ meal.name }}</p>
              <hr>
              <p class="card-text">{{ meal.region }}</p>
              <a href="/meals/{{meal.id}}"
              ><input
                type="submit"
                value="Learn More"
                class="btn btn-danger btn-sm"
                type="button"
            /></a>
            </div>
          </div>
          <br><br><br>
        </div>
      {% endfor %}
    </div>
  </div>
{% endblock %}


### export data into csv from django

from myapp.models import Employee import csv  
def getfile(request):  
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="file.csv"'  
    employees = Employee.objects.all()  
    writer = csv.writer(response)  
    for employee in employees:  
        writer.writerow([employee.eid,employee.ename,employee.econtact])  
    return response  


#send data from application to third party app

@api_view(['POST'])
def cashfree_request(request):                
    if request.method == 'POST':    
        data=request.POST.dict()
        print(data)
        payment_gateway_order_identifier= data['orderId'] 
        amount = data['orderAmount']
       
        order=Orders.objects.get(payment_gateway_order_identifier=payment_gateway_order_identifier)
        payment = Payments(orders=order,amount=amount,)
        payment.save()
 
        URL = "" # external application url where webhook needs to send

        request_data ={
                       order:{
                       'id':order.id,
                       'payment_collection_status': transaction_status,
                       'payment_collection_message': transaction_message
                                         }
                                   }
         json_data = json.dumps(request_data)
         response = requests.post(url = URL, data = json_data)
         return Response(status=status.HTTP_200_OK


# send data from webapp post data to third party
import urllib2

urllib2.urlopen('http://example.com', 'a=1&b=2')
# above code will send a post request to http://example.com, with parameters a=1 and b=2

#There is another way using python famous library Requests

import requests

data = {
  "username": "user",
  "password": "pass",
}

URL = 'http://example.com'
r = requests.post(URL, data=data)

#other way is

def upload(request):
    if request.method == 'POST':
        url=settings.WEBSERVICES_URL+'validate'
        r = requests.post('http://localhost:9090/validate', data=request.POST)
        r2 = requests.get('http://localhost:9090/test')
        return render_to_response("upload.html", context_instance=RequestContext(request))
    else:
        return render_to_response("upload.html", context_instance=RequestContext(request))


#If you want to post data outside of your app, you can take a look to HTTP library Requests

import requests

driver_firstname = request.POST['driver_firstname']
driver_lastname = request.POST['driver_lastname']
driver_email = request.POST['driver_email']

payload = {'driver.driver_firstname': driver_firstname,
           'driver.driver_lastname': driver_lastname,
           'driver.driver_email': driver_email
           }

r = requests.post("http://your-url.org/post", data=payload)

#through ajax

$.ajax({
    type: "POST",
    url: "/post/{{post.id}}/vote/1",
    success: function(){
        //Do something here that lets the user know things worked out
    }
});