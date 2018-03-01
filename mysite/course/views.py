from django.views.generic import TemplateView, ListView    

from .models import Course    

class CourseListView(ListView):    
    model = Course    
    # 声明传入模板的变量名称。如果不写，模板默认变量名称是object
    # 变量指代相应数据表中的所有记录
    context_object_name = "courses"    
    template_name = 'course/course_list.html'
