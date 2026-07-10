from django.shortcuts import render


def error_404(request, exception):
    template_name = 'portal/page_404.html'
    return render(request, template_name, status=404)

# Internal Server Error

def error_500(request):
    template_name = 'portal/page_500.html'
    return render(request, template_name, status=500)


def error_403(request):
    template_name = 'portal/page_403.html'
    return render(request, template_name, status=403)