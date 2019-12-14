from django.shortcuts import render
import datetime 

# Create your views here.
def show_current_time(request):
    return render(
        request, 
        'core/current_time.html', 
        {
            'Moscow': str(datetime.datetime.now())
        }
    ) 
