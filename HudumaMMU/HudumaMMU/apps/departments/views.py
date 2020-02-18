from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import DepartmentSerializers, ReviewSerializer, RatingSerializer
from .models import Department, Review, Rating



# Create your views here.
def get_department(id):
    try:
        department = Department.objects.get(id=id)
        return department
    except Department.DoesNotExist:
        raise NotFound(
    {
        "error": "Department not found"
    })

class DepartmentViewSet(viewsets.ViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthenticated, )



    def list(self, request):
        queryset = Department.objects.all()
        serializer = DepartmentSerializers(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        """create a department"""
        department = request.data
        serializer = self.serializer_class(
            data=department, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Return department when selected with Id"""
        queryset = Department.objects.all()
        department = get_object_or_404(queryset, pk=pk)
        serializer = DepartmentSerializers(department, context={'request': request})
        return Response(serializer.data)


    def update(self, request, pk):
        """update department"""
        queryset = Department.objects.all()
        department = get_object_or_404(queryset, pk=pk)
        department_data = request.data
        serializer = self.serializer_class(instance = department,
            data=department_data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def partial_update(self, request, pk=None):
        queryset = Department.object.all()
        department = get_object_or_404(queryset, pk=pk)
        department_data = request.data
        serializer = self.serializer_class(
            instance=department, data=department_data, partial=True,
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        """delete a department"""
        queryset = Department.objects.all()
        department = get_object_or_404(queryset, pk=pk)
        department.delete()
        return Response({
            "message": "Department deleted successfully"
        },
        status=status.HTTP_200_OK)

        

class ReviewViewSet(viewsets.ViewSet):
    """Class to handle review route'
    One can post a review, retrieve all, retrieve one, update,
    delete reviews
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_specific_review(self, department_id, review_id, request):
        """This methos a single review related to a specific department"""
        get_department(department_id)
        try:
            review = Review.objects.filter(pk=review_id,
                                             department_id=department_id).first()
        except Exception:
            raise NotFound("Error when retrieving review")

        if not review:
            return Response({"error": "Review does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        return review

    def list(self, request, **kwargs):
        """This is the endpoint to view all department reviews"""
        department_id = self.kwargs['pk']
        get_department(department_id)

        try:
            reviews = Review.objects.filter(department_id=department_id,
                                              parent=None).order_by(
                '-created_at')
        except Exception:
            return Response({"error": "No reviews found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(reviews, many=True)
        return Response(
            {
                'Reviews': serializer.data
            }
        )

    def create(self, request, **kwargs):
        """This is the view for creating a new review"""
        department_id = self.kwargs['pk']
        department = get_department(department_id)

        review = request.data
        serializer = self.serializer_class(
            data=review, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(department=department, author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, id, **kwargs):
        """This is the view for updating a review"""
        department_id = self.kwargs['pk']
        review = self.get_specific_review(
            department_id, id, request
        )
        if isinstance(review, Response):
            return review
        serializer = self.serializer_class(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, id, **kwargs):
        """This is the view for updating a review"""
        department_id = self.kwargs['pk']
        review = self.get_specific_review(
            department_id, id, request
        )
        if isinstance(review, Response):
            return review
        if review.author.id != request.user.id:
            return Response({
                "error": "You are not the author of this review"
            },
                status=status.HTTP_401_UNAUTHORIZED)
        review_data = request.data
        serializer = self.serializer_class(
            instance=review, data=review_data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, id, **kwargs):
        """This is the view for deleting a review"""
        department_id = self.kwargs['pk']
        review = self.get_specific_review(
            department_id, id, request
        )
        if isinstance(review, Response):
            return review
        if review.author.id != request.user.id:
            return Response({
                "error": "You are not the author of this review"
            },
                status=status.HTTP_401_UNAUTHORIZED)
        review.delete()
        return Response({
            "message": "Review deleted successfully"
        },
            status=status.HTTP_200_OK)

    def create_reply(self, request, id, **kwargs):
        """This is the view that handles creation of child reviews"""
        department_id = self.kwargs['pk']
        review = self.get_specific_review(
            department_id, id, request
        )
        if isinstance(review, Response):
            return review
        review_data = request.data
        department = Department.objects.get(pk=department_id)
        serializer = self.serializer_class(
            data=review_data, context={'request': request}
        )
        if review.parent:
            return Response({
                "error": "You cannot reply to this review"
            },
                status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.save(department=department, author=request.user, parent=review)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RatingAPIView(GenericAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, id):
        """POST request to rate an department."""
        rating = request.data
        department = get_department(id)

        if request.user.id == department.created_by.id:
            return Response({
                "message": "You cannot rate your own department"
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            current_rating = Rating.objects.get(
                user=request.user.id,
                department=department
            )
            serializer = self.serializer_class(
                current_rating, data=rating)
        except Rating.DoesNotExist:
            serializer = self.serializer_class(data=rating)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, department=department)

        return Response({
            'message': 'Rating submitted sucessfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, id):
        """Get request for an department ratings."""
        rating = None
        department = get_department(id)

        try:
            rating = Rating.objects.get(user=request.user, department=department)
        except Exception:
            rating = None

        if rating is None:
            avg = Rating.objects.filter(
                department=department).aggregate(Avg('user_rating'))
            average_rating = avg['user_rating__avg']
            if avg["user_rating__avg"] is None:
                average_rating = 0

            if request.user.is_authenticated is False:
                return Response({
                    'department_id': department.id,
                    'average_rating': average_rating,
                    'user_rating': 'login to rate the department'
                }, status=status.HTTP_200_OK)

            return Response({
                'message': 'department rating',
                'data': {
                    "department_id": department.id,
                    'average_rating': average_rating,
                    'user_rating': 'you have not rated this department'
                }
            }, status=status.HTTP_200_OK)

        serialized_data = self.serializer_class(rating)
        return Response({
            'message': 'department rating',
            'data': serialized_data.data
        }, status=status.HTTP_200_OK)