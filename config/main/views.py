from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Brands, Cars, Color, Comment, Profile
from django.contrib.auth.models import User
from .form import CarsForm, BrandsForm, ColorForm, CommentFrom, RegisterForm, LoginForm, SendEmail
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView




class IndexListView(ListView):
    model = Cars
    template_name = "index.html"
    context_object_name = "cars"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        """Barcha kerakli ma’lumotlarni kontekstga qo‘shish"""
        context = super().get_context_data(**kwargs)
        context["brands"] = Brands.objects.all()
        context["color"] = Color.objects.all()
        return context

# class IndexListView(ListView):
#     model = Cars
#     template_name = "index.html"
#     context_object_name = "cars"
#     paginate_by = 4
#
#     def get_context_data(self, **kwargs):
#         """Barcha kerakli ma’lumotlarni kontekstga qo‘shish"""
#         context = super().get_context_data(**kwargs)
#         context["brands"] = Brands.objects.all()
#         context["color"] = Color.objects.all()
#         context["cars"] = Cars.objects.all()
#         return context




class ColorDetailView(DetailView):
    model = Color
    template_name = "color_cars.html"
    context_object_name = "color"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars"] = Cars.objects.filter(color=self.object)
        context["all_color"] = Color.objects.all()
        return context



class BrandDetailView(DetailView):
    model = Brands
    template_name = "brand_cars.html"
    context_object_name = "brand"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars"] = Cars.objects.filter(brand=self.object)
        context["all_brands"] = Brands.objects.all()
        return context




class CarDetailView(PermissionRequiredMixin, DetailView):
    model = Cars
    template_name = "car_detail.html"
    context_object_name = "car"
    permission_required = "main.view_car"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(car=self.object)
        context["form"] = CommentFrom()
        return context


class CarUpdateView(UpdateView):
    model = Cars
    form_class = CarsForm
    template_name = 'add_cars.html'

    def get_success_url(self):
        return reverse("car_detail", kwargs={"pk": self.object.pk})

class CarDeleteView(DeleteView):
    model = Cars
    template_name = "confirm_delete.html"

    def get_success_url(self):
        return reverse("index")




class CarCreateView(CreateView):
    model = Cars
    template_name = "add_cars.html"
    fields = ['car_name', 'brand', 'date', 'price', 'color']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("car_detail", kwargs={"pk": self.object.pk})




# class CarUpdateDeleteView(View):
#     """Mashinalarni tahrirlash va o‘chirishni boshqarish"""
#
#     def post(self, request, car_id):
#         car = get_object_or_404(Cars, id=car_id)
#         action = request.POST.get("action")
#
#         if action == "update":
#             if request.user == car.owner or request.user.is_superuser:
#                 form = CarsForm(request.POST, request.FILES, instance=car)
#                 if form.is_valid():
#                     form.save()
#                 return redirect("car_detail", pk=car.id)
#             return HttpResponseForbidden("Siz ushbu mashinani tahrirlash huquqiga ega emassiz!")
#
#         elif action == "delete":
#             if request.user == car.owner or request.user.is_superuser:
#                 car.delete()
#                 return redirect("index")
#             return HttpResponseForbidden("Siz ushbu mashinani o‘chira olmaysiz!")
#
#         return redirect("car_detail", pk=car.id)


class CommentManageView(View):
    """Sharh qo‘shish, tahrirlash va o‘chirishni boshqarish"""

    def post(self, request, car_id):
        car = get_object_or_404(Cars, id=car_id)
        action = request.POST.get("action")
        review_id = request.POST.get("review_id")

        if action == "create":
            form = CommentFrom(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.car = car
                review.user = request.user
                review.save()
            return redirect("car_detail", pk=car.id)

        if review_id and review_id.isdigit():
            review = get_object_or_404(Comment, id=review_id, car=car)

            if action == "update":
                if request.user == review.user:
                    review.text = request.POST.get("text")
                    review.save()
                return redirect("car_detail", pk=car.id)

            elif action == "delete":
                if request.user == review.user:
                    review.delete()
                    return redirect("index")
                return HttpResponseForbidden("Siz ushbu sharhni o‘chira olmaysiz!")

        return redirect("car_detail", pk=car.id)


class UserRegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"{user.username} muvaffaqiyatli qo‘shildi! Xush kelibsiz! 😊")
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "user_login.html"

    def get_success_url(self):
        return reverse_lazy("index")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        messages.success(self.request, f"Xush kelibsiz {user.first_name} {user.last_name}")
        return response


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("user_login")

    def dispatch(self, request, *args, **kwargs):
        messages.warning(request, "Siz akkauntni tark etdingiz, janob!")
        return super().dispatch(request, *args, **kwargs)



class UserProfileView(DetailView):
    model = Profile
    template_name = "profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        """Foydalanuvchi profilini topish"""
        username = self.kwargs.get("username")
        return get_object_or_404(Profile, user__username=username)

    def get_context_data(self, **kwargs):
        """Qo‘shimcha kontekst qo‘shish"""
        context = super().get_context_data(**kwargs)
        user = self.object.user
        context["cars"] = Cars.objects.filter(author=user)
        return context





class SendMailView(View):
    def post(self, request):
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

    def get(self, request):
        form = SendEmail()
        context = {
            'form': form
        }
        return render(request, 'send_main.html', context)


class AddBrandView(CreateView):
    model = Brands
    form_class = BrandsForm
    template_name = "add_brands.html"
    success_url = reverse_lazy("index")

class AddCarView(CreateView):
    model = Cars
    form_class = CarsForm
    template_name = "add_cars.html"
    success_url = reverse_lazy("brands_detail")

class AddColorView(CreateView):
    model = Color
    form_class = ColorForm
    template_name = "add_color.html"
    success_url = reverse_lazy("index")