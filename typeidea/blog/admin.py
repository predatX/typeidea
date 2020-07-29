from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from custom_site import *
# from typeidea.custom_site import *

# Register your models here.

class PostInline(admin.TabularInline):
	fields=('title','desc')
	extra=1
	model=Post
class CategoryAdmin(admin.ModelAdmin):
	inlines=[PostInline,]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name', 'status', 'is_nav', 'created_time')
    fields=('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
    	obj.owner = request.user
    	return super(CategoryAdmin, self).save_model(request, obj, form, change)

    # def post_count(self, obj):
    # 	return obj.post_set.count()

    # post_count.short_description='Totallay artical numbers:~'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=('name', 'status', 'created_time')
    fields=('name', 'status')

    def save_model(self, request, obj, form, change):
    	obj.owner = request.user
    	return super(TagAdmin, self).save_model(request,obj, form, change)

@admin.register(Post, site=CustomSite(name='cus_admin'))
# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
# 	form = PostAdminForm

class PostAdmin(admin.ModelAdmin):

	class Media:
		css={
			'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
		}
		js=('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)

	class CategoryOwnerFilter(admin.SimpleListFilter):
		title='CategoryFilter~'
		parameter_name = 'owner_category'

		def lookups(self, request, model_admin):
			return Category.objects.filter(owner=request.user).values_list('id', 'name')
		def queryset(self, request, queryset):
			category_id = self.value()
			if category_id:
				return queryset.filter(category_id=self.value())
			return queryset

	list_display = [
		'title','category','status','created_time','operator'
	]
	list_display_links=[]

	# list_filter=['category']
	list_filter = [CategoryOwnerFilter]
	search_filelds=['title', 'category_name']

	actions_on_top=True

	exclude=('owner',)

	# fields=(
	# 	('category', 'title'),
	# 	'desc',
	# 	'status',
	# 	'content',
	# 	'tag',
	# )

	fieldsets=(
		('BasicConfig~',{
			'description': 'BasicConfig DESC~',
			'fields':(
				('title', 'category'),
				'status',
				),
		}),
		('Content~', {
			'fields':(
				'desc',
				'content',
				),
		}),
		('AddInfo~', {
			'classes':('Collapse',),
			'fields':('tag',),
		})
	)

	# def operator(self, obj):
	# 	return format_html(
	# 		'<a href="{}">EDITER~</a>',
	# 		reverse('admin:blog_post_change', args=(obj.id,))
	# )
	# operator.short_description='OPERATION~'

	def operator(self, obj):
		return format_html(
			'<a href="{}">EDITER~</a>',
			reverse('cus_admin:blog_post_change', args=(obj.id,))
	)
	operator.short_description='OPERATION~'	

	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		return super(PostAdmin, self).save_model(request, obj, form, change)

	def get_queryset(self, request):
		qs=super(PostAdmin, self).get_queryset(request)
		return qs.filter(owner=request.user)



