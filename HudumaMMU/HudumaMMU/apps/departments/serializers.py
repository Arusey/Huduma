from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from .models import User
from .models import Department, Review, Rating




class DepartmentSerializers(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        max_length =500,
        error_messages={
            'required': 'name cannot be empty',
            'max_length': 'name cannot exceed 500 characters'
        }
    )

    service = serializers.CharField(
        required=False,
        max_length=1000,
        error_messages={
            'max_length': 'description cannot exceed 1000 characters'
        }
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
                queryset=User.objects.all(),
                message='user with this email already exists.'
            )
            ],
        error_messages={
            'required': 'Ensure the email is inserted',
            'invalid': 'Enter a valid email address.'
        }
    )
    class Meta:
        model = Department
        fields = ('name', 'service', 'email', 'phone_number', 'image', 'created_by')


class ReviewSerializer(serializers.ModelSerializer):
    """This is a serializer for the reviews
    body is a required input
    """

    author_id = serializers.SerializerMethodField()
    department_id = serializers.SerializerMethodField()
    body = serializers.CharField(
        required=True,
        max_length=250,
        error_messages={
            'required': 'The review body cannot be empty'
        }
    )

    def format_date(self, date):
        return date.strftime('%d %b %Y %H:%M:%S')

    def create_children(self, instance):
        children = [
            {
                'id': thread.id,
                'body': thread.body,
                'author': thread.author.email,
                'created_at': self.format_date(thread.created_at),
                'updated_at': self.format_date(thread.updated_at)
            } for thread in instance.children.all()
        ]
        return children

    def to_representation(self, instance):
        """For custom output"""

        children = self.create_children(instance)

        representation = super(ReviewSerializer,
                               self).to_representation(instance)
        representation['created_at'] = self.format_date(instance.created_at)
        representation['updated_at'] = self.format_date(instance.updated_at)
        representation['author'] = instance.author.email
        representation['department'] = instance.department.name
        representation['reply_count'] = instance.children.count()
        representation['children'] = children

        return representation

    class Meta:
        model = Review
        fields = (
            'id', 'department_id', 'body', 'author_id', 'created_at',
            'updated_at', 'children'
        )
        read_only_fields = (
            'id', 'created_at', 'updated_at', 'department_id',
            'author_id', 'parent', 'children'
        )

    def get_author_id(self, obj):
        """Return author username"""
        return obj.author.id

    def get_department_id(self, obj):
        """Return department """
        return obj.department.id

    def create(self, validated_data):
        return Review.objects.create(**validated_data)


class RatingSerializer(serializers.ModelSerializer):
    """Serializers for the rating model"""
    max_rating = 5
    min_rating = 1

    user_rating = serializers.FloatField(
        required=True,
        validators=[
            MinValueValidator(
                min_rating, message="The minimum allowed rating is 1"),
            MaxValueValidator(
                max_rating, message="The maximum allowed rating is 5")
        ],
        error_messages={
            "required": "Please provide a rating between 1 and 5"
        }
    )

    department_id = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_department_id(self, obj):
        """Returns the department's id"""
        return obj.department.id

    def get_average_rating(self, obj):
        """Returns the average rating for a department"""
        average_rating = Rating.objects.filter(
            department=obj.department).aggregate(Avg('user_rating'))
        return average_rating["user_rating__avg"]

    class Meta:
        model = Rating
        fields = ("department_id", "user_rating", "average_rating")