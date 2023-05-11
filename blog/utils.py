import datetime

from django.http import HttpRequest


def logging_txt_decorator(func):
    def wrapper(*args, **kwargs):
        request: HttpRequest = args[-1]

        if request.user.is_anonymous:
            username = "Аноним"
        else:
            username = request.user.username
        with open("log.txt", 'a', encoding="utf-8") as file:
            file.write(f"{username} | {request.path} | {request.method} | {datetime.datetime.now()}\n")

        response = func(*args, **kwargs)
        return response

    return wrapper
