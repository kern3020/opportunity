from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Company(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=32)
    state_province = models.CharField(max_length=32)
    country = models.CharField(max_length=3)   # select from three digit country code. 
    website = models.URLField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name'];

class Person(models.Model):
    '''
    People a job seeker has met along the way. 
    '''
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    title = models.CharField(max_length=64)
    company = models.ForeignKey(Company, unique=True)

    def __unicode__(self):
        return self.name

class Position(models.Model):
    company = models.ForeignKey(Company, unique=True)
    title = models.CharField(max_length=64)
    website = models.URLField()
    comment = models.CharField(max_length=256)

    def __unicode__(self):
        return  u'%s at %s' % (self.title, self.company)

    class Meta:
        ordering = ['title']

class Activity(models.Model):
    '''
    The job seeker can record activities. When is the interview? 
	Apply for a job? Sent thank to interviewer? 
    '''
    when = models.DateField()
    comment = models.CharField(max_length=256)

    class Meta:
        abstract = True
        ordering = ['when']

class Interview(Activity):
    position = models.ForeignKey(Position, unique=True)
    company = models.ForeignKey(Company, unique=True)
    withWhom = models.ManyToManyField(Person)

    def __unicode__(self):
        return  u'interviewing with %s for %s' % (self.company.name, self.Position.title)

class Apply(Activity): 
    '''
    applied for job
    '''
    position = models.ForeignKey(Position, unique=True)
    company = models.ForeignKey(Company, unique=True)

    def __unicode__(self):
        return  u'Applied for %s at %s' % (self.Position.title, self.company.name)
 
class Networking(Activity):
    '''
    networking at professional event. Company.name is the venue.
    '''
    venue = models.ForeignKey(Company, unique=True)

    def __unicode__(self):
        return  u'Networking at %s' % (self.company.name)

class Gratitude(Activity):
    '''
    send thank you letters.
    '''
    person = models.ForeignKey(Person, unique=True)

    def __unicode__(self):
        return  u'Thank %s' % (self.person.name)

class Conversation(Activity):
    '''
    Conversation can be via email, phone, in-person, etc.
    '''
    METHOD_OF_COMMUNICATION = (
        ("email","E-mail"),
        ("phone","Phone"),
        ("faceToFace","face to face"),
    )
    via = models.CharField(max_length=16, choices=METHOD_OF_COMMUNICATION)
    person = models.ForeignKey(Person, unique=True) 

    def __unicode__(self):
        return  u'Spoke %s via ' % (self.person.name,self.via)

# A UserProfile is a person which uses our system. 

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    title = models.CharField(max_length=32) 
    url = models.URLField("Website", blank=True)

    def __unicode__(self):
        return self.user.username

# UserProfile is associated with the User table. Listen for the post_save 
# signal. Create a profile when new User added.

def create_user_profile(sender, instance, created, **kwargs):
    """
    This is the callback associated with the post_save signal on User. 	
    """ 
    if created:
        UserProfile.objects.create(user=instance)

# register for post_save signal on User 
post_save.connect(create_user_profile, sender=User)

