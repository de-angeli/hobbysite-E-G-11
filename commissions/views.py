from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, When, Value, IntegerField
from django.forms import modelform_factory

from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobForm, JobApplicationForm


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'

    def get_queryset(self):
        return Commission.objects.annotate(
            status_order=Case(
                When(status="Open", then=Value(0)),
                When(status="Full", then=Value(1)),
                When(status="Completed", then=Value(2)),
                When(status="Discontinued", then=Value(3)),
                output_field=IntegerField()
            )
        ).order_by('status_order', '-created_on')
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            ctx['my_commissions'] = Commission.objects.filter(author=user.profile)
            ctx['applied_commissions'] = Commission.objects.filter(jobs__applications__applicant=user.profile).distinct()
            # gets the commissions that the user has applied for and removes duplicates by using distinct()
        
        return ctx


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/commission_detail.html'

    def get_success_url(self):
        return reverse('commissions:commission-detail', kwargs={'pk':self.object.pk})
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        commission = self.object
        jobs = commission.jobs.all()

        total_manpower = sum(job.manpower_required for job in jobs)
        open_manpower = 0
        
        job_info = []
        for job in jobs:
            occupied_slots = job.applications.filter(status="Accepted").count()
            available_slots = job.manpower_required - occupied_slots
            open_manpower += available_slots
            job_info.append({
                'job': job,
                'available_slots': available_slots,
                'can_apply': self.request.user.is_authenticated and available_slots > 0,
                'own_commission': job.commission.author == self.request.user.profile
            })

        ctx['job_info'] = job_info
        ctx['total_manpower'] = total_manpower
        ctx['open_manpower'] = open_manpower

        if self.request.user.is_authenticated:
            ctx['form'] = JobApplicationForm()
            ctx['user_profile'] = self.request.user.profile

        return ctx
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = JobApplicationForm(request.POST)

        if form.is_valid():
            job_id = request.POST.get('job')
            try:
                job = Job.objects.get(id=job_id, commission=self.object)
            except Job.DoesNotExist:
                return self.render_to_response(self.get_context_data(form=form))
        
            application = form.save(commit=False)
            application.applicant = request.user.profile
            application.job = job
            application.save()

            return redirect(self.get_success_url())
        else:
            ctx = self.get_context_data()
            ctx['form'] = form
            return self.render_to_response(ctx)


class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    template_name = 'commissions/commission_create.html'
    form_class = CommissionForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            commission = form.save(commit=False)
            commission.author = self.request.user.profile
            commission.save()

            roles = request.POST.getlist('job_role')
            manpowers = request.POST.getlist('job_manpower')

            for role, manpower in zip(roles, manpowers):
                if role and manpower: 
                    Job.objects.create(
                        commission=commission,
                        role=role,
                        manpower_required=int(manpower),
                    )

            return redirect(self.get_success_url())
        else:
            return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse('commissions:commission-list')


class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    template_name = 'commissions/commission_update.html'
    form_class = CommissionForm

    def get_queryset(self):
        return Commission.objects.filter(author=self.request.user.profile)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        commission = self.object

        application_forms = []
        for job in commission.jobs.all():
            for application in job.applications.all():
                JobApplicationForm = modelform_factory(JobApplication, fields=['status'])
                form = JobApplicationForm(instance=application, prefix=f'app_{application.id}')
                application_forms.append({
                    'form': form,
                    'application': application,
                    'job': job,
                })
        ctx['application_forms'] = application_forms
        return ctx
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            form.save()

            for job in self.object.jobs.all():
                for application in job.applications.all():
                    JobApplicationForm = modelform_factory(JobApplication, fields=['status'])
                    app_form = JobApplicationForm(
                        request.POST,
                        instance=application,
                        prefix=f'app_{application.id}'
                    )
                    if app_form.is_valid():
                        app_form.save()

            for job in self.object.jobs.all():
                accepted_applications = job.applications.filter(status="Accepted").count()
                if accepted_applications >= job.manpower_required:
                    job.status = "Full"
                else:
                    job.status = "Open"
                job.save(update_fields=["status"])

            if all(job.status == "Full" for job in self.object.jobs.all()):
                self.object.status = "Full"
            else:
                self.object.status = "Open"
            self.object.save(update_fields=["status"])

            return redirect(self.get_success_url())
        return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse('commissions:commission-detail', kwargs={'pk': self.object.pk})