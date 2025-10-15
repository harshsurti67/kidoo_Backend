from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    Program, Gallery, Testimonial, Event, Branch, 
    Inquiry, Blog, TeamMember, FAQ, Setting,
    AboutPage, AboutFeature, HomeSlider, HomeStats, Admission
)
from .serializers import (
    ProgramSerializer, GallerySerializer, TestimonialSerializer, 
    EventSerializer, BranchSerializer, InquirySerializer, 
    BlogSerializer, TeamMemberSerializer, FAQSerializer, SettingSerializer,
    AboutPageSerializer, AboutFeatureSerializer, HomeSliderSerializer, HomeStatsSerializer, AdmissionSerializer
)


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'category']
    search_fields = ['title', 'category']
    ordering_fields = ['title', 'created_at']
    
    def get_serializer_context(self):
        """Pass request to serializer for building absolute URLs"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['rating', 'created_at']


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'created_at']

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        from django.utils import timezone
        upcoming_events = Event.objects.filter(date__gte=timezone.now())
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)


class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'address']
    ordering_fields = ['name']


class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    http_method_names = ['post']  # Only allow POST for creating inquiries

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Inquiry submitted successfully!'}, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['created_at', 'title']

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        blog = self.get_object()
        related_blogs = Blog.objects.exclude(pk=blog.pk)[:3]
        serializer = self.get_serializer(related_blogs, many=True)
        return Response(serializer.data)


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'role']
    ordering_fields = ['name', 'created_at']


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['question', 'answer']
    ordering_fields = ['order', 'question']


class SettingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['key', 'value']
    ordering_fields = ['key']


class AboutPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    
    def list(self, request, *args, **kwargs):
        # Return the first (and only) AboutPage instance
        about_page = AboutPage.objects.first()
        if about_page:
            serializer = self.get_serializer(about_page)
            return Response(serializer.data)
        else:
            # Return default content if no AboutPage exists
            default_data = {
                'title': 'About Kiddoo Preschool',
                'subtitle': 'By Aarya International School - Nurturing young minds with world-class facilities, innovative curriculum, and experienced educators',
                'mission_title': 'Our Mission',
                'mission_content': 'To provide a safe, nurturing, and stimulating environment where children can grow, learn, and develop their full potential through activity-based learning, innovative teaching methods, and personalized attention. We create a foundation for lifelong learning and success.',
                'vision_title': 'Our Vision',
                'vision_content': 'To be recognized as the leading preschool that nurtures young minds through world-class infrastructure, innovative curriculum, and experienced educators. We aim to create confident, compassionate, and globally-aware individuals ready to excel in an ever-changing world.',
                'cta_title': 'Join the Kiddoo Family Today!',
                'cta_content': 'Give your child the best start in life with our world-class facilities and nurturing environment',
                'cta_button_text': 'Enroll Your Child Now'
            }
            return Response(default_data)


class AboutFeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutFeature.objects.filter(is_active=True)
    serializer_class = AboutFeatureSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['order', 'title']
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get features grouped by category"""
        features = self.get_queryset()
        grouped_features = {}
        
        for feature in features:
            category = feature.category
            if category not in grouped_features:
                grouped_features[category] = []
            grouped_features[category].append(self.get_serializer(feature).data)
        
        return Response(grouped_features)


class HomeSliderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomeSlider.objects.filter(is_active=True)
    serializer_class = HomeSliderSerializer
    ordering = ['order', 'title']


class HomeStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomeStats.objects.filter(is_active=True)
    serializer_class = HomeStatsSerializer
    ordering = ['order', 'stat_type']


class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'preferred_program', 'student_gender']
    search_fields = ['student_first_name', 'student_last_name', 'parent_first_name', 'parent_last_name', 'parent_email']
    ordering_fields = ['submitted_at', 'student_first_name', 'student_last_name']
    ordering = ['-submitted_at']
    
    def get_queryset(self):
        # For public submissions, only allow creating new applications
        if self.action == 'create':
            return Admission.objects.none()
        # For admin access, return all applications
        return super().get_queryset()
