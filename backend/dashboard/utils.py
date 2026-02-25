from django.shortcuts import redirect

def superadmin_required(view_func):

    def wrapper(request,*args,**kwargs):

        if not hasattr(request.user,"adminprofile"):
            return redirect("dashboard")

        if request.user.adminprofile.role != "superadmin":
            return redirect("dashboard")

        return view_func(request,*args,**kwargs)

    return wrapper  