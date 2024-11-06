def single_post_view(request, post_id):
    templeate = 'single_post_view.html'
    single_post = SingleKeywordModel.objects.get(pk=post_id)
    context = {'single_post':single_post}
    return render(request, templeate, context=context)
