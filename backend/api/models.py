from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import os


def validate_video_duration(value):
    """Validate that video is not longer than 15 seconds"""
    try:
        import cv2
        cap = cv2.VideoCapture(value.path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 0
        cap.release()
        
        if duration > 15:
            raise ValidationError(f'Video duration is {duration:.1f} seconds. Maximum allowed duration is 15 seconds.')
    except ImportError:
        # If OpenCV is not available, skip duration validation
        pass
    except Exception as e:
        # If there's any error reading the video, allow it to pass
        # The file format validation will catch invalid files
        pass


def validate_video_file_size(value):
    """Validate that video file is not larger than 50MB"""
    max_size = 50 * 1024 * 1024  # 50MB
    if value.size > max_size:
        raise ValidationError(f'Video file size is {value.size / (1024*1024):.1f}MB. Maximum allowed size is 50MB.')


class Program(models.Model):
    name = models.CharField(max_length=200)
    age_group = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='programs/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Gallery(models.Model):
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    CATEGORY_CHOICES = [
        ('Activities', 'Activities'),
        ('Playground', 'Playground'),
        ('Music', 'Music'),
        ('Reading', 'Reading'),
        ('Science', 'Science'),
        ('Cooking', 'Cooking'),
    ]
    
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    # image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    # video_url = models.URLField(blank=True, null=True, help_text="URL for video (YouTube, Vimeo, etc.)")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Activities')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Gallery Items'

    def __str__(self):
        return self.title
    
    @property
    def url(self):
        """Return image URL or video URL based on type"""
        if self.type == 'image' and self.image:
            return self.image.url
        elif self.type == 'video' and self.video_url:
            return self.video_url
        return None


class Testimonial(models.Model):
    parent_name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)  # e.g., "Mother of Sarah"
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    message = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.parent_name} - {self.relation}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title


class Branch(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    map_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    parent_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    child_age = models.IntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"Inquiry from {self.parent_name}"


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='team/', max_length=500)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.role}"


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'question']

    def __str__(self):
        return self.question


class Setting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['key']

    def __str__(self):
        return f"{self.key}: {self.value}"


class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="About Kiddoo Preschool")
    subtitle = models.TextField(default="By Aarya International School - Nurturing young minds with world-class facilities, innovative curriculum, and experienced educators")
    mission_title = models.CharField(max_length=200, default="Our Mission")
    mission_content = models.TextField()
    vision_title = models.CharField(max_length=200, default="Our Vision")
    vision_content = models.TextField()
    cta_title = models.CharField(max_length=200, default="Join the Kiddoo Family Today!")
    cta_content = models.TextField()
    cta_button_text = models.CharField(max_length=100, default="Enroll Your Child Now")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"

    def __str__(self):
        return "About Page Content"


class AboutFeature(models.Model):
    CATEGORY_CHOICES = [
        ('infrastructure', 'Infrastructure & Environment'),
        ('curriculum', 'Curriculum & Learning'),
        ('teachers', 'Teachers & Staff'),
        ('wellbeing', 'Child Development & Well-Being'),
        ('enrichment', 'Exposure & Enrichment'),
        ('innovative', 'Innovative Add-Ons'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=10, help_text="Emoji or icon character")
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0, help_text="Order within category")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'order', 'title']
        verbose_name = "About Feature"
        verbose_name_plural = "About Features"

    def __str__(self):
        return f"{self.get_category_display()} - {self.title}"


class HomeSlider(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, help_text="Main heading for the slide")
    subtitle = models.TextField(help_text="Subtitle or description text")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image', help_text="Type of media for the slide")
    image = models.ImageField(upload_to='home_slider/', blank=True, null=True, help_text="Background image for the slide")
    video = models.FileField(
        upload_to='home_slider/videos/', 
        blank=True, 
        null=True, 
        help_text="Background video for the slide (max 15 seconds, MP4 format, max 50MB)",
        validators=[
            FileExtensionValidator(allowed_extensions=['mp4']),
            validate_video_file_size
        ]
    )
    video_poster = models.ImageField(upload_to='home_slider/posters/', blank=True, null=True, help_text="Poster image for video (shown before video loads)")
    button_text = models.CharField(max_length=100, default="Learn More", help_text="Text for the call-to-action button")
    button_url = models.CharField(max_length=200, default="/programs", help_text="URL to redirect when button is clicked")
    order = models.IntegerField(default=0, help_text="Order of display (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Whether this slide is active and should be displayed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Home Slider"
        verbose_name_plural = "Home Sliders"

    def __str__(self):
        return f"{self.title} (Order: {self.order})"
    
    @property
    def media_url(self):
        """Return image URL or video URL based on media type"""
        if self.media_type == 'image' and self.image:
            return self.image.url
        elif self.media_type == 'video' and self.video:
            return self.video.url
        return None
    
    @property
    def poster_url(self):
        """Return poster image URL for videos"""
        if self.media_type == 'video' and self.video_poster:
            return self.video_poster.url
        return None


class HomeStats(models.Model):
    STAT_TYPE_CHOICES = [
        ('students', 'Happy Students'),
        ('branches', 'Branches'),
        ('awards', 'Awards Won'),
        ('teachers', 'Expert Teachers'),
        ('years', 'Years Experience'),
        ('satisfaction', 'Parent Satisfaction'),
    ]
    
    stat_type = models.CharField(max_length=20, choices=STAT_TYPE_CHOICES, unique=True)
    value = models.IntegerField(help_text="The numeric value to display")
    label = models.CharField(max_length=100, help_text="Display label for the stat")
    suffix = models.CharField(max_length=10, default='', help_text="Suffix to add (e.g., '+', '%', '')")
    icon = models.CharField(max_length=50, default='FaUsers', help_text="Icon name from react-icons/fa")
    color = models.CharField(max_length=50, default='var(--primary-blue)', help_text="CSS color variable or hex code")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Whether this stat is active and should be displayed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'stat_type']
        verbose_name = "Home Stat"
        verbose_name_plural = "Home Stats"

    def __str__(self):
        return f"{self.get_stat_type_display()} - {self.value}{self.suffix}"


class Admission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
    ]
    
    PROGRAM_CHOICES = [
        ('toddler', 'Toddler Program (2-3 years)'),
        ('preschool', 'Preschool Program (3-4 years)'),
        ('pre_k', 'Pre-K Program (4-5 years)'),
    ]
    
    # Student Information
    student_first_name = models.CharField(max_length=100)
    student_last_name = models.CharField(max_length=100)
    student_date_of_birth = models.DateField()
    student_gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    
    # Parent/Guardian Information
    parent_first_name = models.CharField(max_length=100)
    parent_last_name = models.CharField(max_length=100)
    parent_email = models.EmailField()
    parent_phone = models.CharField(max_length=20)
    parent_relationship = models.CharField(max_length=50, default='Parent')
    
    # Additional Contact Information
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relationship = models.CharField(max_length=50)
    
    # Address Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    
    # Program Information
    preferred_program = models.CharField(max_length=20, choices=PROGRAM_CHOICES)
    preferred_start_date = models.DateField()
    current_school = models.CharField(max_length=200, blank=True, null=True)
    
    # Medical Information
    medical_conditions = models.TextField(blank=True, null=True, help_text="Any medical conditions or allergies")
    medications = models.TextField(blank=True, null=True, help_text="Current medications")
    emergency_medical_consent = models.BooleanField(default=True)
    
    # Additional Information
    special_needs = models.TextField(blank=True, null=True, help_text="Any special needs or accommodations required")
    previous_preschool_experience = models.TextField(blank=True, null=True)
    why_choose_us = models.TextField(blank=True, null=True, help_text="Why do you want to enroll your child at Kiddoo Preschool?")
    
    # Application Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True, help_text="Internal notes for staff")
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Admission Application"
        verbose_name_plural = "Admission Applications"

    def __str__(self):
        return f"{self.student_first_name} {self.student_last_name} - {self.get_status_display()}"
    
    @property
    def student_full_name(self):
        return f"{self.student_first_name} {self.student_last_name}"
    
    @property
    def parent_full_name(self):
        return f"{self.parent_first_name} {self.parent_last_name}"