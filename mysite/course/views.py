from django.views.generic import TemplateView, ListView
from braces.views import LoginRequiredMixin

from .models import Course

class UserMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model = Course
    login_url = "/account/login/"

class CourseListView(ListView):
    # 声明传入模板的变量名称。如果不写，模板默认变量名称是object
    # 变量指代相应数据表中的所有记录
    model = Course
    context_object_name = "courses"    
    template_name = 'course/course_list.html'


class ManageCourseListView(UserCourseMixin, ListView):  # 一般将Mixin类放在左边，其它类放在右边
    context_object_name = "courses"    
    template_name = 'course/manage/manage_course_list.html'
