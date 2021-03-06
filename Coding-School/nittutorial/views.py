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
from django.http import JsonResponse, HttpResponseForbidden
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import requests, os


COMPILE_URL = "https://api.hackerearth.com/v3/code/compile/"
RUN_URL = "https://api.hackerearth.com/v3/code/run/"

# access config variable
DEBUG = (os.environ.get('HACKIDE_DEBUG') != None)
# DEBUG = (os.environ.get('HACKIDE_DEBUG') or "").lower() == "true"
CLIENT_SECRET = "f5110b53452e3f8affd7c593ab6bb48899622a66"

permitted_languages = ["C", "CPP", "CSHARP", "CLOJURE", "CSS", "HASKELL", "JAVA", "JAVASCRIPT", "OBJECTIVEC", "PERL", "PHP", "PYTHON", "R", "RUBY", "RUST", "SCALA"]


"""
Check if source given with the request is empty
"""
def source_empty_check(source):
    if source == "":
        response = {
            "message" : "Source can't be empty!",
        }
        return JsonResponse(response, safe=False)


"""
Check if lang given with the request is valid one or not
"""
def lang_valid_check(lang):
    if lang not in permitted_languages:
        response = {
            "message" : "Invalid language - not supported!",
        }
        return JsonResponse(response, safe=False)


"""
Handle case when at least one of the keys (lang or source) is absent
"""
def missing_argument_error():
    response = {
        "message" : "ArgumentMissingError: insufficient arguments for compilation!",
    }
    return JsonResponse(response, safe=False)


"""
View catering to /ide/ URL,
simply renders the index.html template
"""
def editor(request):
    # render the index.html
    return render(request, 'nittutorial/editor.html', {})


"""
Method catering to AJAX call at /ide/compile/ endpoint,
makes call at HackerEarth's /compile/ endpoint and returns the compile result as a JsonResponse object
"""
def compile(request):
    if request.is_ajax():
        try:
            source = request.POST['source']
            # Handle Empty Source Case
            source_empty_check(source)
            
            lang = request.POST['lang']
            # Handle Invalid Language Case
            lang_valid_check(lang)

        except KeyError:
            # Handle case when at least one of the keys (lang or source) is absent
            missing_argument_error()

        else:
            compile_data = {
                'client_secret': CLIENT_SECRET,
                'async': 0,
                'source': source,
                'lang': lang,
            }

            r = requests.post(COMPILE_URL, data=compile_data)
            return JsonResponse(r.json(), safe=False)
    else:
        return HttpResponseForbidden();


"""
Method catering to AJAX call at /ide/run/ endpoint,
makes call at HackerEarth's /run/ endpoint and returns the run result as a JsonResponse object
"""
def run(request):
    if request.is_ajax():
        try:
            source = request.POST['source']
            # Handle Empty Source Case
            source_empty_check(source)
            
            lang = request.POST['lang']
            # Handle Invalid Language Case
            lang_valid_check(lang)

        except KeyError:
            # Handle case when at least one of the keys (lang or source) is absent
            missing_argument_error()

        else:
            # default value of 5 sec, if not set
            time_limit = request.POST.get('time_limit', 5)
            # default value of 262144KB (256MB), if not set
            memory_limit = request.POST.get('memory_limit', 262144)

            run_data = {
                'client_secret': CLIENT_SECRET,
                'async': 0,
                'source': source,
                'lang': lang,
                'time_limit': time_limit,
                'memory_limit': memory_limit,
            }

            # if input is present in the request
            if 'input' in request.POST:
                run_data['input'] = request.POST['input']

            """
            Make call to /run/ endpoint of HackerEarth API
            """
            r = requests.post(RUN_URL, data=run_data)
            return JsonResponse(r.json(), safe=False)
    else:
        return HttpResponseForbidden()


def savedCodeView(request, code_id):
    # render the index.html
    return render(request, 'nittutorial/editor.html', {})
    
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
    return render(request, 'nittutorial/homepage.html', {'tutorials': tutorials})

@user_login_required
def forums(request):
    #tutorials = Tutorials.objects.all()
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    #contents = Tutorials.objects.filter(contentId__contentId=12345)
    return render(request, 'nittutorial/forums.html', {'tutorials': tutorials})

def signup(request):
    print("hi")
    return render(request, 'nittutorial/registration1.html')

@user_login_required
def blogs(request):
    #tutorials = Tutorials.objects.all()
    tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
    #contents = Tutorials.objects.filter(contentId__contentId=12345)
    print("shashank",request.session["user_id"])
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

def post_edit(request, title, id):
    tutorial = get_object_or_404(Tutorial, pk=id)
    if request.method=="POST":
        form = TutorialForm(request.POST, instance=tutorial)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()
            return redirect('post_content', title=post.title, id=post.pk)
    else:
        form = TutorialForm(instance=tutorial)
    return render(request, 'nittutorial/post_edit.html', {'form': form})

def post_delete(request, title, id):
    tutorial = get_object_or_404(Tutorial, pk=id)
    print("hello")
    tutorial.delete()
    return redirect('nittutorial')

def tutorial_new(request):
    if request.method == "POST":
        form = TutorialForm(request.POST)
        print("hi",form)
        if form.is_valid():
            print("hi")
            post = form.save(commit=False)
            post.publishedDate = timezone.now()
            post.save()
            form.save_m2m()
            tutorials = Tutorial.objects.filter(publishedDate__lte=timezone.now()).order_by('publishedDate')
            return redirect('post_content', title=post.title, id=post.pk)
    else:
        form = TutorialForm()
    return render(request, 'nittutorial/post_creation.html', {'form': form})

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
    
def home(request):
    return render(request,'nittutorial/homepage.html')

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
def login_user(request):
    # the following few lines check wether the session is exist already or not, if exist based on session type it redirects to a panel
    if "usertype" in request.session: #checks session existence
        usertype_to_redirect=request.session["usertype"] #gets the user type from session
        #if (usertype_to_redirect=="student"):
        return render(request,'nittutorial/loggedin.html')  #returns to any one of the above choice based on usertype
    #the following will checks the type of user and sets session for a user and redierects to respective panel
    else:
        c={}
        c.update(csrf(request))
        state = "Please log in below..."
        username =''
        password = ''
        if request.POST:
            username = request.POST.get('username') #receives username from loginpage auth.html
            password = request.POST.get('password') #receives password from loginpage auth.html
            request_user = auth.authenticate(username=username, password=password)
            if request_user is not None:
                if request_user.is_active:
                    auth.login(request, request_user)
                    state = "You're successfully logged in!"
                   # db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
                    #cursor = db.cursor()
                    #query="select is_superuser,id from auth_user where username='"+username+"';" #query to check if user is admin
                    #cursor.execute(query)
                    #data=cursor.fetchall()
                    #db.close()
                    usertype={}
                    usertype={"user_type":"admin","user_id":"123"}
                    request.session["user_id"]=usertype["user_id"]
                    request.session["username"]=username
                    request.session["usertype"]=usertype["user_type"]
                    print ("admin id:",request.session["user_id"])
                    return redirect("/accounts/loggedin") #redirection url
                else:
                    state = "Your account is not active, please contact the site admin."
            else:
                state = "Your username and/or password were incorrect."
        return render_to_response('nittutorial/login.html',{'state':state, 'username': username}) #if it doesn't satisfy any role redirects to home only

def loggedin_view(request):
    return render(request,'nittutorial/loggedin.html', {"full_name": request.user.username,"email":request.user.email})
    
def invalid_view(request):
    return  render(request,"nittutorial/invalid_login.html")

def logout_view(request):
    del request.session["user_id"]
    del request.session["usertype"]
    del request.session["username"]
    request.session.set_expiry(0)   
    request.session.modified=True
    auth.logout(request)
    return  render(request,"nittutorial/homepage.html")

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