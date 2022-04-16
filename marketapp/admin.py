from django.contrib import admin
from marketapp.models import *

# Registered models to view on /admin
admin.site.register(PostModel)
admin.site.register(LikeModel)
admin.site.register(TransactionModel)