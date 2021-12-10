from django.http import HttpResponse
from rest_framework.views import APIView


# class ValidatePhoneSendOTP(APIView):
#
#     def post(self, request, *args, **kwargs):
#         phone_number = request.data.get('phone')
#         password = request.data.get('password', False)
#         username = request.data.get('username', False)
#         email = request.data.get('email', False)
#
#         if phone_number:
#             phone = str(phone_number)
#             user = User.objects.filter(phone__iexact=phone)
#             if user.exists():
#                 return Response({
#                     'status': False,
#                     'detail': 'Phone number already exists'
#                 })
#
#             else:
#                 key = send_otp(phone)
#                 if key:
#                     old = PhoneOTP.objects.filter(phone__iexact=phone)
#                     if old.exists():
#                         old = old.first()
#                         count = old.count
#                         if count > 10:
#                             return Response({
#                                 'status': False,
#                                 'detail': 'Sending otp error. Limit Exceeded. Please Contact Customer support'
#                             })
#
#                         old.count = count + 1
#                         old.save()
#                         print('Count Increase', count)
#
#                         conn.request("GET",
#                                      "https://2factor.in/API/R1/?module=SMS_OTP&apikey=1028fcd9-3158-11ea-9fa5-0200cd936042&to=" + phone + "&otpvalue=" + str(
#                                          key) + "&templatename=WomenMark1")
#                         res = conn.getresponse()
#
#                         data = res.read()
#                         data = data.decode("utf-8")
#                         data = ast.literal_eval(data)
#
#                         if data["Status"] == 'Success':
#                             old.otp_session_id = data["Details"]
#                             old.save()
#                             print('In validate phone :' + old.otp_session_id)
#                             return Response({
#                                 'status': True,
#                                 'detail': 'OTP sent successfully'
#                             })
#                         else:
#                             return Response({
#                                 'status': False,
#                                 'detail': 'OTP sending Failed'
#                             })

def api_index(request):
    return HttpResponse('HI Opundorr')
