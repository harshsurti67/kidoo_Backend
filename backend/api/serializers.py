from rest_framework import serializers
from .models import (
    Program, Gallery, Testimonial, Event, Branch, 
    Inquiry, Blog, TeamMember, FAQ, Setting,
    AboutPage, AboutFeature, HomeSlider, HomeStats, Admission
)
def _normalize_media_url(url: str) -> str:
    """Improved URL normalization for Cloudinary storage.
    Handles various URL formats and prevents double-prefixing issues.
    """
    if not url:
        return url
    
    # If it's already a complete Cloudinary URL, return as-is
    if url.startswith('https://res.cloudinary.com/'):
        return url
    
    # If it starts with /media/, remove it
    if url.startswith('/media/'):
        url = url[7:]  # Remove '/media/'
    
    # Handle cases where Cloudinary URL is embedded in path
    cloudinary_marker = 'https://res.cloudinary.com/'
    if cloudinary_marker in url:
        start_idx = url.find(cloudinary_marker)
        return url[start_idx:]
    
    # If it's a relative path, return as-is (Cloudinary will handle it)
    return url

class ProgramSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            url = obj.image.url
            url = _normalize_media_url(url)
            return request.build_absolute_uri(url) if request and not url.startswith('http') else url
        else:
            # Provide fallback image when no image is uploaded
            return f"https://via.placeholder.com/400x300?text={obj.name.replace(' ', '+')}"


class GallerySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Gallery
        fields = ['id', 'title', 'type', 'url', 'category', 'created_at']
    
    def get_url(self, obj):
        """Return the appropriate URL based on type"""
        request = self.context.get('request')
        if obj.type == 'image' and obj.image:
            url = _normalize_media_url(obj.image.url)
            if request and not url.startswith('http'):
                return request.build_absolute_uri(url)
            return url
        elif obj.type == 'video' and obj.video_url:
            return obj.video_url
        elif obj.type == 'image':
            # Provide fallback image when no image is uploaded
            return f"https://via.placeholder.com/800x600?text={obj.title.replace(' ', '+')}"
        return None


class TestimonialSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = '__all__'

    def get_photo(self, obj):
        if not obj.photo:
            return None
        request = self.context.get('request')
        url = _normalize_media_url(obj.photo.url)
        return request.build_absolute_uri(url) if request and not url.startswith('http') else url


class EventSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        url = _normalize_media_url(obj.image.url)
        return request.build_absolute_uri(url) if request and not url.startswith('http') else url


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
    image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        url = _normalize_media_url(obj.image.url)
        return request.build_absolute_uri(url) if request and not url.startswith('http') else url


class TeamMemberSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = '__all__'

    def get_photo(self, obj):
        if not obj.photo:
            return None
        request = self.context.get('request')
        url = _normalize_media_url(obj.photo.url)
        return request.build_absolute_uri(url) if request and not url.startswith('http') else url


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
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = HomeSlider
        fields = '__all__'
    
    def get_media_url(self, obj):
        """Return the appropriate media URL based on media type"""
        request = self.context.get('request')
        if obj.media_type == 'image' and obj.image:
            url = _normalize_media_url(obj.image.url)
            if request and not url.startswith('http'):
                return request.build_absolute_uri(url)
            return url
        elif obj.media_type == 'video' and obj.video:
            url = _normalize_media_url(obj.video.url)
            if request and not url.startswith('http'):
                return request.build_absolute_uri(url)
            return url
        return None
    
    def get_poster_url(self, obj):
        """Return poster image URL for videos"""
        request = self.context.get('request')
        if obj.media_type == 'video' and obj.video_poster:
            url = _normalize_media_url(obj.video_poster.url)
            if request and not url.startswith('http'):
                return request.build_absolute_uri(url)
            return url
        return None

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        url = _normalize_media_url(obj.image.url)
        if request and not url.startswith('http'):
            return request.build_absolute_uri(url)
        return url
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
