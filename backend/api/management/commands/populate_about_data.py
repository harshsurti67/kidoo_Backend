from django.core.management.base import BaseCommand
from api.models import AboutPage, AboutFeature


class Command(BaseCommand):
    help = 'Populate About Us page data'

    def handle(self, *args, **options):
        # Create AboutPage content
        about_page, created = AboutPage.objects.get_or_create(
            id=1,
            defaults={
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
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created AboutPage content'))
        else:
            self.stdout.write(self.style.SUCCESS('AboutPage content already exists'))

        # Create AboutFeature data
        features_data = {
            'infrastructure': [
                {'icon': '🏫', 'title': 'Safe & Child-Friendly Campus', 'desc': 'Soft flooring, CCTV surveillance', 'order': 1},
                {'icon': '🎨', 'title': 'Thematic Classrooms', 'desc': 'Colorful, concept-based interiors', 'order': 2},
                {'icon': '🎪', 'title': 'Indoor & Outdoor Play Zones', 'desc': 'Slides, seesaw, tunnel, horses, magic scooter & nature garden', 'order': 3},
                {'icon': '💻', 'title': 'Smart Class Technology', 'desc': 'Interactive boards, AR/VR-based learning', 'order': 4},
                {'icon': '🪑', 'title': 'Child-Sized Furniture', 'desc': 'Ergonomic tables, chairs, and cubbies', 'order': 5}
            ],
            'curriculum': [
                {'icon': '📚', 'title': 'Activity-Based Learning', 'desc': 'Montessori, play-way method', 'order': 1},
                {'icon': '🧩', 'title': 'Memory Tool Games', 'desc': 'Puzzles, coding toys', 'order': 2},
                {'icon': '🗣️', 'title': 'Language Development', 'desc': 'Phonics, storytelling, puppet shows', 'order': 3},
                {'icon': '🎭', 'title': 'Art & Creativity Corners', 'desc': 'Painting, music, dance, drama', 'order': 4},
                {'icon': '❤️', 'title': 'Life Skills & Values', 'desc': 'Manners, teamwork, empathy', 'order': 5}
            ],
            'teachers': [
                {'icon': '👩‍🏫', 'title': 'Trained & Certified Teachers', 'desc': 'ECCEd qualified with child psychology knowledge', 'order': 1},
                {'icon': '👥', 'title': 'Low Student-Teacher Ratio', 'desc': 'Personalized attention (ideal: 1:12)', 'order': 2},
                {'icon': '📖', 'title': 'Continuous Teacher Training', 'desc': 'Updated with latest methods', 'order': 3}
            ],
            'wellbeing': [
                {'icon': '🧸', 'title': 'Child Counselling & Assessments', 'desc': 'Regular progress tracking', 'order': 1},
                {'icon': '🍎', 'title': 'Healthy Meals & Nutrition Plans', 'desc': 'Dietician-approved menus', 'order': 2},
                {'icon': '✨', 'title': 'Hygiene & Wellness Practices', 'desc': 'Sanitized classrooms, regular health checkups', 'order': 3}
            ],
            'enrichment': [
                {'icon': '🌳', 'title': 'Field Trips & Nature Walks', 'desc': 'Practical learning experiences', 'order': 1},
                {'icon': '🎉', 'title': 'Festivals & Cultural Celebrations', 'desc': 'Diversity & tradition', 'order': 2},
                {'icon': '👨‍👩‍👧', 'title': 'Parent Engagement', 'desc': 'Workshops, parent-child activities', 'order': 3},
                {'icon': '🌍', 'title': 'Global Curriculum Elements', 'desc': 'Exposure to languages & cultures', 'order': 4}
            ],
            'innovative': [
                {'icon': '📱', 'title': 'AI & Smart Learning Apps', 'desc': 'Track school activities via parent app', 'order': 1},
                {'icon': '🧘', 'title': 'Skill-Based Clubs', 'desc': 'Yoga, dance, storytelling clubs, Art & craft', 'order': 2},
                {'icon': '📹', 'title': 'CCTV Live Access for Parents', 'desc': 'Transparent monitoring', 'order': 3}
            ]
        }

        created_count = 0
        for category, features in features_data.items():
            for feature_data in features:
                feature, created = AboutFeature.objects.get_or_create(
                    category=category,
                    title=feature_data['title'],
                    defaults={
                        'icon': feature_data['icon'],
                        'description': feature_data['desc'],
                        'order': feature_data['order'],
                        'is_active': True
                    }
                )
                if created:
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} AboutFeature items')
        )
        self.stdout.write(
            self.style.SUCCESS('About Us data population completed!')
        )
