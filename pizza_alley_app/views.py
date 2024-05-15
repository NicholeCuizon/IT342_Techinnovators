from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.template import loader

from pizza_alley_app.models import CurrentOrder, Products

# Create your views here.
# Cuizon
def landing(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render())

# Delgado
@csrf_exempt
def pizza_employeeOrder(request):
    if request.method == 'POST':
        if 'remove_item' in request.POST:
            currentid = request.POST.get('id')
            currentorder = CurrentOrder.objects.get(id=currentid)
            currentorder.delete()
 
            return redirect('pizza_employeeOrder')
 
        elif 'add_item' in request.POST:
            product_id = request.POST.get('product_id')
            quantitypost = request.POST.get('quantity')
 
            product = Products.objects.get(productID=product_id)
 
            order = CurrentOrder(productID=product_id,item=product.productName, quantity=quantitypost, price = product.price, total=product.price * int(quantitypost))
            order.save()
 
            return redirect('pizza_employeeOrder')
   
    else:  #Get request
        products = Products.objects.all()
        current_order = CurrentOrder.objects.all()  
        total = sum(order.total for order in current_order)
 
        return render(request, 'pizza_employeeOrder.html', {'products': products, 'current_order': current_order, 'total': total})
    
# <Next Member>