import logging

from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, SearchParts
from .models import Part
from django.views.generic import TemplateView, View
from django.forms.models import model_to_dict
from django.db.models import Q

# class SearchResultsView(ListView):
#     model = Part
#     template_name = "index2.html"
#
#     def get_queryset(self):
#         query = self.request.GET.get("part_name")
#         object_list = Part.objects.filter(
#             Q(name__icontains=query) | Q(state__icontains=query)
#         )
#         return object_list


class Index(View):
    def get(self, request):
        request.session.modified = True
        form = SearchParts(request.GET)
        if form.is_valid():
            query = request.GET.get("part_name")
            object_list = Part.objects.filter(
                part_name__icontains=query
            )
            request.session.modified = True
            return render(request, 'index2.html', {'queryset': object_list})

        else:
            form = SearchParts()
            request.session.modified = True
            return render(request, 'index.html', {'form': form})

    def post(self, request):
        if request.POST.get('part_selected'):
            request.session['part_selected'] = request.POST.get('part_selected')
            logging.warning(request.POST.get('part_selected'))
            input_value = request.session['part_selected']
            data = Part.objects.filter(part_name=input_value)
            request.session.modified = True
            return render(request, 'part_info.html', {'queryset': data})
        else:
            input_value = request.session['part_selected']
            data = Part.objects.filter(part_name=input_value)
            if 'cart_list' not in request.session or not request.session['cart_list']:
                request.session['cart_list'] = [input_value]
            else:
                request.session['cart_list'].append(input_value)
            logging.warning(request.session['cart_list'])
            request.session.modified = True
            return render(request, 'part_info.html', {'queryset': data})


# def part_info(request):
#     input_value = request.session['part_selected']
#     data = Part.objects.filter(part_name=input_value)
#     if request.method == 'POST':
#         if 'cart_list' not in request.session or not request.session['cart_list']:
#             request.session['cart_list'] = [input_value]
#         else:
#             request.session['cart_list'].append(input_value)
#         logging.warning(request.session['cart_list'])
# request.session.modified = True
#     return render(request, 'part_info.html', {'queryset': data})

""" spróbuj zrobić wózek na sesji, to będzie lepsze """ """ Gotowe """


class Cart(View):
    def get(self, request):
        request.session.modified = True
        value = 0
        cart_list = request.session['cart_list']
        cart = []
        for each in cart_list:
            data = Part.objects.get(part_name=each)
            cart.append(model_to_dict(data))
            value += data.price_netto
        # data_ser = serializers.serialize('json', self.get_queryset())
        request.session['cart'] = cart
        logging.warning(request.session['cart'])
        request.session.modified = True
        return render(request, 'show_cart.html', {'cart_list': request.session['cart'], 'value': value})

    def post(self, request):
        value = 0
        value2 = request.POST.get('delete')
        logging.warning(value2)
        logging.warning(request.session['cart'])
        part_to_delete = request.POST.get('delete')
        for ind, each in enumerate(request.session['cart']):
            if str(each) == part_to_delete:
                del request.session['cart'][ind]
                del request.session['cart_list'][ind]
                break
        for each in request.session['cart']:
            value += each['price_netto']
        request.session.modified = True
        return render(request, 'show_cart.html', {'cart_list': request.session['cart'], 'value': value})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not user.is_staff:
                return redirect('index2')
            else:
                return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)
