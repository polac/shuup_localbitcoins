
from shuup.apps import AppConfig

class ShuupLocalbitcoinsAppConfig(AppConfig):
    name = "shuup_localbitcoins"
    verbose_name = "Shuup Localbitcoins Checkout integration"
    label = "shuup_localbitcoins"
    provides = {
        "service_provider_admin_form": [
            "shuup_localbitcoins.admin_forms:LocalbitcoinsAdminForm",
        ],
        "payment_processor_wizard_form_def": [
            "shuup_localbitcoins.admin_forms:LocalbitcoinsWizardFormDef",
        ],
    }
