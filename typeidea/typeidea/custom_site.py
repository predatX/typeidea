from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
	site_header='Typeidea'
	site_title='Typeidea ADMINCONSOLE~'
	index_title='HOME~'

custom_site=CustomSite(name='cus_admin')

# print(custome_site)