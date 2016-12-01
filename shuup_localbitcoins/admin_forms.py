
from django import forms

from shuup.admin.forms import ShuupAdminForm
from shuup.admin.modules.service_providers.forms import ServiceWizardForm, ServiceWizardFormDef

from shuup_localbitcoins.models import LocalbitcoinsCheckoutPaymentProcessor

class LocalbitcoinsAdminForm(ShuupAdminForm):
    class Meta:
        model = LocalbitcoinsCheckoutPaymentProcessor
        fields = '__all__'
        widgets = {
            'api_key': forms.PasswordInput(render_value=True),
            'api_secret': forms.PasswordInput(render_value=True),
        }

class LocalbitcoinsWizardForm(ServiceWizardForm):
    class Meta:
        model = LocalbitcoinsCheckoutPaymentProcessor
        fields = ("name", "api_key", "api_secret")
        widgets = {
            'api_key': forms.PasswordInput(render_value=True),
            'api_secret': forms.PasswordInput(render_value=True),
        }

class LocalbitcoinsWizardFormDef(ServiceWizardFormDef):
    def __init__(self):
        super(LocalbitcoinsWizardFormDef, self).__init__(
            name="localbitcoins",
            form_class=LocalbitcoinsWizardForm,
            template_name="shuup/localbitcoins/wizard_form.jinja",
        )