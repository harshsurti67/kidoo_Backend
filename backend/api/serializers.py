from rest_framework import serializers
from .models import (
    Program, Gallery, Testimonial, Event, Branch, 
    Inquiry, Blog, TeamMember, FAQ, Setting,
    AboutPage, AboutFeature, HomeSlider, HomeStats, Admission
)


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Gallery
        fields = ['id', 'title', 'type', 'url', 'category', 'created_at']
    
    def get_url(self, obj):
        """Return the appropriate URL based on type"""
        request = self.context.get('request')
        if obj.type == 'image' and obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        elif obj.type == 'video' and obj.video_url:
            return obj.video_url
        return None


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'

    def create(self, validated_data):
        return Inquiry.objects.create(**validated_data)


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'


class AboutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage
        fields = '__all__'


class AboutFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutFeature
        fields = '__all__'


class HomeSliderSerializer(serializers.ModelSerializer):
    media_url = serializers.SerializerMethodField()
    poster_url = serializers.SerializerMethodField()
    
    class Meta:
        model = HomeSlider
        fields = '__all__'
    
    def get_media_url(self, obj):
        """Return the appropriate media URL based on media type"""
        request = self.context.get('request')
        if obj.media_type == 'image' and obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        elif obj.media_type == 'video' and obj.video:
            if request:
                return request.build_absolute_uri(obj.video.url)
            return obj.video.url
        return None
    
    def get_poster_url(self, obj):
        """Return poster image URL for videos"""
        request = self.context.get('request')
        if obj.media_type == 'video' and obj.video_poster:
            if request:
                return request.build_absolute_uri(obj.video_poster.url)
            return obj.video_poster.url
        return None


class HomeStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeStats
        fields = '__all__'


class AdmissionSerializer(serializers.ModelSerializer):
    student_full_name = serializers.ReadOnlyField()
    parent_full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Admission
        fields = '__all__'
        read_only_fields = ['submitted_at', 'updated_at', 'reviewed_at', 'reviewed_by']
