# General Query All Data
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404  # search by ID
from django.db.models import Q # Multiple DB query

# CRUD
# Create
Model.objects.create('argements)
# Read
Model.objects.get(pk=data_id)
VoteRecord.objects.filter('argeuments')

# Update
Model.objects.get(pk=data_id)
Model.objects.filter('argeuments').frist()
Model.arg = 'data'
Model.save()
# Delete
Model.objects.get(pk=data_id)
Model.objects.filter('argeuments').frist()
Model.delete()
                     

"""
``` All Document: https://github.com/samratpro/Django-Component/blob/master/Model/queryset.md ```
    MyModel.objects.all()                  ``` Get All data
    MyModel.objects.filter(field=value)    ``` Filter return **List/multiple data**, It can be used for any backend continuous logic until getting certain data
    MyModel.objects.get(field=value)       ``` Get return **Single Data**, 
    from django.db.models import Q
    keyword_pending = BulkKeywordModel.objects.filter(Q(status='Pending') | Q(status='Running...'))   ``` Multiple query,
    
``` Here filed list: ```
    Document: https://docs.djangoproject.com/en/4.2/ref/models/querysets/#id4
    pk = Primary Key
    id = Identity Like PK
    custom_name = Our created custom variable name
    custom_name__contains = custom_name is variable
    id__in= [1, 3, 4] *** it can take multiple or Single id values
    custom_name__in =  *** It can take multiple or Single id values       
    
``` Render data from the Model don't affect your POST or GET method Runtime, ```
``` VT(view.py to temple.html) data will affect by the User action, ```
``` MTV(Models Views Template) data won't affect by the User action ..without Logic.., ```
"""

# Save data ***********************************************
@login_required(login_url='login/')  # login/  is custom login URL path
def website(request):
    template = 'add_data_.html'
    if request.method == 'POST':
        form = DataForms(request.POST)
        context = {'data_form':form}
        if form.is_valid():
            data_name = form.cleaned_data['data_name']
            data_url = form.cleaned_data['data_url']
            obj = DataModel(data_name=data_name, data_url=data_url)
            obj.save()
            return redirect('/alldata')
        else:
            return redirect('/add_data')
    else:
        form = DataForms()
        context = {'data_form':form}
        return render(request, template, context=context)

# Showing all data, like posts in category ***********************************************
@login_required(login_url='login/')  # login/  is custom login URL path
def AllDataShow(request):
    all_data = WesiteModel.objects.filter(user=request.user)  # accroding to current authenticate user data
    all_data = WesiteModel.objects.all()
    template = 'all_data_show.html'
    context = {'all_data':all_data}
    return render(request, template, context=context)

# Viewing Single Data .....................................
@login_required(login_url='login/')  # login/  is custom login URL path
def single_data(request, data_id):   # ```data_id``` should be pass in url as <data_id>
    template = "single_data.html"
    sigle_data = WesiteModel.objects.get(pk=data_id)                           # we can't use `id` as function argument
  
    if request.user.is_authenticated:
       sigle_data = WesiteModel.objects.get(pk=data_id)      # only authenticate user can see this data
  
    sigle_data = WesiteModel.objects.get(user=request.user, pk=data_id)        # only specific authenticate user's data will show
    context = {'sigle_data': sigle_data,'data_id': data_id}   # data id for editing request
    return render(request, template, context)

# Update Data ***********************************************
@login_required(login_url='login/')  # login/  is custom login URL path
def update_data(request, data_id):   # ```data_id``` should be pass in url as <data_id>
    template = "update_data.html"
    data = WesiteModel.objects.get(pk=data_id)
    data = WesiteModel.objects.get(pk=data_id, user=request.user)        # only authenticate user can update this data
    if request.method == "POST":
        update_form = WebsiteForms(request.POST)
        if update_form.is_valid():
            data.data_name = update_form.cleaned_data['data_name']
            data.data_url = update_form.cleaned_data['data_url']
            data.save()
            return redirect('/alldata')
    else:
        update_form = WebsiteForms(initial={
            'data_name': website.data_name,
            'data_url': website.data_url,
        })
    context = {'update_form': update_form,'data_id': data_id}
    return render(request, template, context)

# Delete Data ***********************************************
@login_required(login_url='login/')  # login/  is custom login URL path
def delete_data(request, data_id):   # ```data_id``` should be pass in url as <data_id>
    data = WesiteModel.objects.get(pk=data_id, user=request.user)        # only authenticate user can delete this data
    data.delete()
    return redirect('/alldata')


# Select Data From different Model From HTML Template ***********************************************
@login_required(login_url='login/')  # login/  is custom login URL path
from .task import *
import threading
scheduler_thread = None  
def bulkpost(request):
    template = 'bulkpost.html'
    website = WesiteModel.objects.all()
    openaiapi = OpenaiAPIModel.objects.all()
    youtubeapi = YoutubeAPIModel.objects.all()
    keyword_pending = BulkKeywordModel.objects.filter(status='Pending')
    context = {'keyword_pending': keyword_pending, 'openaiapi':openaiapi, 'youtubeapi':youtubeapi, 'website':website}
    
    if request.method == 'POST':
        keyword_list = request.POST.get('keyword_list')
        keywords = keyword_list.split('\n')
        
        website_id = request.POST['website_id']
        website_url = WesiteModel.objects.get(pk=website_id).website_url
        website_username = WesiteModel.objects.get(pk=website_id).username
        website_app_pass = WesiteModel.objects.get(pk=website_id).app_pass
        
        openaiapi_id = request.POST['openaiapi_id']
        openai_api_key = OpenaiAPIModel.objects.get(pk=openaiapi_id).API_Key
        
        youtubeapi_id = request.POST['youtubeapi_id']
        youtube_api_key = YoutubeAPIModel.objects.get(pk=youtubeapi_id).API_Key 
        
        print('website_url : ', website_url)
        print('website_username : ', website_username)
        print('website_app_pass : ', website_app_pass)
        print('openai_api_key : ', openai_api_key)
        print('youtube_api_key : ', youtube_api_key)
        
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword:
                BulkKeywordModel.objects.create(name=keyword, status='Pending')

        global scheduler_thread
        if scheduler_thread is None or not scheduler_thread.is_alive():
            # Start the task scheduler in a separate thread
            scheduler_thread = threading.Thread(target=BulkKeywordsJob)
            scheduler_thread.start()
        return redirect('bulkpost')
    
    return render(request, template, context=context)



# Select Data From different Model and Save another model  (ForignKey) ***********************************************
@login_required(login_url='login/')
def profile(request):
    user_profile = AppUser.objects.get(email=request.user.email)
    all_deparment = Deperment.objects.all()
    context = {'user_profile': user_profile, 'all_deparment': all_deparment}

    if request.method == 'POST':
        email = request.POST.get('email')
        deparment_id = request.POST.get('deparment')

        if deparment_id:
            deparment_instance = get_object_or_404(Deperment, id=deparment_id)
            user_profile.deperment = deparment_instance    # **************** Foreign key take another class's instance so have to pass instance
            user_profile.save()


# Uses of next() to retrive gather all similar data that ForignKey connection ***********************************
# This example is vote count
# Here has 5 models connection, 1. Vote(), 2. VoteRecord() 3. Department() 4. Semester() 5. AppUser()

@login_required
def vote_results(request):
    user = request.user
    existing_vote = Vote.objects.filter(department=user.department, semester=user.semester).first()
    if existing_vote:
        if existing_vote.end_date <= timezone.now():
            # Annotate votes received by each student for a specific vote
            vote_records = (
                VoteRecord.objects
                .filter(vote=existing_vote)  # Filters VoteRecords by the given existing_vote
                .values(
                    'voted_for__id',          # Retrieves the ID of the student voted for
                    'voted_for__first_name',  # Retrieves the first name of the voted-for student
                    'voted_for__last_name',   # Retrieves the last name of the voted-for student
                    'voted_for__profile_image' # Retrieves the profile image of the voted-for student
                )
                .annotate(total_votes=Count('voted_for'))  # Counts the total votes received by each voted-for student
            )
            
            # Get all students in the department and semester
            all_students = AppUser.objects.filter(semester=user.semester, department=user.department)
            
            # Combine both vote records and students who haven't received votes
            # Adding 'total_votes' to all students to indicate votes received
            for student in all_students:
                student.total_votes = next((record['total_votes'] for record in vote_records if record['voted_for__id'] == student.id), 0)
            '''
                1. `student.total_votes` for assigns a new attribute to each student object. 
                    It adds dynamically to the student object retrieved from all_students.

                2. student: Represents each student in the loop.

                3. record['total_votes'] for record in vote_records if record['voted_for__id'] == student.id: 
                   This part is a generator expression. 
                   It iterates through vote_records and filters to find records where the voted_for user ID matches 
                   the current student.id. It retrieves the total_votes for that student if such a record is found.

                4. filters the vote_records queryset to find the records where the voted_for 
                   user ID matches the current student.id. It retrieves the total_votes for that student if found.

                5. next(): This function retrieves the next value from the generator expression. 

                6. If no matching record is found (i.e., the student hasn't received any votes), it returns a default value of 0.
            '''     
            return render(request, 'vote/vote_results.html', {'all_students': all_students})
        else:
            return render(request, 'vote/vote_running.html', {'existing_vote': existing_vote})
    else:
        return render(request, 'vote/no_vote_results.html')
