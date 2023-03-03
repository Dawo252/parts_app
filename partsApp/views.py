from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, SearchParts
from .models import Part
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


def index(request):
    if request.method == 'GET':
        form = SearchParts(request.GET)
        if form.is_valid():
            query = request.GET.get("part_name")
            # object_list2 = Part.objects.get(part_name=query)
            object_list = Part.objects.filter(
                part_name__icontains=query
            )
            return render(request, 'index2.html', {'queryset': object_list})
    else:
        form = SearchParts()
    data = None
    if request.method == 'POST':
        input_value = request.POST.get('input_value')
        if input_value:
            data = Part.objects.filter(part_name=input_value)
        return render(request, 'part_info.html', {'queryset': data})
    return render(request, 'index.html', {'form': form})


def part_info(request, first_param=None, second_param=None):
    if request.method == "GET":
        query = request.GET.dict()
        # object_list2 = Part.objects.get(part_name=query)
        # object_list = Part.objects.filter(
        #     part_name__icontains=query
        # )
        return HttpResponse(request.GET.dict())
        # return render(request, "part_info.html", {'queryset': object_list})


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