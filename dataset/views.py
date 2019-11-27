import time
import json
import sys 
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

dict_arr={} 

#function for creating a key value pair.
@csrf_exempt  #To Avoid CSRF Issue as we are not using CSRF token
def create(request): 
    key=request.POST['key'] #Key obtained from the user or from some source
    value=request.POST['value']#Value obtained from the user or from some source
    if request.POST['timeoutvalue'].isnumeric()=='true': #to check the validation for the timeout
        timeout=int(request.POST['timeoutvalue'])
    else:
        timeout=0
        #To avoid duplicate entry check if the key already exists in array
    if key in dict_arr:
        return JsonResponse("Error! Key already exists",safe=False) 
        #else make an entry into the array
    else:
        if(key.isalpha()): #Allow if key contains alphabet
        #To check the file size 
            if sys.getsizeof(dict_arr)<(1024*8388608) and sys.getsizeof(value)<=(16000): 
                if timeout!=0:
                    time_var=[value,time.time()+timeout]
                else:
                    time_var=[value,timeout]
                if len(key)<=32: #constraints for key name capped at 32chars
                    dict_arr[key]=time_var
                    return JsonResponse("Key Value pair created successfully",safe=False) 
            else:
                return JsonResponse("Error! Exceeded Memory limit !! ",safe=False) 
        else:#if key is not alphabets
            return JsonResponse("Error! Invalid key name!! key name must contain only alphabets",safe=False) 

#Function for reading a key value pair. 
@csrf_exempt  
def read(request):
    key=request.POST['key']
    if key not in dict_arr:
        return JsonResponse("Error! Please enter a valid key",safe=False) 
    else:
        temp=dict_arr[key]
        if temp[1]==0:
            stri=str(key)+":"+str(temp[0])
            return JsonResponse(stri,safe=False) 
        else:
            if temp[1]>time.time(): 
                stri=str(key)+":"+str(temp[0]) #returns JSON Object
                return JsonResponse(stri,safe=False) 
            else:
                return JsonResponse("Error! time-to-live of has expired",safe=False) 

#Function for reading all key value pair. 
@csrf_exempt  
def readAll(request):
    return JsonResponse(dict_arr,safe=False) #returns all the key value pairs

#Function for deleting a key value pair. 
@csrf_exempt  
def delete(request):
    key=request.POST['key'] #key to delete the particular item
    if key not in dict_arr: #if the given key is not in array
        return JsonResponse("Error! Please enter a valid key",safe=False)  
    else:
        temp=dict_arr[key]
        if temp[1]!=0:
            if temp[1]>time.time(): #comparing the current time with expiry time
                del dict_arr[key]
                return JsonResponse("Key is deleted successfully",safe=False) 
            else:
                msg="Error! time-to-live of",key,"has expired"
                return JsonResponse(msg,safe=False)
        else:
            del dict_arr[key]
            return JsonResponse("key is deleted successfully",safe=False) 