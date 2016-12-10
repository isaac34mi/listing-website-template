from django import forms
from state.models import Products, Category,Images#,UserProfile
from registration.forms import  RegistrationForm
from django.utils.translation import ugettext_lazy as _
from registration.users import UserModel

User = UserModel()
class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Category
		fields =['name',]

class ProductForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Please enter the name of product.")
	description =forms.CharField(help_text ="Please enter a brief and detaild description about product",widget=forms.Textarea)
	product_price = forms.DecimalField(help_text="Please enter product amount",decimal_places=2,required=False)
	coverImage = forms.ImageField(label="Please choose a cover photo", required=False)
	contact_Name = forms.CharField(max_length=128,help_text="Please Enter Contact display name",required=False)
	contact_email = forms.EmailField(help_text="This will be shown for contact. Leave black to use default",required="False")
	contact_number = forms.IntegerField(help_text="Please enter number without '-'",required=False)
	product_location = forms.CharField(max_length=128,help_text="Please enter item location")
	Fb_url = forms.CharField(max_length=200, help_text="Add link to images or product like Facebook.",required =False)
	date_created =forms.DateTimeField(widget=forms.HiddenInput(),required=False)
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)#,help_text="Choose product Image")

	class Meta:
		model = Products
		fields = ['title','description','Fb_url','views','contact_number',"contact_Name",'product_location','contact_email','coverImage','date_created',]
		exclude = ('category','code')

	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('Fb_url')

		if url and not url.startswith('http://'):
			url ='http://' + url
			cleaned_data['Fb_url'] = url
		return cleaned_data

class ImageForm(forms.ModelForm):
	image = forms.ImageField(label="Please add product image")
	class Meta:
		model = Images
		fields =['image',]


class RegForm(RegistrationForm):

    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']

    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.

        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("You can only register with your student email"))
       # return self.cleaned_data['email']

        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

