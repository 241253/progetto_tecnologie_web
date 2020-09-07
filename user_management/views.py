from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, ListView, DeleteView, TemplateView
from booking_management.models import Booking, BookingStatus
from lessons_management.models import UserPackets, Packet
from user_cart.models import PurchasedLessons
from user_management.forms import ProfileCreationForm, UserForm, UserUpdateForm, StaffForm, StaffUpdateForm
from user_management.models import Profile

def login_redirect(request):
    if request.user.is_staff:
        context = {}
        context['profile'] = Profile.objects.get(user__id=request.user.id)
        return render(request, 'user_management/staff/staff_page.html', context)
    else:
        context = {}
        context['profile'] = Profile.objects.get(user=request.user)
        context['purchased_items'] = PurchasedLessons.objects.filter(user_id=request.user.id)[:7]
        context['empty_items'] = [x for x in range(7 - len(PurchasedLessons.objects.filter(user_id=request.user.id)[:7]) + 1)]
        context['booking_items'] = Booking.objects.filter(user_id=request.user.id).exclude(id__in=[x.booking.id for x in BookingStatus.objects.filter(booking__user_id=request.user.id)])[:7]
        context['empty_booking'] = [x for x in range(7 - len(Booking.objects.filter(user_id=request.user.id).exclude(id__in=[x.booking.id for x in BookingStatus.objects.filter(booking__user_id=request.user.id)])[:7]) + 1)]
        context['packets'] = Packet.objects.filter(id__in=[x.packet.id for x in UserPackets.objects.filter(user__id=request.user.id)])[:7]
        context['empty_packet'] = [x for x in range(7 - len(Packet.objects.filter(id__in=[x.packet.id for x in UserPackets.objects.filter(user__id=request.user.id)])[:7]) + 1)]
        return render(request, 'user_management/user/user_page.html', context)

#USER VIEW
def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileCreationForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.foto = profile_form.cleaned_data['foto']
            profile.save()
            profile_form.save()

            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('homePage')
    else:
        user_form = UserForm()
        profile_form = ProfileCreationForm(data=request.GET, files=request.FILES or None)

    context = {'user_form':user_form, 'profile_form':profile_form}
    return render(request, 'user_management/user/user_create.html', context)

@method_decorator(login_required, name='dispatch')
class UserPage(DetailView):
    context_object_name = 'user'
    template_name = 'user_management/user/user_page.html'
    queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        context = super(UserPage, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.all().filter(user=context['user'])[0]
        context['purchased_items'] = PurchasedLessons.objects.filter(user_id=context['user'].id)[:7]
        context['empty_items'] = [x for x in range(7-len(PurchasedLessons.objects.filter(user_id=context['user'].id)[:7])+1)]
        context['booking_items'] = Booking.objects.filter(user_id=context['user'].id).exclude(id__in=[x.booking.id for x in BookingStatus.objects.filter(booking__user_id=context['user'].id)])[:7]
        context['empty_booking'] = [x for x in range(7 - len(Booking.objects.filter(user_id=context['user'].id).exclude(id__in=[x.booking.id for x in BookingStatus.objects.filter(booking__user_id=context['user'].id)])[:7]) + 1)]
        context['packets'] = Packet.objects.filter(id__in=[x.packet.id for x in UserPackets.objects.filter(user__id=context['user'].id)])[:7]
        context['empty_packet'] = [x for x in range(7 - len(Packet.objects.filter(id__in=[x.packet.id for x in UserPackets.objects.filter(user__id=context['user'].id)])[:7]) + 1)]
        return context

@method_decorator(login_required, name='dispatch')
class UserUpdate(UpdateView):
    form_class = UserUpdateForm
    model = User
    template_name = 'user_management/user/user_update.html'
    success_url = reverse_lazy('user_update_complete')

@method_decorator(login_required, name='dispatch')
class ProfilePictureUpdate(UpdateView):
    fields = ['foto']
    model = Profile
    template_name = 'user_management/user/user_img_update.html'
    success_url = reverse_lazy('profile_picture_update_complete')
    
    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
            return super().form_valid(form)

def UserUpdateComplete(request):
    return render(request, 'user_management/user/user_update_complete.html')

def UserImgUpdateComplete(request):
    return render(request, 'user_management/user/user_img_update_complete.html')

@method_decorator(login_required, name='dispatch')
class UserPurchasedLessonView(TemplateView):
    template_name = 'user_management/user/user_purchased_lesson.html'

    def get_context_data(self, **kwargs):
        context = super(UserPurchasedLessonView, self).get_context_data(**kwargs)
        context['lessons'] = PurchasedLessons.objects.filter(user_id=self.request.user.id)
        return context

@method_decorator(login_required, name='dispatch')
class UserPacketsView(TemplateView):
    template_name = 'user_management/user/user_packets.html'

    def get_context_data(self, **kwargs):
        context = super(UserPacketsView, self).get_context_data(**kwargs)
        context['packets'] = Packet.objects.filter(id__in=[x.packet.id for x in UserPackets.objects.filter(user_id=self.request.user.id)])
        return context

#STAFF VIEW
@method_decorator(login_required, name='dispatch')
class StaffPage(DetailView):
    class Meta:
        model = User

    template_name = 'user_management/staff/staff_page.html'

    def get_context_data(self, **kwargs):
        context = super(StaffPage, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user__id=self.request.user.id)
        return context

@method_decorator(login_required, name='dispatch')
class StaffList(ListView):
    model = User
    template_name = 'user_management/staff/staff_list.html'

def create_staff(request):
    if request.method == 'POST':
        user_form = StaffForm(request.POST)
        profile_form = ProfileCreationForm(data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.is_staff = True

            profile = profile_form.save(commit=False)
            profile.user = user
            profile_form.save()

            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')

            return redirect('staff_list')
    else:
        user_form = UserForm()
        profile_form = ProfileCreationForm(data=request.GET, files=request.FILES or None)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'user_management/staff/staff_create.html', context)

@method_decorator(login_required, name='dispatch')
class DeleteStaff(DeleteView):
    model = User
    template_name = 'user_management/staff/staff_delete.html'
    success_url = reverse_lazy('staff_list')

@method_decorator(login_required, name='dispatch')
class UpdateStaff(UpdateView):
    model = User
    form_class = StaffUpdateForm
    template_name = 'user_management/staff/staff_update.html'
    success_url = reverse_lazy('staff_list')

@method_decorator(login_required, name='dispatch')
class DetailStaff(DetailView):
    context_object_name = 'user'
    queryset = User.objects.all()
    # extra_context = {'profile': queryset[0].profile}
    template_name = 'user_management/staff/staff_detail.html'

@method_decorator(login_required, name='dispatch')
class StaffDetailUpdate(UpdateView):
    model = User
    form_class = StaffUpdateForm
    template_name = 'user_management/staff/staff_detail_update.html'
    success_url = reverse_lazy('login_redirect_url')

@method_decorator(login_required, name='dispatch')
def StaffDetailUpdateComplete(request):
    return render(request, 'user_management/staff/staff_detail_update_complete.html')