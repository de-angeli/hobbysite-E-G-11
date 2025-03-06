from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Commission

class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'

class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/commission_detail.html'

def commission_list(request):
    commissions = Commission.objects.all()
    ctx = {
        'commissions' : commissions
    }

    return render(request, 'commissions/commission_list.html', ctx)

def commission_detail(request, pk):
    ctx = { 'commission': Commission.objects.get(pk=pk) }

    return render(request, 'commissions/commission_detail.html', ctx)