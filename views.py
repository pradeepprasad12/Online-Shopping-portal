from django.shortcuts import render, redirect
from .models import Product, Contact, Orders, OrderUpdate, ProductImage, OfferProduct
from django.contrib.auth.models import User
from django.contrib import messages
from math import ceil
import json
from .forms import EditProfileForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.http import HttpResponse


# Create your views here.

def index(request):
    Offer = OfferProduct.objects.all()
    #print(Offer)
    n = len(Offer)
    #print(n)

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    # params = {'allProds': allProds}
    # p = {'Offer': Offer}
    # print(p)
    return render(request, 'shop/index.html', {'allProds': allProds,
                                               'Offer': Offer})


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method == "POST":
        user = request.user
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(user=user, name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def searchMatch(query, item):
    if query in item.product_name or query in item.category:
        return True
    else:
        return False


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    #print(product)
    return render(request, "shop/prodView.html", {'product': product[0]})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        #print(orderId)
        #print(email)
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def checkout(request):
    if request.method == "POST":
        user = request.user
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')

        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(user=user, items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(user=user, order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')


def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        model = User
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) < 6:
            messages.error(request, " Your user name must be under 6 characters")
            return redirect('/shop')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('/shop')
        if pass1 != pass2:
            messages.error(request, " Passwords do not match")
            return redirect('/shop')

        # check for errorneous input

        # Create the user

        if User.objects.filter(username=username).exists():
            messages.warning(request, " Your account has been not created please try another Username")
            return redirect('/shop')
        else:
            myuser = User.objects.create_user(username, email, pass1)

            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()

            messages.success(request, " Your signin has been successfully created")
            return redirect('/shop')

    else:
        return HttpResponse("404 - Not found")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/shop')


def handeLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('/shop')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect('/shop')

    return HttpResponse("404- Not found")


def profile(request):
    # args = {'user': request.user}
    return render(request, 'shop/profile.html')


def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = EditProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                messages.success(request, 'profile updated successful...')
                fm.save()
        else:
            fm = EditProfileForm(instance=request.user)
        return render(request, 'shop/edit_profile.html', {'name': request.user, 'form': fm})
    else:
        return redirect('/shop')
