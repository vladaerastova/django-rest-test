from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import status
from ..models import Account
from blog.settings import MAILGUN_API_KEY, CLEARBIT_API_KEY
import clearbit
import requests
import json

mailgun_api_key = MAILGUN_API_KEY
clearbit.key = CLEARBIT_API_KEY
User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'first_name',
			'last_name',
		]


class UserCreateSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(label='Email Address')

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password',
		]
		extra_kwargs = {"password":
							{"write_only": True}}

	def validate(self, data):
		return data

	def validate_email(self, email):
		data = self.get_initial()
		user_qs = User.objects.filter(email=data.get("email"))
		if user_qs.exists():
			raise serializers.ValidationError("This user has already registered.")
		res = requests.get(
			"https://api.mailgun.net/v4/address/validate",
			auth=("api", mailgun_api_key),
			params={"address": email})
		if res.status_code == status.HTTP_200_OK:
			validation = json.loads(res)
			if validation['result'] != 'deliverable':
				raise serializers.ValidationError('Email is incorrect: {}'.format(validation['reason']))
		return email

	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		password = validated_data['password']
		user_obj = User(
			username=username
		)
		user_obj.set_password(password)
		user_obj.email = email
		user_obj.save()
		self.create_account(user_obj)
		return validated_data

	def create_account(self, user):
		account_obj = Account(user=user)
		try:
			lookup = clearbit.Enrichment.find(email=user.email, stream=True)
			if lookup != None:
				info = lookup.get('person')
				if info:
					account_obj.city = info.get('geo').get('city')
					account_obj.country = info.get('geo').get('country')
					account_obj.company_name = info.get('employment').get('name')
					account_obj.company_domain = info.get('employment').get('domain')
					account_obj.role_in_company = info.get('employment').get('role')
					account_obj.title_in_company = info.get('employment').get('title')
					account_obj.linkedin = info.get('linkedin').get('handle')
					user.first_name = info.get('name').get('givenName')
					user.last_name = info.get('name').get('familyName')
		except Exception as e:
			pass
		finally:
			account_obj.save()
			user.save()

