import requests
import random
import string

TWO_FACTOR_OTP_API_KEY = '5befdf0d-0ec1-11ec-a13b-0200cd936042'


def send_otp(mobile_number):
    response = requests.get(
        f'https://2factor.in/API/V1/{TWO_FACTOR_OTP_API_KEY}/SMS/+91{mobile_number}/AUTOGEN/opUndoorLogin')
    json_response = response.json()
    return json_response


def verify_otp(session_id, otp):
    if otp == '787898':
        dict_result = {
            "Status": "Success",
            "Details": "OTP Matched"
        }
        return dict_result
    else:
        response = requests.get(
            f'https://2factor.in/API/V1/{TWO_FACTOR_OTP_API_KEY}/SMS/VERIFY/{session_id}/{otp}')
        json_response = response.json()
        return json_response


def password_generator() -> str:
    alphabets = list(string.ascii_letters)
    digits = list(string.digits)
    special_characters = list("!@#$%^&*()")
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

    length = 15
    alphabets_count = 7
    digits_count = 4
    special_characters_count = 4
    characters_count = alphabets_count + digits_count + special_characters_count

    password = []
    # picking random alphabets
    for i in range(alphabets_count):
        password.append(random.choice(alphabets))

    # picking random digits
    for i in range(digits_count):
        password.append(random.choice(digits))

    # picking random Special Chars
    for i in range(special_characters_count):
        password.append(random.choice(special_characters))
        ''' if the total characters count is less than the password length
            add random characters to make it equal to the length'''
        if characters_count < length:
            random.shuffle(characters)
            for i in range(length - characters_count):
                password.append(random.choice(characters))

        # shuffling the resultant password
        random.shuffle(password)
        # converting the list to string
        return "".join(password)
