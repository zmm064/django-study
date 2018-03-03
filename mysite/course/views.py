from django.views.generic import TemplateView, ListView
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import redirect
from .forms import CreateCourseForm

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


class CreateCourseView(UserCourseMixin, CreateView):
    fields = ['title', 'overview']  # 声明在表单中显示的字段
    template_name = 'course/manage/create_course.html'

    def post(self, request, *args, **kargs):
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form":form})


class DeleteCourseView(UserCourseMixin, DeleteView):
    template_name = 'course/manage/delete_course_confirm.html'
    success_url = reverse_lazy("course:manage_course")
