
from django.forms import model_to_dict

def jsonExample(obj):
    print("yes coming",obj)
    s = model_to_dict(obj)
    # s is a string with [] around it, so strip them off
    print(s)
    return s
    # o=s.strip("[]")
    # return django.http.HttpResponse(o, mimetype="application/json")