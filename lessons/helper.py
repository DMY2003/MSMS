from django.shortcuts import redirect

def login_prohibited(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            role = request.user.role 
            if role == "Administrator":
                return redirect('admin_unapproved_requests')
            else:
                return redirect('student_requests')
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def map_terms(terms):
    mapped_terms = {}

    for i in range(len(terms)):
        mapped_terms[i + 1] = terms[i]

    return mapped_terms