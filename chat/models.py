from datetime import datetime
from django.utils import timezone
from django.db import models
from accounts.models import User

# Create your models here.



class Message(models.Model):
    body = models.TextField()
    sent_by = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)

    class Meta:
        ordering = ('created_at',)

    def __str__(self) :
        return f'{self.sent_by}'
    

class Room(models.Model):
    WAITING = 'waiting'
    ACTIVE = 'active'
    CLOSED = 'closed'

    CHOICES_STATUS = (
        (WAITING, 'Waiting'),
        (ACTIVE, 'Active'),
        (CLOSED,'Closed')
    )

    uuid = models.CharField(max_length=300)
    client = models.CharField(max_length=255)
    agent = models.ForeignKey(User,related_name='rooms',blank=True,null=True ,on_delete=models.SET_NULL)
    messages = models.ManyToManyField(Message,blank=True)
    url = models.CharField(max_length=255, blank=True,null=True)
    status = models.CharField(max_length=20,choices=CHOICES_STATUS,default=WAITING)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) :
        return f'{self.client} - {self.uuid}'
    
    def get_status_display(self):
        return self.status
    
class UserContacts(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username
    
    def get_contact_list(self):
        return ", ".join([str(i) for i in self.friends.all()])

    