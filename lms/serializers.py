from rest_framework.serializers import ModelSerializer, SerializerMethodField
from lms.validators import YouTubeValidator
from lms.models import Course, Lesson, Subscription
from rest_framework import serializers


class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"
        video_url = serializers.CharField(validators=[YouTubeValidator()])

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseWithLessonsCountSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "preview",
            "lessons_count",
            "lessons",
        )
