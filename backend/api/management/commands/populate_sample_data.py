from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
from api.models import (
    Program, Gallery, Testimonial, Event, Branch, 
    Blog, TeamMember, FAQ, Setting
)


class Command(BaseCommand):
    help = 'Populate the database with sample data for Kidoo Preschool'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate sample data...'))
        
        # Create sample data for each model
        self.create_programs()
        self.create_gallery()
        self.create_testimonials()
        self.create_events()
        self.create_branches()
        self.create_blogs()
        self.create_team_members()
        self.create_faqs()
        self.create_settings()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated sample data!'))

    def create_programs(self):
        """Create sample programs"""
        programs_data = [
            {
                'name': 'Toddler Program',
                'age_group': '2-3',
                'description': 'A nurturing environment for toddlers to explore, learn, and grow through play-based activities. Our toddler program focuses on developing motor skills, language, and social interaction.',
                'image': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Preschool Program',
                'age_group': '3-4',
                'description': 'Comprehensive early childhood education focusing on social, emotional, and cognitive development. Children learn through structured play and hands-on activities.',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Pre-K Program',
                'age_group': '4-5',
                'description': 'Advanced preparation for kindergarten with emphasis on literacy, math, and critical thinking skills. Our Pre-K program ensures children are ready for school success.',
                'image': 'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Summer Camp',
                'age_group': '3-6',
                'description': 'Fun-filled summer activities including arts and crafts, outdoor play, water activities, and educational games. Perfect for keeping children engaged during summer break.',
                'image': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'After School Care',
                'age_group': '5-8',
                'description': 'Safe and supervised after-school care with homework help, snacks, and recreational activities. We provide a comfortable environment for children after school hours.',
                'image': 'https://images.unsplash.com/photo-1509062522246-3755977927d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
            }
        ]
        
        for program_data in programs_data:
            program, created = Program.objects.get_or_create(
                name=program_data['name'],
                defaults=program_data
            )
            if created:
                self.stdout.write(f'Created program: {program.name}')
            else:
                self.stdout.write(f'Program already exists: {program.name}')

    def create_gallery(self):
        """Create sample gallery items"""
        gallery_data = [
            {
                'title': 'Children Playing in Garden',
                'type': 'image',
                'url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'category': 'Activities'
            },
            {
                'title': 'Art and Craft Session',
                'type': 'image',
                'url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'category': 'Activities'
            },
            {
                'title': 'Story Time',
                'type': 'image',
                'url': 'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'category': 'Learning'
            },
            {
                'title': 'Outdoor Play',
                'type': 'image',
                'url': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'category': 'Activities'
            },
            {
                'title': 'Music and Dance',
                'type': 'video',
                'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'category': 'Activities'
            },
            {
                'title': 'Science Experiment',
                'type': 'image',
                'url': 'https://images.unsplash.com/photo-1509062522246-3755977927d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'category': 'Learning'
            },
            {
                'title': 'Lunch Time',
                'type': 'image',
                'url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'category': 'Daily Life'
            },
            {
                'title': 'Nap Time',
                'type': 'image',
                'url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'category': 'Daily Life'
            }
        ]
        
        for gallery_data_item in gallery_data:
            # Convert 'url' to 'video_url' for compatibility
            item_data = gallery_data_item.copy()
            if 'url' in item_data:
                item_data['video_url'] = item_data.pop('url')
            
            # Update categories to match new choices
            if item_data['category'] == 'Learning':
                item_data['category'] = 'Reading'
            elif item_data['category'] == 'Daily Life':
                item_data['category'] = 'Activities'
            
            gallery_item, created = Gallery.objects.get_or_create(
                title=item_data['title'],
                defaults=item_data
            )
            if created:
                self.stdout.write(f'Created gallery item: {gallery_item.title}')

    def create_testimonials(self):
        """Create sample testimonials"""
        testimonials_data = [
            {
                'parent_name': 'Sarah Johnson',
                'relation': 'Mother of Emma (4 years old)',
                'rating': 5,
                'message': 'Kidoo Preschool has been amazing for our daughter Emma. The teachers are caring and professional, and Emma has learned so much in just a few months. She looks forward to going to school every day!',
                'photo': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            },
            {
                'parent_name': 'Michael Chen',
                'relation': 'Father of Alex (3 years old)',
                'rating': 5,
                'message': 'The staff at Kidoo Preschool goes above and beyond to ensure each child feels loved and supported. Alex has developed great social skills and confidence since joining.',
                'photo': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            },
            {
                'parent_name': 'Lisa Rodriguez',
                'relation': 'Mother of Sofia (5 years old)',
                'rating': 5,
                'message': 'I am so impressed with the educational programs at Kidoo Preschool. Sofia is well-prepared for kindergarten and has developed a love for learning. Highly recommended!',
                'photo': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            },
            {
                'parent_name': 'David Thompson',
                'relation': 'Father of James (4 years old)',
                'rating': 5,
                'message': 'The facilities are excellent and the curriculum is well-structured. James has made wonderful friends and the teachers are fantastic. We feel confident leaving our child in their care.',
                'photo': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            },
            {
                'parent_name': 'Jennifer Lee',
                'relation': 'Mother of Maya (3 years old)',
                'rating': 5,
                'message': 'Kidoo Preschool provides a safe, nurturing environment where children can thrive. Maya has blossomed since starting here. The communication with parents is excellent.',
                'photo': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            }
        ]
        
        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                parent_name=testimonial_data['parent_name'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(f'Created testimonial from: {testimonial.parent_name}')

    def create_events(self):
        """Create sample events"""
        events_data = [
            {
                'title': 'Spring Art Exhibition',
                'description': 'Come see the amazing artwork created by our talented students! The exhibition will showcase paintings, drawings, and crafts from all age groups.',
                'date': timezone.now() + timedelta(days=15),
                'image': 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
            },
            {
                'title': 'Parent-Teacher Conference',
                'description': 'Scheduled meetings with teachers to discuss your child\'s progress, achievements, and areas for development. Please book your appointment.',
                'date': timezone.now() + timedelta(days=20),
                'image': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
            },
            {
                'title': 'Summer Camp Registration',
                'description': 'Registration opens for our exciting summer camp program! Activities include swimming, arts and crafts, field trips, and educational games.',
                'date': timezone.now() + timedelta(days=30),
                'image': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
            },
            {
                'title': 'Graduation Ceremony',
                'description': 'Celebrate our Pre-K graduates as they prepare to enter kindergarten! A special ceremony to honor their achievements and growth.',
                'date': timezone.now() + timedelta(days=45),
                'image': 'https://images.unsplash.com/photo-1509062522246-3755977927d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
            },
            {
                'title': 'Family Fun Day',
                'description': 'Join us for a day of fun activities, games, and food! This is a great opportunity for families to connect and for children to show off their skills.',
                'date': timezone.now() + timedelta(days=60),
                'image': 'https://images.unsplash.com/photo-1511632765486-a01980e01a18?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
            }
        ]
        
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults=event_data
            )
            if created:
                self.stdout.write(f'Created event: {event.title}')

    def create_branches(self):
        """Create sample branches"""
        branches_data = [
            {
                'name': 'Downtown Campus',
                'address': '123 Main Street, Downtown, City 12345',
                'phone': '(555) 123-4567',
                'map_url': 'https://maps.google.com/?q=123+Main+Street+Downtown'
            },
            {
                'name': 'Westside Branch',
                'address': '456 Oak Avenue, Westside, City 12345',
                'phone': '(555) 234-5678',
                'map_url': 'https://maps.google.com/?q=456+Oak+Avenue+Westside'
            },
            {
                'name': 'Eastside Campus',
                'address': '789 Pine Street, Eastside, City 12345',
                'phone': '(555) 345-6789',
                'map_url': 'https://maps.google.com/?q=789+Pine+Street+Eastside'
            },
            {
                'name': 'Northside Branch',
                'address': '321 Elm Drive, Northside, City 12345',
                'phone': '(555) 456-7890',
                'map_url': 'https://maps.google.com/?q=321+Elm+Drive+Northside'
            }
        ]
        
        for branch_data in branches_data:
            branch, created = Branch.objects.get_or_create(
                name=branch_data['name'],
                defaults=branch_data
            )
            if created:
                self.stdout.write(f'Created branch: {branch.name}')

    def create_blogs(self):
        """Create sample blog posts"""
        blogs_data = [
            {
                'title': 'The Importance of Play in Early Childhood Development',
                'slug': 'importance-of-play-early-childhood',
                'excerpt': 'Discover why play is crucial for your child\'s development and how we incorporate it into our curriculum.',
                'content': '''Play is not just fun for children—it's essential for their development. At Kidoo Preschool, we understand that play is the foundation of learning.

Through play, children develop:
- Social skills and emotional intelligence
- Problem-solving abilities
- Creativity and imagination
- Physical coordination and motor skills
- Language and communication skills

Our teachers are trained to facilitate meaningful play experiences that support each child's individual growth and development. We create environments that encourage exploration, experimentation, and discovery.

Research shows that children who engage in quality play experiences are better prepared for academic success and have stronger social-emotional skills. That's why play is at the heart of everything we do at Kidoo Preschool.''',
                'image': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            },
            {
                'title': 'Preparing Your Child for Kindergarten',
                'slug': 'preparing-child-kindergarten',
                'excerpt': 'Learn about the essential skills your child needs for kindergarten success and how our Pre-K program helps.',
                'content': '''Kindergarten readiness is about more than just knowing letters and numbers. It's about developing the whole child—socially, emotionally, and academically.

Key areas of kindergarten readiness include:

**Social-Emotional Skills:**
- Following directions and routines
- Working independently and in groups
- Managing emotions and conflicts
- Showing respect for others

**Academic Foundations:**
- Basic letter and number recognition
- Fine motor skills for writing
- Listening and comprehension skills
- Problem-solving abilities

**Physical Development:**
- Gross motor skills for playground activities
- Fine motor skills for writing and cutting
- Self-care skills like dressing and eating

Our Pre-K program is specifically designed to prepare children for kindergarten success. We focus on building confidence, independence, and a love for learning that will serve them throughout their educational journey.''',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            },
            {
                'title': 'Healthy Eating Habits for Preschoolers',
                'slug': 'healthy-eating-habits-preschoolers',
                'excerpt': 'Tips for encouraging healthy eating habits in young children and how we promote nutrition at our preschool.',
                'content': '''Developing healthy eating habits early in life sets the foundation for lifelong wellness. At Kidoo Preschool, we're committed to promoting good nutrition and healthy eating habits.

**Our Approach to Nutrition:**

We provide balanced, nutritious meals and snacks that include:
- Fresh fruits and vegetables
- Whole grains and lean proteins
- Limited processed foods and sugars
- Plenty of water throughout the day

**Teaching Healthy Habits:**

Our teachers help children learn about:
- Different food groups and their benefits
- Trying new foods and flavors
- Listening to their bodies' hunger cues
- Making healthy choices

**Tips for Parents:**

1. **Be a role model** - Children learn by watching adults
2. **Make mealtimes pleasant** - Avoid pressure and stress
3. **Offer variety** - Introduce new foods regularly
4. **Get children involved** - Let them help with meal preparation
5. **Be patient** - It can take multiple exposures for children to accept new foods

Remember, every child is different, and it's normal for preschoolers to be picky eaters. The key is to provide a variety of healthy options and create positive mealtime experiences.''',
                'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            }
        ]
        
        for blog_data in blogs_data:
            blog, created = Blog.objects.get_or_create(
                slug=blog_data['slug'],
                defaults=blog_data
            )
            if created:
                self.stdout.write(f'Created blog post: {blog.title}')

    def create_team_members(self):
        """Create sample team members"""
        team_data = [
            {
                'name': 'Dr. Sarah Williams',
                'role': 'Director & Founder',
                'bio': 'Dr. Williams has over 15 years of experience in early childhood education. She holds a Ph.D. in Child Development and is passionate about creating nurturing learning environments.',
                'photo': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'
            },
            {
                'name': 'Ms. Jennifer Martinez',
                'role': 'Lead Teacher - Pre-K',
                'bio': 'Ms. Martinez has been teaching for 10 years and specializes in kindergarten readiness. She creates engaging lesson plans that prepare children for academic success.',
                'photo': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'
            },
            {
                'name': 'Mr. David Johnson',
                'role': 'Lead Teacher - Preschool',
                'bio': 'Mr. Johnson brings creativity and enthusiasm to the classroom. He has a background in art education and loves helping children express themselves through various mediums.',
                'photo': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'
            },
            {
                'name': 'Ms. Lisa Chen',
                'role': 'Lead Teacher - Toddler Program',
                'bio': 'Ms. Chen specializes in working with our youngest learners. She has a gentle approach and creates a warm, secure environment for toddlers to explore and grow.',
                'photo': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'
            },
            {
                'name': 'Ms. Maria Rodriguez',
                'role': 'Music & Movement Specialist',
                'bio': 'Ms. Rodriguez brings the joy of music and movement to our students. She has a degree in Music Education and loves seeing children discover their rhythm and creativity.',
                'photo': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'
            },
            {
                'name': 'Mr. James Thompson',
                'role': 'Physical Education Coordinator',
                'bio': 'Mr. Thompson promotes physical fitness and healthy habits through fun activities and games. He believes that active children are happy children.',
                'photo': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'
            }
        ]
        
        for member_data in team_data:
            member, created = TeamMember.objects.get_or_create(
                name=member_data['name'],
                defaults=member_data
            )
            if created:
                self.stdout.write(f'Created team member: {member.name}')

    def create_faqs(self):
        """Create sample FAQs"""
        faqs_data = [
            {
                'question': 'What age groups do you serve?',
                'answer': 'We serve children from 2 to 6 years old. Our programs include Toddler (2-3 years), Preschool (3-4 years), and Pre-K (4-5 years). We also offer after-school care for children up to 8 years old.',
                'order': 1
            },
            {
                'question': 'What are your operating hours?',
                'answer': 'Our regular hours are Monday through Friday, 7:00 AM to 6:00 PM. We offer flexible drop-off and pick-up times to accommodate working families.',
                'order': 2
            },
            {
                'question': 'Do you provide meals and snacks?',
                'answer': 'Yes, we provide nutritious meals and snacks throughout the day. Our menu is designed by a nutritionist and includes fresh fruits, vegetables, whole grains, and lean proteins.',
                'order': 3
            },
            {
                'question': 'What is your teacher-to-student ratio?',
                'answer': 'We maintain low teacher-to-student ratios to ensure individual attention. Our ratios are: Toddler (1:4), Preschool (1:6), and Pre-K (1:8), which exceed state requirements.',
                'order': 4
            },
            {
                'question': 'How do you handle discipline?',
                'answer': 'We use positive discipline techniques that focus on teaching appropriate behavior rather than punishment. Our approach includes redirection, positive reinforcement, and helping children understand the consequences of their actions.',
                'order': 5
            },
            {
                'question': 'What safety measures do you have in place?',
                'answer': 'Safety is our top priority. We have secure entry systems, regular safety drills, trained staff in first aid and CPR, and maintain strict health and hygiene protocols.',
                'order': 6
            },
            {
                'question': 'Do you offer part-time programs?',
                'answer': 'Yes, we offer both full-time and part-time programs. Part-time options include 2, 3, or 4 days per week, and half-day or full-day schedules.',
                'order': 7
            },
            {
                'question': 'How do you communicate with parents?',
                'answer': 'We maintain regular communication through daily reports, parent-teacher conferences, newsletters, and our parent portal. We also use a mobile app for real-time updates and photos.',
                'order': 8
            },
            {
                'question': 'What is your enrollment process?',
                'answer': 'Our enrollment process includes a school tour, meeting with the director, completing enrollment forms, and providing required documentation. We recommend starting the process 2-3 months before your desired start date.',
                'order': 9
            },
            {
                'question': 'Do you offer financial assistance?',
                'answer': 'Yes, we offer various payment options and may have financial assistance available for qualifying families. Please contact our office to discuss your specific situation.',
                'order': 10
            }
        ]
        
        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
            if created:
                self.stdout.write(f'Created FAQ: {faq.question}')

    def create_settings(self):
        """Create sample settings"""
        settings_data = [
            {
                'key': 'whatsapp_number',
                'value': '+1234567890',
                'description': 'WhatsApp contact number for quick communication'
            },
            {
                'key': 'phone_number',
                'value': '(555) 123-4567',
                'description': 'Main phone number for the preschool'
            },
            {
                'key': 'email',
                'value': 'info@kidoopreschool.com',
                'description': 'Main email address for inquiries'
            },
            {
                'key': 'address',
                'value': '123 Main Street, Downtown, City 12345',
                'description': 'Main campus address'
            },
            {
                'key': 'facebook_url',
                'value': 'https://facebook.com/kidoopreschool',
                'description': 'Facebook page URL'
            },
            {
                'key': 'instagram_url',
                'value': 'https://instagram.com/kidoopreschool',
                'description': 'Instagram profile URL'
            },
            {
                'key': 'youtube_url',
                'value': 'https://youtube.com/kidoopreschool',
                'description': 'YouTube channel URL'
            },
            {
                'key': 'newsletter_signup_text',
                'value': 'Subscribe to our newsletter for updates and parenting tips!',
                'description': 'Text for newsletter signup section'
            }
        ]
        
        for setting_data in settings_data:
            setting, created = Setting.objects.get_or_create(
                key=setting_data['key'],
                defaults=setting_data
            )
            if created:
                self.stdout.write(f'Created setting: {setting.key}')
