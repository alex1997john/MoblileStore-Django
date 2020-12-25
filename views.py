from django.shortcuts import render,redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User,auth
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import product,cart,address,order,card
import datetime
from datetime import datetime, timedelta

from django.conf import settings 
from django.core.mail import send_mail 
from django.db.models import Q

# Create your views here.
def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(username=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.info(request,f'Hi {request.user.first_name}, welcome to MobiCart.... 😊😊😊😊')
            return redirect('/')
        else:
            messages.info(request,"Your Username or Password is incoorect..Please check....🤧🤧🤧🤧")
            return redirect(login)
    else:
        return render(request,'login.html')
def index(request):
    # a="2020-12-01"
    # Date = datetime.strptime(a, "%Y/%m/%d")
    # print(Date)
    # b=Date+ timedelta(1)
    # res=order.objects.filter(date__range=["2020-11-25",b ])
    # print(res)
    product1=product.objects.all().order_by('-id')[:6]
    product2=product.objects.all()[:6]
    return render(request,'index.html', {'product':product1,'product2':product2})
# def login(request):
#     return render(request,'login.html')
def register(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        mobilenumber=request.POST['mobileno']
        password=request.POST['password']
        repassword=request.POST['repassword']
        
        if User.objects.filter(username=email).exists():
            print('username already exists')
            messages.info(request,'plase check your Email....it is already existed 🙄🙄🙄  ')
            return redirect(register)
        
        elif len(mobilenumber)!=10:
            messages.info(request,'please check mobile number.. it should be 10 digits🤧🤧')
            return redirect(register)
        elif len(password)<8 :
             messages.info(request,'Password should have atleast 8 Character🤧🤧')
             return redirect(register)
        elif password!=repassword:
            messages.info(request,'Please check the password...password and re-entered password should be same.🤧🤧')
            return redirect(register)
        else:
            user=User.objects.create_user(first_name=fname,last_name=lname,email=email,username=email,password=password)
            user.save()
            print('user created')
            messages.info(request,'You are Successfully registread. Please Log in')
            return redirect(login)
    else:
        return render(request,'register.html')
def logout(request):
    auth.logout(request)
    return redirect(login)

def details(request):
    
    id=request.GET.get('q','')
    print('haii')
    print(id)
    a=[1,2,3,4]
    for i in a:
        print(i)
    product1=product.objects.filter(id=id)
    for i in product1:
        b=i.rate
    print(b)
    c=range(0,b)
    print(c)
        # return redirect(cart)
    return render(request,'product.html',{'product':product1,'c':c})

def addtocart(request):
    if request.user.is_authenticated:
        id=request.GET.get('q','')
        print(id)
        add=cart()
        user1=request.user.id
        print(user1)
        return redirect(index)
    else:
        messages.info(request,"Please Login.......")
        return redirect(login)
def profile(request):
    if request.user.is_authenticated:
        ads=address.objects.filter(user=request.user)
        ord=order.objects.filter(user=request.user).order_by('-id')
    return render(request,'profile.html',{'ads':ads,'ord':ord})
def addproduct(request):
    # if request.method=='POST':
    add=cart()
    if 'addtocart' in request.POST:
        if request.user.is_authenticated:
            print("12345")
            car=cart.objects.filter(user=request.user)
            for i in car:
                if i.product_id==product.objects.get(id=request.POST['id1']):
                    return redirect(cart1)
            else:
                if request.user.is_authenticated:
                    add.user=request.user
                    add.product_id=product.objects.get(id=request.POST['id1'])
                    add.count=request.POST['count']
                    add.date= datetime.now()
                    add.save()
                    messages.info(request,'Your product is added to the cart....')
                    return redirect(cart1)
        else:
            messages.info(request,'Please Log in....')
            return redirect(login)
        
    elif 'buynow' in request.POST:
        if request.user.is_authenticated:
            id=request.POST['id1']
            count=request.POST['count']
            count=int(count)
            pro=product.objects.filter(id=id)
            x=0
            a=[2]
            y=[]
            for i in pro:
                x=x+i.offer_price*count
                y.append(i.id)
            print(y)
            ads=address.objects.filter(user=request.user)
            return render(request,'checkout.html',{'cart1':pro,'ads':ads,'x':x,'count':count,'a':a,'y':y})
        else:
            messages.info(request,'Please Log in....')
            return redirect(login)
    
    return render(request,'login.html')


def cart1(request):
    if request.user.is_authenticated:
        cart1=cart.objects.filter(user=request.user)
        x=0
        y=0
        z=0
        for i in cart1:
            x=x+(i.product_id.actual_price * i.count)
        y=y+(x*10/100)
        z=x+y
        print(x)
        return render(request,'cart.html',{'cart1':cart1,'x':x,'y':y,'z':z})
    else:
        messages.info(request,'Please Log in........')
        return redirect(login)
def remove(request):
    id=request.GET.get('q','')
    cat=cart.objects.get(id=id)
    cat.delete()
    return redirect(cart1)


def checkout(request):

    if 'proceed' in request.POST:
        cart1=cart.objects.filter(user=request.user)
        if not cart1:
            messages.info(request,'Cart is empty plase add some product to the cart...')
            return redirect(index)
        ads=address.objects.filter(user=request.user)
        x=0
        y=[]
        a=[1]
        for i in cart1:
            x=x+i.product_id.offer_price*i.count
            y.append(i.product_id.id)
        return render(request,'checkout.html',{'cart1':cart1,'ads':ads,'x':x,'y':y,'a':a})
    elif 'update' in request.POST:
        return redirect(register)
    else:
         return redirect(login)
def checkout1(request):
    pass

def payment(request):
    if request.method=='POST':
        selectadd=request.POST.get('selectadd')
        products=request.POST.get('products')
        x=request.POST.get('amountt')
        count=request.POST.get('count')
        identity=request.POST.get('identity')
        print(count)
        print(products)
        a=products.split()
        print(a)

        if bool(selectadd):
            return render(request,'card.html',{'id':selectadd,'products':products,'x':x,'count':count,'identity':identity})
            
        else:
            name=request.POST.get('name')
            add=address()
            add.user=request.user
            add.name=request.POST.get('name')
            add.mobileno=request.POST.get('mobileno')
            add.house_name=request.POST.get('house_name')
            add.area=request.POST.get('area')
            add.state=request.POST.get('state')
            add.pincode=request.POST.get('pincode')
            add.address_type=request.POST.get('address_type')
            add.save()
            ads=address.objects.filter(user=request.user).filter(name=name)
            for i in ads:
               id=i.id
            return render(request,'card.html',{'id':id,'products':products,'x':x,'count':count})
            


def cardd(request,id,products,x):
    print(id)
    b=[]
    for i in products:
        b.append(i)
    # b.remove(',')
    # b.remove('[')
    # b.remove(']')
    # b.remove(' ')
    # print(b)
    return render(request,'card.html',{'id':id,'products':products,'x':x})

def order_product(request):
    if request.method=='POST':
        products=request.POST.get('products')
        id=request.POST.get('id')
        amount=request.POST.get('amountt')
        identity=request.POST.get('identity')
        name=request.POST.get('first-name')
        card_number=request.POST.get('number')
        cvv=request.POST.get('cvc')
        expiry=request.POST.get('expiry')
        carddd=card.objects.all()
        for j in carddd:
            if(j.name==name.upper() and j.card_number==card_number and j.cvv==int(cvv) and j.expiry==expiry):
                
                print(identity)
                b=list(products)
                if '[' in b:
                    b.remove('[')
                if ']' in b:
                    b.remove(']')
                if ',' in b:
                    b.remove(',')
                if ' ' in b:
                    b.remove(' ')
                
                print(id)
                print(amount)
                if identity=='[1]':
                    for i in b:
                        print(i)
                        add=order()
                        add.user=request.user
                        add.product=product.objects.get(id=i)
                        add.addres=address.objects.get(id=id)
                        pro=product.objects.get(id=i)
                        car=cart.objects.get(product_id=i,user=request.user)
                        am=pro.offer_price*car.count
                        add.amount=am
                        add.quantity=car.count
                        add.date= datetime.now()
                        add.save()
                        pro=product.objects.get(id=i)
                        c=pro.count
                        pro=product.objects.get(id=i)
                        pro.count=c-1
                        car.delete()

                    subject = 'Booking Confirmation Mail'
                    message = f'Hi {request.user}, thank you for your booking your product in Mobicart.😊'
                    email_from = settings.EMAIL_HOST_USER 
                    recipient_list =[request.user, ] 
                    send_mail( subject, message, email_from, recipient_list ) 
                    messages.info(request,'Your product is booked.. with the given address... You will get a confirmation mail soon  Thank you for Shopping with us 👍')
                    return redirect('/')
                elif identity=='[2]':
                    for i in b:
                        print(i)
                        add=order()
                        add.user=request.user
                        add.product=product.objects.get(id=i)
                        add.addres=address.objects.get(id=id)
                        pro=product.objects.get(id=i)
                        add.amount=pro.offer_price
                        add.quantity=1
                        add.date= datetime.now()
                        add.save()
                        pro=product.objects.get(id=i)
                        c=pro.count
                        pro.count=c-1
                        pro.save(update_fields=['count'])
                        subject = 'Booking Confirmation Mail'
                        message = f'Hi {request.user}, thank you for your booking your product in Mobicart😊'
                        email_from = settings.EMAIL_HOST_USER 
                        recipient_list =[request.user, ] 
                        send_mail( subject, message, email_from, recipient_list ) 
                        messages.info(request,'Your product is booked.. with the given address... You will get a confirmation mail soon 😊 Thank you for Shopping with us 👍')
                        return redirect('/')
        else:
            messages.info(request,'card credential not correct........')
            print('card credential not correct')
        return redirect('/')



def search(request):
    if request.method=='POST':
        que=request.POST.get('search')
        result=product.objects.filter(Q(name__icontains=que) | Q(title__icontains=que))
        return render(request,'productlist.html',{'result':result})
    else:
        return redirect(login)


def cartincrement(request):
    if request.method=='POST':
        id=request.POST.get('id')
        car=cart.objects.get(id=id)
        if car.count==3:
            messages.info(request,'you can add maximum 3 product........')
            return redirect(cart1)
        else:
            car.count=car.count+1
            car.save(update_fields=['count'])
            print(id)
            return redirect(cart1)

def cartdecrement(request):
    if request.method=='POST':
        id=request.POST.get('id')
        car=cart.objects.get(id=id)
        if car.count==1:
            car.delete()
        else:
            car.count=car.count-1
            car.save(update_fields=['count'])
        print(id)
        return redirect(cart1)

def edit(request):
    id=request.GET.get('q','')
    add=address.objects.filter(id=id)
    print(add)
    for i in add:
        print(i.user)
    return render(request,'edit.html',{'add':add})
def editaddress(request):
    if request.method=='POST':
        id=request.POST.get('id')
        mobileno=request.POST.get('mobileno')
        name=request.POST.get('name')
        house_name=request.POST.get('house_name')
        area=request.POST.get('area')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        address_type=request.POST.get('address_type')
       
        add=address.objects.get(id=id)
        add.name=name
        add.mobileno=mobileno
        add.house_name=house_name
        add.area=area
        add.state=state
        add.pincode=pincode 
        add.address_type=address_type
        add.save(update_fields=['mobileno','name','house_name','area','state','pincode','address_type'])
        return redirect(profile)

def view_product(request):
    result=product.objects.all()
    return render(request,'productlist.html',{'result':result})

def cancel(request):
     id=request.GET.get('q','')
     print(id)
     ord=order.objects.get(id=id)
     ord.status="canceled by you"
     ord.save()
     messages.info(request,'Your order is canceled... refundable take upto 3-5 Business days...')
     return redirect(profile)



    


        





