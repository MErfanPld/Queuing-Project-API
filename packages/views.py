from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from packages.filters import PackageFilters
from .models import Package
from .forms import PackageForm, PackageReviewForm
from django.views.generic.edit import FormView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from acl.mixins import PermissionMixin
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Package
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Package, PackageReview
from .forms import PackageReviewForm


class PackageListView(ListView):
    model = Package
    template_name = 'packages/package_list.html'
    context_object_name = 'packages'


class PackageDetailView(FormMixin, DetailView):
    model = Package
    template_name = 'packages/package_detail.html'
    context_object_name = 'package'
    form_class = PackageReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['review_form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            review, created = PackageReview.objects.update_or_create(
                user=self.request.user, package=self.object,
                defaults={
                    'rating': form.cleaned_data['rating'], 'comment': form.cleaned_data['comment']}
            )
            if created:
                messages.success(self.request, "نظر شما با موفقیت ثبت شد.")
            else:
                messages.success(self.request, "نظر شما به‌روزرسانی شد.")
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse('packages:package_detail', kwargs={'pk': self.object.pk})


class AddReviewView(LoginRequiredMixin, FormView):
    template_name = 'packages/package_detail.html'
    form_class = PackageReviewForm

    def form_valid(self, form):
        package = get_object_or_404(Package, id=self.kwargs['package_id'])
        review, created = PackageReview.objects.update_or_create(
            user=self.request.user, package=package,
            defaults={
                'rating': form.cleaned_data['rating'], 'comment': form.cleaned_data['comment']}
        )
        if created:
            messages.success(self.request, "نظر شما با موفقیت ثبت شد.")
        else:
            messages.success(self.request, "نظر شما به‌روزرسانی شد.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('packages:package_detail', kwargs={'pk': self.kwargs['pk']})



# ? ============================= Package CRUD =============================


class PackageListViewAdmin(PermissionMixin, ListView):
    permissions = ['Package_list']
    model = Package
    context_object_name = 'Package_list'
    template_name = 'packages/package_admin_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return PackageFilters(data=self.request.GET, queryset=queryset).qs


class PackageCreateViewAdmin(PermissionMixin, CreateView):
    permissions = ['Package_create']
    template_name = 'packages/package_admin_form.html'
    model = Package
    form_class = PackageForm
    success_url = reverse_lazy("package-admin-list")


class PackageUpdateViewAdmin(PermissionMixin, UpdateView):
    permissions = ['Package_list_edit']
    template_name = 'packages/package_admin_form.html'
    model = Package
    form_class = PackageForm
    success_url = reverse_lazy("package-admin-list")


class PackageDeleteViewAdmin(PermissionMixin, DeleteView):
    permissions = ['Package_list_delete']
    model = Package
    template_name = 'packages/confirm_package_delete.html'
    success_url = reverse_lazy("package-admin-list")


# ? ============================= PackageReview CRUD =============================

class PackageReviewListViewAdmin(PermissionMixin, ListView):
    permissions = ['Package_list']
    model = PackageReview
    context_object_name = 'Package_Review_list'
    template_name = 'packages/package_review_admin_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

class PackageReviewDeleteViewAdmin(PermissionMixin, DeleteView):
    permissions = ['Package_list_delete']
    model = PackageReview
    template_name = 'packages/confirm_package_review_delete.html'
    success_url = reverse_lazy("package-admin-list")