
@login_required(login_url='login/')
def profile(request):
    user_profile = AppUser.objects.get(email=request.user.email)
    all_deparment = Deperment.objects.all()
    all_semseter = Semester.objects.all()
    context = {'user_profile': user_profile, 'all_deparment': all_deparment, 'all_semseter': all_semseter}

    if request.method == 'POST':
        profile_image = request.FILES.get('img_upload')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        admission_year = request.POST.get('admission_year')
        deparment_id = request.POST.get('deparment')
        semester_id = request.POST.get('semester')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password')

        if deparment_id:
            deparment_instance = get_object_or_404(Deperment, id=deparment_id)
            user_profile.deperment = deparment_instance
            user_profile.save()

        if semester_id:
            semester_instance = get_object_or_404(Semester, id=semester_id)
            user_profile.semester = semester_instance
            user_profile.save()

        if admission_year:
            user_profile.admission_year = admission_year
            user_profile.save()

        if first_name:
            user_profile.first_name = first_name
            user_profile.save()

        if last_name:
            user_profile.last_name = last_name
            user_profile.save()

        if email:
            user_profile.email = email
            user_profile.save()

        if password1 is not None and password1 == password2:
            user_profile.set_password(password1)
            user_profile.save()

        if profile_image:
            user_profile.profile_image = profile_image
            user_profile.save()

        return redirect('profile')

    return render(request, 'user/profile/profile.html', context=context)
