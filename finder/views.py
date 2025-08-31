from django.shortcuts import render , redirect
from django.core.paginator import Paginator
from .models import MissingPerson , Report, Searcher
from .utils import get_possible_child_blood_types
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .forms import AdvancedSearchForm , ReportForm,  MissingPersonForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .serializers import MissingPersonSerializer
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "finder/home.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "finder/signup.html", {"form": form})


@login_required(login_url="login")
def add_missing_with_report(request):
    # تأكد من أن الـ User الحالي عنده Searcher (لو User قديم)
    Searcher.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.username,
            'email': request.user.email,
            'phone_number': ''
        }
    )

    if request.method == "POST":
        person_form = MissingPersonForm(request.POST, request.FILES)
        report_form = ReportForm(request.POST)

        if person_form.is_valid() and report_form.is_valid():
            missing_person = person_form.save()  # حفظ بيانات المفقود

            # حفظ البلاغ مربوط بالمفقود والمستخدم الحالي كـ searcher
            report = report_form.save(commit=False)
            report.missing_person = missing_person
            report.searcher = request.user.searcher  # الآن مضمون أن الـ Searcher موجود
            report.save()

            return redirect("report-list")  # رجوع لقائمة البلاغات
    else:
        person_form = MissingPersonForm()
        report_form = ReportForm()

    return render(request, "finder/add_missing_with_report.html", {
        "person_form": person_form,
        "report_form": report_form,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def advanced_search_api(request):
    name = request.GET.get("name")
    address = request.GET.get("address")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    blood_type = request.GET.get("blood_type")
    mother = request.GET.get("mother_blood_type")
    father = request.GET.get("father_blood_type")

    queryset = MissingPerson.objects.all()

    if name:
        queryset = queryset.filter(full_name__icontains=name)
    if address:
        queryset = queryset.filter(disappearance_location__icontains=address)
    if date_from:
        queryset = queryset.filter(disappearance_date__gte=date_from)
    if date_to:
        queryset = queryset.filter(disappearance_date__lte=date_to)

    if blood_type:
        queryset = queryset.filter(blood_type=blood_type)
    elif mother and father:
        possible_types = get_possible_child_blood_types(mother, father)
        queryset = queryset.filter(blood_type__in=possible_types)

    serializer = MissingPersonSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@login_required
def advanced_search(request):
    form = AdvancedSearchForm(request.GET or None)
    page_obj = None
    searched = False   # جديد

    if form.is_valid() and request.GET:  
        searched = True   # يعني فيه بحث فعلاً
        name = form.cleaned_data.get("name")
        address = form.cleaned_data.get("address")
        date_from = form.cleaned_data.get("date_from")
        date_to = form.cleaned_data.get("date_to")
        blood_type = form.cleaned_data.get("blood_type")
        mother = form.cleaned_data.get("mother_blood_type")
        father = form.cleaned_data.get("father_blood_type")

        queryset = MissingPerson.objects.all()

        if name:
            queryset = queryset.filter(full_name__icontains=name)
        if address:
            queryset = queryset.filter(disappearance_location__icontains=address)
        if date_from:
            queryset = queryset.filter(disappearance_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(disappearance_date__lte=date_to)

        if blood_type:
            queryset = queryset.filter(blood_type=blood_type)
        elif mother and father:
            possible_types = get_possible_child_blood_types(mother, father)
            queryset = queryset.filter(blood_type__in=possible_types)

        paginator = Paginator(queryset, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    return render(request, "finder/advanced_search.html", {
        "form": form,
        "page_obj": page_obj,
        "searched": searched,   # نبعته للـ template
    })


@login_required(login_url="login")
def search_view(request):
    query_set = MissingPerson.objects.all()

    blood_type = request.GET.get("blood_type")
    full_name = request.GET.get("full_name")
    gender = request.GET.get("gender")
    disappearance_location = request.GET.get("disappearance_location")

    if blood_type:
        query_set = query_set.filter(blood_type__iexact=blood_type)
    if full_name:
        query_set = query_set.filter(full_name__icontains=full_name)
    if gender:
        query_set = query_set.filter(gender=gender)
    if disappearance_location:
        query_set = query_set.filter(disappearance_location__icontains=disappearance_location)

    # ترتيب بالاسم (أبجديًا) وبعدين الأحدث في تاريخ الاختفاء
    query_set = query_set.order_by("full_name", "-disappearance_date")

    # Pagination (10 نتائج في الصفحة)
    paginator = Paginator(query_set, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"results": page_obj}
    return render(request, "finder/search_results.html", context)

@login_required(login_url="login")
def report_list(request):
    reports = Report.objects.all().order_by("-report_date")
    return render(request, "finder/report_list.html", {"reports": reports})

@login_required(login_url="login")
def report_create(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.searcher = request.user.searcher  # المستخدم الحالي
            report.missing_person = MissingPerson.objects.create(
                full_name=request.POST.get("full_name"),
                blood_type=request.POST.get("blood_type"),
                disappearance_location=request.POST.get("disappearance_location"),
                disappearance_date=request.POST.get("disappearance_date"),
                mother_blood_type=request.POST.get("mother_blood_type"),
                father_blood_type=request.POST.get("father_blood_type"),
            )
            report.save()
            return redirect("report-list")
    else:
        form = ReportForm()
    return render(request, "finder/report_create.html", {"form": form})








