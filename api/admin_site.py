from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class CustomAdminSite(AdminSite):
    site_title = _('Gangan Admin')
    site_header = _('Gangan Administration')
    index_title = _('Gangan Admin Portal')

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_list += [
            {
                'name': 'Dashboard',
                'app_label': 'dashboard',
                'models': [{
                    'name': 'Statistics',
                    'object_name': 'statistics',
                    'admin_url': '/admin/dashboard/',
                    'view_only': True,
                }],
            }
        ]
        return app_list

custom_admin_site = CustomAdminSite(name='custom_admin')

