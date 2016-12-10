
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from state.forms import CategoryForm,ProductForm,ImageForm
from state.models import Category, Products, Images


def category(request, category_name_slug):
	context_dict = {}
	category_list = Category.objects.order_by('-likes')
	try:
		category = Category.objects.get(slug = category_name_slug)
		context_dict['category_name'] = category.name

		products = Products.objects.filter(category=category)
		context_dict['products'] = products

		context_dict['category'] = category
		context_dict['categories'] = category_list

	except Category.DoesNotExist:
		pass

	return render(request, 'state/category.html',context_dict)

@login_required
def add_category(request):
	if request.method =="POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			#save the new categroy
			form.save(commit =True)
			return index(request)
		else:
		    print(form.errors)
	else:
		form =CategoryForm()

	return render(request, 'state/add_category.html', {'form':form})

@login_required
def add_product(request, category_name_slug,pk):
	category_list = Category.objects.order_by('-likes')
	context_dict={'categories':category_list}
	try:
		category = Category.objects.get(slug=category_name_slug)

	except Category.DoesNotExist:
		category = None
	form = ProductForm(request.POST)
	ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=3)
	if request.method == "POST":
		user = User.objects.get(pk=pk)
		formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())
		#formset = ProductForm(request.POST,request.FILES)
		if form.is_valid() and formset.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.user = user
				page.views = 0
				if 'coverImage' in request.FILES:
					page.coverImage = request.FILES['coverImage']
				page.save()
				num= Products.objects.values_list('code', flat=True).order_by('-code')

				num = num[0]
				for frm in formset.cleaned_data:
				    #will leter use pillow to reduce the size of image before it is saved.
				    image = frm.get('image')
				    photo = Images(post=num,user=user,image=image)
				    photo.save()
				return HttpResponseRedirect(reverse('add_sucess'))
		else:
			print (form.errors, formset.errors)
	else:
		form = ProductForm()
		formset = ImageFormSet(queryset=Images.objects.none())

	context_dict['form']=form
	context_dict['category']=category
	context_dict['formset']=formset

	return render(request, 'state/add_page.html',context_dict)

def index(request):
	category_list = Category.objects.order_by('-likes')
	context_dict = {'categories':category_list}
	products = Products.objects.order_by('-date_created')
	context_dict['products'] = products
	return render(request,'state/index.html',context_dict)

def about(request):
	category_list = Category.objects.order_by('-likes')
	context_dict = {'categories':category_list}
	return render(request,'state/about.html',context_dict)

def add_sucess(request):
	category_list = Category.objects.order_by('-likes')
	context_dict = {'categories':category_list}
	return render (request,'state/product_add_sucess.html',context_dict)

def email_success(request):
	category_list = Category.objects.order_by('-likes')
	context_dict = {'categories':category_list}
	return render (request,'state/email_success.html',context_dict)

def delete_product_success(request):
	category_list = Category.objects.order_by('-likes')
	context_dict = {'categories':category_list}
	return render(request,'state/delete_Product_suc.html',context_dict)

def search(request):
	category_list = Category.objects.order_by('-likes')
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		results = Products.objects.filter(title__icontains=q)
		return render (request,"state/search_results.html",{'results':results,'query':q,'categories':category_list})
	else:
		message ='You submitted an empty search'
		return HttpResponse(message)

@login_required
def profile(request,pk):
	user =User.objects.get(pk=pk)
	category_list = Category.objects.order_by('-likes')
	product = Products.objects.filter(user=user)
	context_dict = {'categories':category_list,'products':product}
	return render(request,'state/profile.html',context_dict)

def contact(request):
	if request.method == "POST":
		full_name = request.POST.get("name")
		email = request.POST.get("email")
		comment = request.POST.get("comment")
		Subject = "State-Shop"
		message = "Name: {} \n Email: {} \n message \n {}".format(full_name,email,comment)
		from_email = settings.EMAIL_HOST_USER
		to_email =['stateshopinfo@gmail.com']

		send_mail(
		    Subject,
		    message,
		    from_email,
		    to_email,
		    fail_silently=False,
		    )
		return HttpResponseRedirect(reverse('email_success'))
	else:
		return HttpResponse("there was an error")

@login_required
def account_delete(request, pk):
    if request.method=='POST':
    	user = User.objects.get(pk=pk)
    	product = Products.objects.filter(user=pk)
    	product.delete()
    	user.delete()
    	return HttpResponseRedirect(reverse('index'))
    return render(request, "state/profile.html", {'object':user})

@login_required
def product_delete(request, id):
	if request.method=='POST':
		try:
			product_instance = Products.objects.get(code=id)
			product_image = Images.objects.filter(post=id)
			product_instance.delete()
			product_image.delete()
		except Products.DoesNotExist:
			raise Http404
		except:
			raise Http404
		return HttpResponseRedirect(reverse('delete_product_success'))
	return render(request, "state/profile.html")

def product_detail_view(request, id):
	category_list = Category.objects.order_by('-likes')
	product_instance = get_object_or_404(Products, code=id)
	product_image =Images.objects.filter(post=id)

	try:
		product_instance = Products.objects.get(code=id)
	except Products.DoesNotExist:
		raise Http404
	except:
		raise Http404

	template = "state/product_details.html"
	context = {
		"object": product_instance,
		'categories':category_list,
		'pics':product_image,
	}
	return render(request, template, context)

	###Error handling
def handler404(request):
	context_dict = RequestContext(request)
	response = render(request,'404.html',{'context_dict':context_dict})
	response.status_code = 404
	return response

def handler400(request):
	context_dict = RequestContext(request)
	response = render(request,'400.html',{'context_dict':context_dict})
	response.status_code = 400
	return response

def handler500(request):
	context_dict = RequestContext(request)
	response = render(request,'500.html',{'context_dict':context_dict})
	response.status_code = 500
	return response

def handler403(request):
	context_dict = RequestContext(request)
	response = render(request,'403.html',{'context_dict':context_dict})
	response.status_code = 403
	return response
