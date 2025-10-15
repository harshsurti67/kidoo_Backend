from django.core.management.base import BaseCommand
from api.models import HomeStats

class Command(BaseCommand):
    help = 'Populates initial data for the Home Stats'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting Home Stats data population...'))

        # Clear existing stats to avoid duplicates if re-running
        HomeStats.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing Home Stats items.'))

        stats_data = [
            {
                'stat_type': 'students',
                'value': 500,
                'label': 'Happy Students',
                'suffix': '+',
                'icon': 'FaUsers',
                'color': 'var(--primary-blue)',
                'order': 1,
                'is_active': True
            },
            {
                'stat_type': 'branches',
                'value': 8,
                'label': 'Branches',
                'suffix': '',
                'icon': 'FaSchool',
                'color': 'var(--secondary-teal)',
                'order': 2,
                'is_active': True
            },
            {
                'stat_type': 'awards',
                'value': 25,
                'label': 'Awards Won',
                'suffix': '+',
                'icon': 'FaTrophy',
                'color': 'var(--warm-yellow)',
                'order': 3,
                'is_active': True
            },
            {
                'stat_type': 'teachers',
                'value': 50,
                'label': 'Expert Teachers',
                'suffix': '+',
                'icon': 'FaHeart',
                'color': 'var(--soft-pink)',
                'order': 4,
                'is_active': True
            },
            {
                'stat_type': 'years',
                'value': 15,
                'label': 'Years Experience',
                'suffix': '+',
                'icon': 'FaGraduationCap',
                'color': 'var(--accent-indigo)',
                'order': 5,
                'is_active': True
            },
            {
                'stat_type': 'satisfaction',
                'value': 98,
                'label': 'Parent Satisfaction',
                'suffix': '%',
                'icon': 'FaStar',
                'color': 'var(--primary-blue)',
                'order': 6,
                'is_active': True
            }
        ]

        stats_count = 0
        for item in stats_data:
            HomeStats.objects.create(
                stat_type=item['stat_type'],
                value=item['value'],
                label=item['label'],
                suffix=item['suffix'],
                icon=item['icon'],
                color=item['color'],
                order=item['order'],
                is_active=item['is_active']
            )
            stats_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {stats_count} Home Stats items'))
        self.stdout.write(self.style.SUCCESS('Home Stats data population completed!'))
