# pip install django-user-agents
# pip install django-ipware

from django_user_agents.utils import get_user_agent
from django.http import HttpResponse
from ipware import get_client_ip


def ip(request):
    # Get the visitor's IP address
    visitor_device_ip = request.META.get('REMOTE_ADDR')
    client_ip, status = get_client_ip(request)

    ip_prefix = '.'.join([part for part in client_ip.split('.')[:3]])  # last two digit can be change that's why split and remove

    # browser_fingerprint
    browser_fingerprint = fingerprint.get(request)

    # Get device information
    user_agent = get_user_agent(request)
    device = user_agent.device
    browser = user_agent.browser
    os = user_agent.os

    response = f"<h2>visitor device IP: {visitor_device_ip}</h2><br>"
    response += f"<h2>client_ip: {client_ip}</h2><br>"
    response += f"<h2>ip_prefix: {ip_prefix}</h2><br>"
    response += f"<h2>Device: {device}</h2><br>"
    response += f"<h2>Browser: {browser}</h2><br>"
    response += f"<h2>Operating System: {os}</h2>"
    response += f"<h2>Browser Fingerprint: {browser_fingerprint}</h2>"

    return HttpResponse(response)
