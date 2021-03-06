from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.utils import json
from selenium.webdriver.common.by import By

from accounts.serializers import UserSerializer


from selenium import webdriver


User=get_user_model()

def get_api_key(email):
    driver = webdriver.Chrome('/Users/f5/python/CLOUD_2020/chromedriver')
    driver.implicitly_wait(5)
    driver.get('https://finnhub.io/register')

    email_input = driver.find_element_by_xpath(
        '//*[@id="root"]/div[2]/div/div/div/form/input[2]')
    password_input = driver.find_element_by_xpath(
        '//*[@id="root"]/div[2]/div/div/div/form/input[3]')

    email_input.send_keys(email)
    password_input.send_keys('1234')
    driver.find_element_by_xpath('//*[@id="root"]/div[2]/div/div/div/a').click()

    key = driver.find_element_by_xpath(
        '//*[@id="root"]/div[2]/div/div/div[2]/div[1]/div/div[2]/input').get_attribute('value')

    return key
@csrf_exempt
def check_email(request):
    email = json.loads(request.body.decode('utf-8'))['email']
    try:
        User.objects.get(email=email)
        return JsonResponse({'message':'already exists'})
    except:
        api_key = get_api_key(email)
        return JsonResponse({'message':'success','api_key':api_key})

class SignupView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

def jwt_response_payload_handler(token, user=None, request=None):

    return {
        'token': token,
        'api_key': user.api_key
    }
