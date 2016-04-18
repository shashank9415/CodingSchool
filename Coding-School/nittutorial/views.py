from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Tutorial
from .models import Topic
from .forms import MyRegistrationForm
from django.http import HttpResponse
from django.forms import modelformset_factory
from django.shortcuts import render
from .models import Author
from .forms import TutorialForm
from django.shortcuts import render_to_response
import requests
import json 
import re
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.contrib import auth
from django.core.context_processors import csrf
from taggit.models import Tag
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
def user_login_required(f):
        def wrap(request, *args, **kwargs):
                if 'user_id' not in request.session.keys():
                        return HttpResponseRedirect(request.build_absolute_uri('/'))
                return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap
@user_login_required
def tut1(request):
	#tutorials = Tutorials.objects.all()
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    #contents = Tutorials.objects.filter(contentId__contentId=12345)
    return render(request, 'nittutorial/check.html', {'tutorials': tutorials})
@user_login_required
def forums(request):
    #tutorials = Tutorials.objects.all()
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    #contents = Tutorials.objects.filter(contentId__contentId=12345)
    return render(request, 'nittutorial/forums.html', {'tutorials': tutorials})
@user_login_required
def blogs(request):
    #tutorials = Tutorials.objects.all()
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    #contents = Tutorials.objects.filter(contentId__contentId=12345)
    return render(request, 'nittutorial/blogs.html', {'tutorials': tutorials})
def contributors(request):
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    return render(request, 'nittutorial/contributors.html',{'tutorials': tutorials})
def about(request):
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    return render(request, 'nittutorial/about.html',{'tutorials': tutorials})
def contact(request):
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    return render(request, 'nittutorial/contact.html',{'tutorials': tutorials})

def manage_authors(request):
    AuthorFormSet = modelformset_factory(Author, fields=('name', 'title','birth_date'))
    if request.method == "POST":
        formset = AuthorFormSet(request.POST, request.FILES,
                                queryset=Author.objects.filter(name__startswith='O'))
        if formset.is_valid():
            formset.save()
            # Do something.
    else:
        formset = AuthorFormSet(queryset=Author.objects.filter(name__startswith='O'))
    return render(request, 'nittutorial/registration.html', {'formset': formset})

def post_content(request, title, id):
    tutorial = get_object_or_404(Tutorial, pk=id)
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    tag=[]
    for e in tutorial.tags.all():
        tag.append(e)
    print(tag)
    return render(request, 'nittutorial/post_content.html', { 'tutorials': tutorials, 'tutorial': tutorial,'tag':tag})

def tutorial_new(request):
    if request.method == "POST":
        form = TutorialForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.publishedDate = timezone.now()
            post.save()
            form.save_m2m()
            tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
            print(tutorials)
            return redirect('post_content', title=post.title, id=post.pk)
    else:
        form = TutorialForm()
    return render(request, 'nittutorial/post_edit.html', {'form': form})

def cf_profile(request):
    jsonList=[]
    parsedData = []
    if request.method == 'POST':
        username = request.POST.get('user')
        req=requests.get('http://codeforces.com/api/user.info?handles='+username)
        jsonList.append(json.loads(req.text))
        userData = {}
        for data in jsonList:
           userData['handle'] = data["result"][0]['handle']
           userData['contribution'] = data["result"][0]['contribution']
           userData['rank'] = data["result"][0]['rank']
           userData['rating'] = data["result"][0]['rating']
           userData['maxRating'] = data["result"][0]['maxRating']
        parsedData.append(userData)
    #return HttpResponse(parsedData)
        tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
        return render(request, 'nittutorial/cf_profile.html',{'tutorials': tutorials,'data':parsedData})

def cf_form(request):
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    return render(request, 'nittutorial/cf_form.html',{'tutorials': tutorials})
@user_login_required
def problems_find(request):
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    return render(request, 'nittutorial/problems_find.html',{'tutorials': tutorials})
def problems_display(request):
    jsonList=[]
    parsedData = []
    if request.method == 'POST':
        tag=request.POST.get('tag')
        req=requests.get('http://codeforces.com/api/problemset.problems?tags='+tag)
        jsonList.append(json.loads(req.text))
        problemName={}
        i = 0 
        while i < 10:
            problemName['problem']=jsonList[0]["result"]["problems"][i]['name']
            problemName['contestId']=jsonList[0]["result"]["problems"][i]['contestId']
            problemName['index']=jsonList[0]["result"]["problems"][i]['index']
            parsedData.append(problemName)
            i=i+1
        #return HttpResponse(parsedData)
        tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
        return render(request, 'nittutorial/problems_display.html',{'tutorials': tutorials,'data':parsedData})
        #return HttpResponse(jsonList[0]["result"]["problems"][0]['name'])
def editor(request):
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    return render(request, 'nittutorial/editor.html',{'tutorials': tutorials})
def compile(request):
    if request.method == 'POST':
        code=request.POST.get('code')
        print(code);
        Compile_URL = u'http://api.hackerearth.com/code/compile/'
        CLIENT_SECRET = 'fee4190d6e63d82853d4cb30495a2a0ecaf7e9bf'
        source = code
        data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': source,
        'lang': "PYTHON",
        'time_limit': 5,
        'memory_limit': 262144,
         }
        jsonList=[]
        req = requests.post(Compile_URL, data=data)
        jsonList.append(json.loads(req.text))
        return HttpResponse(jsonList[0]['compile_status'])
def run(request):
    if request.method == 'POST':
        code=request.POST.get('code')
        language=request.POST.get('language')
        Run_URL = u'http://api.hackerearth.com/code/run/'
        CLIENT_SECRET = 'fee4190d6e63d82853d4cb30495a2a0ecaf7e9bf'
        source = code
        data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': source,
        'lang': language,
        'time_limit': 5,
        'memory_limit': 262144,
         }
        jsonList=[]
        req = requests.post(Run_URL, data=data)
        jsonList.append(json.loads(req.text))
        parsedData = []
        userData = {}
        userData['compile_status']=jsonList[0]['compile_status']
        userData['status']=jsonList[0]['run_status']['status']
        userData['time_used']=jsonList[0]['run_status']['time_used']
        userData['memory_used']=jsonList[0]['run_status']['memory_used']
        userData['output_html']=jsonList[0]['run_status']['output_html']
        parsedData.append(userData)
        return HttpResponse(parsedData)
def home(request):
    return render(request,'nittutorial/index.html')

def search_titles(request):
    if(request.method == "POST"):
        search_text = request.POST["search-text"]
    else:
        search_text = ""
    print(search_text)
    search_text=search_text.split(",")
    #re.split('; |,|\*|\n',search_text)
    #print(search_text)
    #for e in search_text:
    Tutorials =  Tutorial.objects.filter(tags__name__in=search_text).distinct()
    #print(Tutorials)
    #print(Tutorials)
    return render(request, "nittutorial/search.html",{"tutorials": Tutorials})

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

class ProductIndex(TagMixin, ListView):
    template_name = 'nittutorial/search.html'
    model = Tutorial
    paginate_by = '10'
    queryset = Tutorial.objects.all()
    context_object_name = 'tutorials'

class TagIndexView(TagMixin, ListView):
    template_name = 'nittutorial/search.html'
    model = Tutorial
    paginate_by = '10'
    context_object_name = 'tutorials'

    def get_queryset(self):
        return Tutorial.objects.filter(tags__slug=self.kwargs.get('slug')).distinct()

def login_view(request):
    c = {}
    c.update(csrf(request))
    return  render(request,"nittutorial/login.html", c)

def auth_view(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = auth.authenticate(username=username, password=password)

    #The above doesn't log them in. It just retrieves the user from the database based on the provided user/pass. If the user/pass is invalid, no user was retrieved, because no user row matched.

    #Below takes that user object and logs them into the database.

    if(user is not None):
        auth.login(request, user)
        return  redirect("/accounts/loggedin")

    #user is None

    return  redirect("/accounts/invalid")

def loggedin_view(request):
    return render(request,'nittutorial/loggedin.html', {"full_name": request.user.username})
    
def invalid_view(request):
    return  render(request,"nittutorial/invalid_login.html")

def logout_view(request):
    auth.logout(request)
    return  render(request,"nittutorial/logout.html")

def register_user_account_view(request):
    if(request.method == "POST"):
        form = MyRegistrationForm(request.POST)
        if(form.is_valid()):
            form.save()
            return  HttpResponseRedirect("/accounts/register_success")
    args = {}
    args.update(csrf(request))
    args["form"] = MyRegistrationForm()

    return  render(request,"nittutorial/login.html", args)

def register_user_account_success_view(request):
    return  render(request,"nittutorial/register_success.html")