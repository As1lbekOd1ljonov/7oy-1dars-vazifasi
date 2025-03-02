from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from .models import Brands, Cars, Color, Comment, Profile
from django.contrib.auth.models import User
from .form import CarsForm, BrandsForm, ColorForm, CommentFrom, RegisterForm, LoginForm, SendEmail
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.core.mail import send_mail





def index(request):
    brands = Brands.objects.all()
    cars = Cars.objects.all()
    color = Color.objects.all()
    context = {
        'brands': brands,
        'cars': cars,
        'color': color
    }
    return render(request, 'index.html', context)



def color_detail(request, color_id):
    color = get_object_or_404(Color, id=color_id)
    cars = Cars.objects.filter(color=color)
    all_color = Color.objects.all()
    context = {
        'color': color,
        'cars': cars,
        'all_color': all_color
    }
    return render(request, 'color_cars.html', context)



def brand_detail(request, brand_id):
    brand = get_object_or_404(Brands, id=brand_id)
    cars = Cars.objects.filter(brand=brand)
    all_brands = Brands.objects.all()
    context = {
        'brand': brand,
        'cars': cars,
        'all_brands': all_brands
    }
    return render(request, 'brand_cars.html', context)


@permission_required('main.view_car', raise_exception=True)
def car_detail(request, car_id):
    """Mashina sahifasini ko‘rsatish va sharhlarni boshqarish"""
    car = get_object_or_404(Cars, id=car_id)
    comment = Comment.objects.filter(car=car)
    form = CommentFrom()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            form = CommentFrom(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.car = car
                review.user = request.user
                review.save()
            return redirect("car_detail", car_id=car.id)

        elif action == "update":
            review_id = request.POST.get("review_id")
            review = get_object_or_404(Comment, id=review_id, car=car)

            if request.user == review.user:
                review.text = request.POST.get("text")
                review.save()

            return redirect("car_detail", car_id=car.id)

        elif action == "delete":
            review_id = request.POST.get("review_id")
            review = get_object_or_404(Comment, id=review_id, car=car)
            if request.user == review.user:
                review.delete()

            return redirect("index")

    context = {
        "car": car,
        "comments": comment,
        "form": form
    }
    return render(request, "car_detail.html", context)


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"{user.username} muofiqiyatli qo'shildi !\n"
                                      "Iltimos login qiling !")
            return redirect("user_login")

    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)



def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz {user.first_name} {user.last_name}")
            return redirect('index')
    else:
        form = LoginForm()
    context = {
        'form' : form
    }

    return render(request, 'user_login.html', context)



@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, f"Siz akoutni tark etingiz janob !")
    return redirect("user_login")

def profile(request, username):

    context = {}
    try:
        user = get_object_or_404(User, username=username)
        car = Cars.objects.filter(author=user)
        profile = get_object_or_404(Profile, user=user)
        context['profile'] = profile
        context['car'] = car
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('index')
    return render(request, "profile.html", context)


def send_message_to_email(request):
    if request.method == "POST":
        form = SendEmail(data=request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            for user in User.objects.all():
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='rustamovasilbek1221@gmail.com',
                    recipient_list=[user.email]
                )
        messages.success(request, "Habar yuborildi")
        return redirect('index')
    else:
        form = SendEmail()
    context = {
        'form':form
    }
    return render(request, 'send_main.html', context)