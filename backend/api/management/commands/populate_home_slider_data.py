from django.core.management.base import BaseCommand
from api.models import HomeSlider

class Command(BaseCommand):
    help = 'Populates initial data for the Home Slider'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting Home Slider data population...'))

        # Clear existing slider items to avoid duplicates if re-running
        HomeSlider.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing Home Slider items.'))

        slider_data = [
            {
                'title': 'Welcome to Kiddoo Preschool',
                'subtitle': 'Where every child\'s journey begins with joy, learning, and endless possibilities. Discover our world-class facilities and nurturing environment.',
                'image': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
                'button_text': 'Explore Programs',
                'button_url': '/programs',
                'order': 1,
                'is_active': True
            },
            {
                'title': 'Nurturing Young Minds',
                'subtitle': 'Our experienced teachers and innovative curriculum create the perfect foundation for your child\'s educational journey. Join our family today!',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
                'button_text': 'Learn More',
                'button_url': '/about',
                'order': 2,
                'is_active': True
            },
            {
                'title': 'Admissions Open Now',
                'subtitle': 'Give your child the best start in life. Limited seats available for the upcoming academic year. Apply now and secure your child\'s future.',
                'image': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
                'button_text': 'Apply Now',
                'button_url': '/admissions',
                'order': 3,
                'is_active': True
            }
        ]

        slider_count = 0
        for item in slider_data:
            HomeSlider.objects.create(
                title=item['title'],
                subtitle=item['subtitle'],
                image=item['image'],
                button_text=item['button_text'],
                button_url=item['button_url'],
                order=item['order'],
                is_active=item['is_active']
            )
            slider_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {slider_count} Home Slider items'))
        self.stdout.write(self.style.SUCCESS('Home Slider data population completed!'))
