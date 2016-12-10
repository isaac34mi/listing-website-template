from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
# class UserProfile(models.Model):
# 	#this line is required . links UserProfile to user Model instance.
# 	user = models.OneToOneField(User)

# 	#The additional attributes we wish to include
# 	picture = models.ImageField(upload_to = 'profile_images', blank = True)

# 	#override trhe __unicode__() method to return out something meaningful

# 	def __unicode__(self):
# 		return self.user.username

class Category(models.Model):
 	name = models.CharField(max_length=128, unique = True)
 	views = models.IntegerField(default = 0)
 	likes = models.IntegerField(default = 0)
 	slug = models.SlugField()
 	def save(self, *args, **kwargs):
 		self.slug = slugify(self.name)
 		super(Category, self).save(*args, **kwargs)

 	class Meta:
 		verbose_name_plural = "categories"

 	def __unicode__(self):
 		return self.name

class Products(models.Model):
	category = models.ForeignKey(Category)
	user = models.ForeignKey(User)
	title = models.CharField(max_length = 128)
	description =models.TextField()
	product_price =models.DecimalField(decimal_places=2,max_digits = 20,blank=True,null =True)
	coverImage = models.ImageField(upload_to ='product_images',blank =True)
	contact_Name = models.CharField(max_length = 128,blank=True)
	contact_email = models.EmailField(blank=True)
	product_location = models.CharField(max_length = 128,blank=True)
	contact_number = models.IntegerField(blank=True, null = True)
	Fb_url = models.CharField(max_length=128,blank=True)
	views = models.IntegerField(default = 0)
	date_created = models.DateTimeField(auto_now=True)
	code = models.AutoField(primary_key=True)

	def __unicode__(self):
	    return "{0} {1}".format(self.title , self.code)

class Images(models.Model):
	post= models.IntegerField(default=0)
	user = models.ForeignKey(User)
	image = models.ImageField(upload_to ='product_images',blank =True,verbose_name="Images")

	def __unicode__(self):
		return self.image.name
