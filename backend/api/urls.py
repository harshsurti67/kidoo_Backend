from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProgramViewSet, GalleryViewSet, TestimonialViewSet, EventViewSet,
    BranchViewSet, InquiryViewSet, BlogViewSet, TeamMemberViewSet,
    FAQViewSet, SettingViewSet, AboutPageViewSet, AboutFeatureViewSet,
    HomeSliderViewSet, HomeStatsViewSet, AdmissionViewSet
)

router = DefaultRouter()
router.register(r'programs', ProgramViewSet)
router.register(r'gallery', GalleryViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'events', EventViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'inquiries', InquiryViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'team', TeamMemberViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'settings', SettingViewSet)
router.register(r'about-page', AboutPageViewSet)
router.register(r'about-features', AboutFeatureViewSet)
router.register(r'home-slider', HomeSliderViewSet)
router.register(r'home-stats', HomeStatsViewSet)
router.register(r'admissions', AdmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
