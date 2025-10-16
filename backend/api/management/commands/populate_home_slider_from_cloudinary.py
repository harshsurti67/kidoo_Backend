from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import HomeSlider
import cloudinary
from cloudinary import api as cloudinary_api


class Command(BaseCommand):
    help = "Populate HomeSlider with a few recent Cloudinary images for testing."

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=3, help='Number of images to import')

    def handle(self, *args, **options):
        count = options['count']

        # Fetch recent uploaded images from Cloudinary
        self.stdout.write(self.style.WARNING('Fetching recent images from Cloudinary...'))
        result = cloudinary_api.resources(type='upload', resource_type='image', max_results=count, order='desc')
        resources = result.get('resources', [])

        if not resources:
            self.stdout.write(self.style.ERROR('No Cloudinary images found to import.'))
            return

        created_any = False
        for idx, res in enumerate(resources, start=1):
            title = res.get('public_id').split('/')[-1]
            secure_url = res.get('secure_url') or res.get('url')
            if not secure_url:
                continue

            slider, created = HomeSlider.objects.get_or_create(
                title=f"Cloudinary Test {title}",
                defaults={
                    'subtitle': 'Cloudinary test slide',
                    'media_type': 'image',
                    'order': idx,
                    'is_active': True,
                    'button_text': 'Learn More',
                    'button_url': '/programs',
                }
            )

            # Assign the secure URL directly to the ImageField; Cloudinary storage will serve it
            if created or not slider.image:
                slider.image = secure_url
                slider.save(update_fields=['image'])
                created_any = True
                self.stdout.write(self.style.SUCCESS(f'Added slide for: {secure_url}'))
            else:
                self.stdout.write(f'Slide already exists: {slider.title}')

        if created_any:
            self.stdout.write(self.style.SUCCESS('HomeSlider has been populated with Cloudinary images.'))
        else:
            self.stdout.write('No new slides were created.')


