from django.http import HttpResponseRedirect
from django.views.generic import FormView

from frontend.forms import SaintForm


class SaintView(FormView):
    template_name = "saint_list.html"
    # model = Saint
    form_class = SaintForm

    def form_valid(self, form):
        return HttpResponseRedirect("")

    # def post(self):
    #     pass
