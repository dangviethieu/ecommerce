from django.shortcuts import render

def _cart_id(request):
    card = request.session.session_key
    if not card:
        card = request.session.create()
    return card
