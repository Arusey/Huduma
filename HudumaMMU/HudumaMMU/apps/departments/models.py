from django.db import models
from django.core.validators import RegexValidator
from ..authentication.models import User
from cloudinary.models import CloudinaryField

# Create your models here.






class Department(models.Model):
    """Create models for the departments"""
    name = models.CharField(max_length=50, blank=False)
    service = models.CharField(max_length=400, blank=False)
    email = models.EmailField(max_length=40, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    image = CloudinaryField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='departments',
                               on_delete=models.CASCADE,
                               blank=True, null=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        """create an department and save to the database"""
        super().save(*args, **kwargs)


class Review(models.Model):
    """This class creates a model for department reviews
    
    Reviews must have department_id, author_id, and a body
    Some comments have parent comments to facilitate comment threading and replies
    """
    body = models.CharField(max_length=250, blank=False)
    department = models.ForeignKey(Department, related_name='reviews', on_delete=models.CASCADE, blank=False)
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, blank=False)
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        null=True,
        default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable version of model objects"""
        return self.body

    def save(self, *args, **kwargs):
        return super(Review, self).save(*args, **kwargs)
        

class Rating(models.Model):
    """Rating model"""
    user = models.ForeignKey(
        User,
        related_name="rater",
        on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        Department,
        related_name='rated_department',
        on_delete=models.CASCADE
    )

    user_rating = models.FloatField(default=0)

    def __str__(self):
        return self.user_rating