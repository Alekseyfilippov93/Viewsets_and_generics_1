from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_link


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        required=False,
        validators=[validate_youtube_link]
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribed(self, obj):
        request = self.context.get("request")

        if not request:
            return False

        user = request.user

        if user.is_anonymous:
            return False

        return Subscription.objects.filter(
            user=user,
            course=obj
        ).exists()
