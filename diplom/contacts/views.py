from django.shortcuts import render
from .models import Contact

def contacts_page(request):
    contact_info = Contact.objects.filter(is_active=True).first()
    return render(request, 'contacts/contacts_page.html', {'contact': contact_info})