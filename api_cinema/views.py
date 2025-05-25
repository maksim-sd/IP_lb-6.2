from django.shortcuts import render, HttpResponse


def main(request):
    return HttpResponse("<a href='/api/docs'><input type='button', value='api-docs'><a/> \
                        <a href='/admin'><input type='button', value='admin'><a/>")
