from .tasks import content_creation_job


@login_required(login_url='login/')
def bulk_posting(request):
    # Your existing code...

    if request.method == 'POST':
        try:
           arg1 = request.POST.get('data1')
           arg2 = request.POST.get('data2')
          
           content_creation_job.delay(arg1, arg2)  # We can't pass such as argument that dosen't support JSON format 
                                                   # like, a model, a object etc
            
          
           return redirect('info_bulk_posting')
        except Exception as e:
            return redirect('posting')
    else:
        return render(request, template, context=context)
