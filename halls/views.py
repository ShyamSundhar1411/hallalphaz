from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Hall,Video
from django.contrib.auth import authenticate,login
from .forms import VideoForm,Search
from django.http import Http404, JsonResponse
import requests
import urllib as u
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
YOUTUBE_API_KEY = 'AIzaSyCUoHYkjv_WGJpkf4RgBd6VI_U5_FmxMx8'
def home(request):
    recent_hall = Hall.objects.all().order_by('-id')[:2]
    
    return render(request,'halls/home.html',{'rec':recent_hall})
@login_required
def dashboard(request):
    hall = Hall.objects.filter(user = request.user)
    return render(request,'halls/dashboard.html',{'hall':hall})
@login_required
def video(request,pk):
    form = VideoForm()
    search_form = Search()
    hall = Hall.objects.get(pk=pk)
    if not hall.user == request.user:
        raise Http404
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            vi = Video()
            vi.url = form.cleaned_data['url']
            vi.hall = hall
            parsed = u.parse.urlparse(vi.url)
            vidid = u.parse.parse_qs(parsed.query).get('v')
            if vidid:
                vi.youtube_id = vidid[0]
                response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ vidid[0] }&key={YOUTUBE_API_KEY}')
                json = response.json()
                title = json['items'][0]['snippet']['title']
                vi.title = title
                vi.save()
                return redirect('detail',pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Needs to be a YouTube URL')
    return render(request,'halls/add.html',{'form':form,'search':search_form,'hall':hall})
@login_required
def video_search(request):
    se = Search(request.GET)
    if se.is_valid():
        encoded_term =  u.parse.quote(se.cleaned_data['search'])
        response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_term}&key={YOUTUBE_API_KEY}' )
        return JsonResponse(response.json())
    return JsonResponse({'error':'Not able to validate form'})
class Signup(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'
    def form_valid(self,form):
        v = super(Signup, self).form_valid(form)
        username, password = form.cleaned_data.get('username'),form.cleaned_data.get('password1')
        user = authenticate(username = username, password = password)
        login(self.request, user)
        return v
class Create(LoginRequiredMixin,generic.CreateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/create.html'
    success_url = reverse_lazy('dashboard')
    def form_valid(self,form):
        form.instance.user = self.request.user
        super(Create, self).form_valid(form)
        return redirect('dashboard')
class Detail(generic.DetailView):
    model = Hall
    template_name = 'halls/detail.html'
class Update(LoginRequiredMixin,generic.UpdateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/update.html'
    success_url = reverse_lazy('dashboard')
    def get_object(self):
        hall = super(Update,self).get_object()
        if not hall.user == self.request.user :
            raise Http404
        return hall
class Delete(LoginRequiredMixin , generic.DeleteView):
    model = Hall
    template_name = 'halls/delete.html'
    success_url = reverse_lazy('dashboard')
    def get_object(self):
        video = super(Delete,self).get_object()
        if not video.user == self.request.user :
            raise Http404
        return video
class DelVid(LoginRequiredMixin , generic.DeleteView):
    model = Video
    template_name = 'halls/delvid.html'
    success_url = reverse_lazy('dashboard')
    def get_object(self):
        video = super(DelVid,self).get_object()
        if not video.hall.user == self.request.user :
            raise Http404
        return video
def about(request):
    return render(request,'halls/about.html')
