from django.shortcuts import render

# Create your views here.
def test_ui(request):
    return render(request, "test_ui.html")
