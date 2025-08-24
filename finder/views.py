from django.shortcuts import render
from .models import MissingPerson
from .utils import get_possible_child_blood_types
from rest_framework.decorators import api_view
from rest_framework.response import Response


def search_form(request):
    return render(request, "search_form.html")


@api_view(['GET'])
def search_view(request):
    search_blood_type = request.GET.get('search_blood_type')
    mother_blood_type = request.GET.get('mother_blood_type')
    father_blood_type = request.GET.get('father_blood_type')

    query_set = MissingPerson.objects.all()

    if search_blood_type:
        query_set = query_set.filter(blood_type=search_blood_type)
    elif mother_blood_type and father_blood_type:
        possible_types = get_possible_child_blood_types(mother_blood_type, father_blood_type)
        if possible_types:
            query_set = query_set.filter(blood_type__in=possible_types)
        else:
            query_set = MissingPerson.objects.none()
    else:
        query_set = MissingPerson.objects.none()

    if request.headers.get("Accept") == "application/json":
        return Response({
            "count": query_set.count(),
            "results": list(query_set.values(
                "id", "full_name", "blood_type", "disappearance_location", "disappearance_date"
            ))
        })
    else:
        context = {"results": query_set}
        return render(request, "search_results.html", context)


