from .models import MyContacts

def global_contacts(request):
    try:
        contacts = MyContacts.objects.first()
    except MyContacts.DoesNotExist:
        contacts = None
    return {'contacts': contacts}