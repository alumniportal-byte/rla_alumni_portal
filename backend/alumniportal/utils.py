def is_superadmin(user):
    return hasattr(user,"adminprofile") and user.adminprofile.role == "superadmin"

def is_admin(user):
    return hasattr(user,"adminprofile")