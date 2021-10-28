from django.http import HttpResponse
from django.core import serializers

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

import datetime
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
now = datetime.datetime.today().strftime("%Y-%m-%d")


def index(request):
    
    request.session['current_page']=''
    if not 'amount' in request.session:
        request.session['amount']={}
    if not 'cart' in request.session:
        request.session['cart'] = 0
    
    
    if not 'customer_id' in request.session:
        customer = ''
        first_customer = '' 
        last_customer = ''
        
                 
    else:
        customer = Customer.objects.get(id=request.session['customer_id'])
        first_customer = customer.customer_first_name
        last_customer = customer.customer_last_name

    length=request.session['cart']
    
    

    # item_name =Item.item_name
   # item = Item.objects.all()
    item = Item.objects.order_by('-created_at')[:10]
    #item_name = Item.objects.get(item_name)
    # item_price = Item.item_price
    # latest_item_list = Item.objects.order_by('created_at')[:5]
    #latest_item_list = Item.objects
    context = {
        'customer': customer, 
          
        'length' : length,
        'first':first_customer,
        'last':last_customer,
        #'latest_item_list' : latest_item_list,
        
        # 'item_name':item_name,
        'item': item,
        # 'item_price' : item_price,
    }
        
    return render(request, 'index.html', context)


def showitem(request , slug):
    if 'cart' in request.session:
        length=request.session['cart'] 
    else:
        length=0  
    
    request.session['current_page']='showitem'
    if not 'customer' in request.session:
        customer = ''
        first_customer = '' 
        last_customer = ''
    else:
        customer = Customer.objects.get(id=request.session['customer_id'])
        first_customer = Customer.first_name       
        last_customer = Customer.last_name
    # if 'id' in request.GET:
    #     id = request.GET['id']
    #     item=Item.objects.get(id=id)

    item = Item.objects.get(slug=slug)    
    item_roll = Item.objects.order_by('-created_at')[:8]
    # if 'item' in request.session:
    #     itemlist = request.session['item']
    # else:
    #     itemlist=''    
    #     print(itemlist)    
           


    context={
        'item':item,
        'item_roll':item_roll,
        #'itemlist': itemlist,
        'customer': customer,   
        'first':first_customer,
        'last':last_customer,
        'length':length
    }
    return render(request, 'item-detail.html', context)



def all_items(request):
    if 'cart' in request.session:
        length=request.session['cart'] 
    else:
        length=0   
    request.session['current_page']='all_items'
    if not 'customer_id' in request.session:
        customer = ''
        first_customer = '' 
        last_customer = ''
    else:
        customer = Customer.objects.get(id=request.session['customer_id'])
        first_customer = Customer.customer_first_name   
        last_customer = Customer.customer_last_name
        

        
    
    if 'item' in request.session:
        itemlist = request.session['item']
    else:
        itemlist=''    
        print(itemlist)

    items = Item.objects.order_by('-item_price')[:12]
    context={
        'items': items,
        'itemlist': itemlist,
        'customer': customer,   
        'first_customer':first_customer,
        'last_customer':last_customer,
        'length':length,
    }
    return render(request, 'item-list.html', context)

    
    
# def register(request):
#     display='1'
#     if request.method == 'POST':
#         form=request.POST
#         errors = []
        
#         if len(form['first_name']) < 2:
#             errors.append('First name must be at least 2 characters.')
#         if len(form['last_name']) < 2:
#             errors.append('Last name must be at least 2 characters.')
#         if len(form['password']) < 8:
#             errors.append('Password must be at least 8 characters.')
#         if not form['password'] == form['cpassword']:
#             errors.append('Password/Confirmation do not match.')
#         if not EMAIL_REGEX.match(form['email']):
#             errors.append('Please provide a valid email') 
        
#         if errors:
#             for e in errors:
#                 messages.error(request, e)
#         else:        
#             try:
#                 Customer.objects.get(email=form['email'])
#                 messages.error(request, 'Your email already exists. Please Login.')
                
#             except Customer.DoesNotExist:
#                 hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
#                 c_hashed_pw = hashed_pw.decode('utf-8')
#                 Customer.objects.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=c_hashed_pw)
#                 messages.success(request,"You successfully registered. Please login!")
#             context={
#             'displayl':display,
#             }  
#             # 
#             return render(request, 'register.html', context)   
#     context={   
#         'displayr':display,
#     }             
#     return render(request, 'register.html', context)

def register(request):
    display='1'
    if request.method == 'POST':
        form=request.POST
        errors = []
        
        if len(form['first_name']) < 2:
            errors.append('First name must be at least 2 characters.')
        if len(form['last_name']) < 2:
            errors.append('Last name must be at least 2 characters.')
        if len(form['password']) < 8:
            errors.append('Password must be at least 8 characters.')
        if not form['password'] == form['cpassword']:
            errors.append('Password/Confirmation do not match.')
        if not EMAIL_REGEX.match(form['email']):
            errors.append('Please provide a valid email') 
        
        if errors:
            for e in errors:
                messages.error(request, e)
        else:        
            try:
                Customer.objects.get(customer_email=form['email'])
                messages.error(request, 'Your email already exists. Please Login.')
                
            except Customer.DoesNotExist:
                hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
                c_hashed_pw = hashed_pw.decode('utf-8')
                Customer.objects.create(customer_first_name=form['first_name'], customer_last_name=form['last_name'], customer_email=form['email'], customer_password=c_hashed_pw)
                messages.success(request,"You successfully registered. Please login!")
            context={
            'displayl':display,
            }  
            return render(request, 'register.html', context)   
    context={   
        'displayr':display,
    }             
    return render(request, 'register.html', context)



def login(request):
    confirm = ''
    display='1'
    if not 'current_page' in request.session:
        current_page = ''
    if request.method == 'POST':
        errors = []
        form=request.POST 
        if not EMAIL_REGEX.match(form['emaill']):
            errors.append('Please provide a valid email') 
        else:
            try:
                customer=Customer.objects.get(customer_email=form['emaill'])
                result = bcrypt.checkpw(request.POST['passwordl'].encode(), customer.customer_password.encode())
                if result:
                    request.session['user_id'] = customer.id
                    
                    confirm = 'yes'
                    location = request.session['current_page']
                    print('location is ',location)
                    if location=='':
                        return redirect("/")
                    else:
                        return redirect("/"+location)
                    # use confirm for signin function in logpay

                    # if 'prod_id' in request.session: 
                          
                    #     return redirect('/cart')
                    # return redirect('/')    
                else:
                    messages.error(request, 'Password does not match.')    
            except Customer.DoesNotExist:
                messages.error(request, 'Your email does not exists. Please register.')
                return redirect('/register')
        
        if errors:
            for e in errors:
                messages.error(request, e)  
             
    context={
        'displayl':display,
    }  
    return render(request, 'login.html', context)   
# def login(request):
#     confirm = ''
#     display='1'
#     if not 'current_page' in request.session:
#         current_page = ''
#     if request.method == 'POST':
#         errors = []
#         form=request.POST 
#         if not EMAIL_REGEX.match(form['emaill']):
#             errors.append('Please provide a valid email') 
#         else:
#             try:
#                 customer=Customer.objects.get(email=form['emaill'])
#                 result = bcrypt.checkpw(request.POST['passwordl'].encode(), customer.password.encode())
#                 if result:
#                     request.session['customer_id'] = customer.id
                    
#                     confirm = 'yes'
#                     location = request.session['current_page']
#                     print('location is ',location)
#                     if location=='':
#                         return redirect("/")
#                     else:
#                         return redirect("/"+location)
#                     # use confirm for signin function in logpay

#                     # if 'prod_id' in request.session: 
                          
#                     #     return redirect('/cart')
#                     # return redirect('/')    
#                 else:
#                     messages.error(request, 'Password does not match.')    
#             except Customer.DoesNotExist:
#                 messages.error(request, 'Your email does not exists. Please register.')
#                 return redirect('/register')
        
#         if errors:
#             for e in errors:
#                 messages.error(request, e)  
             
#     context={
#         'displayl':display,
#     }  
#     return render(request, 'login.html', context)   

def logout(request):
    location = request.session['current_page']
    request.session.clear()
    print('location is ',location)
    if location=='':
        return redirect("/")
    else:
        return redirect("/"+location)

# def search(request):
#     if request.method == 'POST':
#         form=request.POST
#         cate = form['category']
#         cat=int(cate)
#         if cat >0 and cat < 13:
#             return redirect('/men?cat='+cate)
#         elif cat>12 and cat<25:
#             return redirect('/women?cat='+cate) 
#         else:
#             return redirect('/kid?cat='+cate)
#     return redirect("/")

def cart(request):
    #Cart data
    if not 'cart' in request.session:
        request.session['cart'] = 0
    iteminfo = ''
    customer_id = ''
    amount = 0
    length=0
    request.session['current_page']='cart'
    
    #Customer ID and data
    if not 'customer_id' in request.session:
        customer = ''
        first_customer = '' 
        last_customer = ''
        if 'id' in request.GET:
            id = request.GET['id']
            if not 'item_id' in request.session:
                request.session['item_id'] = id    
                # return redirect('/register') 
    else:
        customer = request.session['customer_id']
        customer_id = Customer.objects.get(id=customer)
        first_customer = customer_id.customer_first_name 
        last_customer = Customer.customer_last_name 

 
    if 'item' in request.session:
        itemlist = request.session['item']
        if (itemlist != {}):
            if 'amount' in request.session:
                amount = request.session['amount']
                print(amount)  #log
            iteminfo = {}
                    
            for key, val in itemlist.items():
                iteminfo[Item.objects.get(id = key)] = val
            length=len(iteminfo)    


    request.session['cart']=length
    context={
        'customer':customer_id,
        'itemlist':iteminfo,
        'amount':amount, 
        'item_length':length, 
        'first':first_customer,
        'last':last_customer,          
    }
    
    
    return render(request, 'cart.html', context)

# def cart(request, slug):
#     if not 'cart' in request.session:
#         request.session['cart'] = []
#     request.session['current_page']='cart'

#     saved_list = []#request.session['cart']
#     saved_list.append(Item.objects.get(slug=slug))
#     request.session['cart'] = saved_list
#     length = len(saved_list)
#     #missing length session parameter (might change it to cart_length in all views, Preferred!)

#     if not 'amount' in request.session:
#         request.session['amount'] = 0
#         amount = 0
#         for item in saved_list():
#              amount = amount + item.item_price
#         request.session['amount'] = amount
#     else:
#         amount = request.session['amount']
#         amount = amount +  Item.objects.get(slug=slug).item_price

#     if not 'customer_id' in request.session:
#         customer = ''
#         first_customer = '' 
#         last_customer = ''
#     else:
#         customer = request.session['customer_id']
#         customer_id = Customer.objects.get(id=customer)
#         first_customer = customer_id.customer_first_name 
#         last_customer = customer_id.customer_last_name

#     context={
#         'customer':customer_id,
#         'cart_list':saved_list,
#         'amount':amount, 
#         'item_length':length, 
#         'first':first_customer,
#         'last':last_customer,
#         }

#     return render(request, 'cart.html', context)


      
def order(request):
    if  'customer_id' in request.session:   
        customer = request.session['customer_id']
        customer_d = Customer.objects.get(id=customer)
        first_customer = customer_d.first_name 
        last_customer = customer_d.last_name
    
    else:
        customer = ''
        first_customer = '' 
        last_customer = ''



    length=request.session['cart']
    if request.method == 'POST':
        form=request.POST
        errors = []
        
        if len(form['name']) < 5:
            errors.append('Name must be at least 5 characters.')
        if errors:
            for e in errors:
                messages.error(request, e)
                return redirect('/order')
        else:
            return redirect('/success')
    context={
            'customer':customer,
            'length':length, 
            'first':first_customer,
            'last':last_customer, 
    }        
    return render(request, 'buy.html', context) 

def success(request):
    if 'cart' in request.session:
        del request.session['cart']
    if 'item' in request.session:
        del request.session['item']

    if 'customer_id' in request.session:
        customer = request.session['customer_id']
        customer_d = Customer.objects.get(id=customer)
        first_cusromer = customer_d.first_name
        last_customer = customer_d.last_name
    
    else:
        customer = ''
        customer_d = ''
        first_cusromer = ''
        last_customer = ''


    context={
        'customer':customer,
        'first':first_cusromer,
        'last':last_customer, 
    }  
    return render(request, 'success.html', context)

def checkout(request):
    length=request.session['cart']
    customer = request.session['customer_id']
    customer_id = Customer.objects.get(id=customer)
    first_customer = customer_id.customer_first_name 
    last_customer = customer_id.customer_last_name 
    
    if request.method == 'POST':
        form=request.POST
        errors = []
        
        if len(form['full_name']) < 5:
            errors.append('Full name must be at least 5 characters.')
        if len(form['state']) < 5:
            errors.append('State must be at least 5 characters.')
        if len(form['address']) < 8:
            errors.append('Address must be at least 8 characters.')
        if errors:
            for e in errors:
                messages.error(request, e)
                return redirect('/checkout')
    context={
        'cart_length':length, 
        'first':first_customer,
        'last':last_customer, 
    }            
    return render(request, 'checkout.html', context)

       
def add(request):
    if not 'item' in request.session:
        request.session['item'] = {}
    if 'id' in request.GET:
        id = request.GET['id']
        
        if'loc' in request.GET:
            loc=request.GET['loc']
       

        if not 'id' in request.session:
            request.session['id'] = ''
        request.session['id'] = id    
        item = Item.objects.get(id=id)
        itemlist = request.session['item']
        
        if (itemlist == {}):
            itemlist[item.id] = 1
            request.session['item'] = itemlist 
        else:     
            found = ''
            for key, val in itemlist.items():
                if (key == item.id):
                    found = 'yes'
            if (found == ''):
                itemlist[item.id] = 1
            request.session['item'] = itemlist
        request.session['cart']=len(itemlist)    

        
        amount = float(Item.objects.get(id = id).item_price)
        
        amountlist = request.session['amount']
        if (amountlist == {}):
            amountlist[item.id] = amount
            request.session['amount'] = amountlist 
        else:     
            found = ''
            for key, val in amountlist.items():
                if (key == item.id) :
                    found = 'yes'
            if (found == '') :
                amountlist[id] = amount 
            request.session['amount'] = amountlist 

    return redirect('/'+loc) 


def remove(request):
    if 'id' in request.GET:
        id = request.GET['id']
        itemlist = request.session['item']
        print('id', id)
        for key, val in itemlist.items():
            if (key == id):
                print('came here')
                itemlist.pop(key)
                break
        request.session['item'] = itemlist
        print('itemlist', itemlist)
        amountlist = request.session['amount']

        for key, val in amountlist.items():
            if (key == id):
                amountlist.pop(key)
                break
        request.session['amount'] = amountlist
        print('amountlist', amountlist)
        
    return redirect('/cart')    


def quantity(request):
    if request.method == 'POST':
        if 'id' in request.GET:
            id = request.GET['id']       
        quantity = int(request.POST['quantity'])
        
        if request.POST['button'] == 'left':
            if quantity > 1:
                quantity -= 1
        elif request.POST['button'] == 'right':   
            quantity += 1
        if quantity < 1 :
            quantity = 1
        
        amount = quantity * Item.objects.get(id = id).price
        
        amountlist = request.session['amount']
        
        for key, val in amountlist.items():
            if (key == id) :
                amountlist[key] = amount      
        request.session['amount'] = amountlist
        
        
        itemlist = request.session['item']
        for key, val in itemlist.items():
            if key == id :
                itemlist[key] = quantity

        request.session['item'] = itemlist

    return redirect('/cart') 

def contact_view(request):
    return render(request, 'contact.html')


def about_us(request):
    return render(request, 'about-us.html')



def privacy_policy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms_and_condition.html')


def myacc(request):
    return render(request, 'my-account.html')