from django.core.management.base import BaseCommand
from api.models import FAQ

class Command(BaseCommand):
    help = 'Populates initial data for the FAQ'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting FAQ data population...'))

        # Clear existing FAQs to avoid duplicates if re-running
        FAQ.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing FAQ items.'))

        faq_data = [
            {
                'question': 'What age groups do you accept?',
                'answer': 'We accept children from 2 to 5 years old. We have programs for Toddlers (2-3 years), Preschool (3-4 years), and Pre-K (4-5 years).',
                'order': 1
            },
            {
                'question': 'What are your operating hours?',
                'answer': 'Our regular hours are Monday through Friday, 7:00 AM to 6:00 PM. We offer both full-day and half-day programs to accommodate different family needs.',
                'order': 2
            },
            {
                'question': 'Do you provide meals and snacks?',
                'answer': 'Yes, we provide nutritious meals and snacks throughout the day. Our menu is designed by a nutritionist and includes fresh fruits, vegetables, and balanced meals.',
                'order': 3
            },
            {
                'question': 'What is your teacher-to-student ratio?',
                'answer': 'We maintain low teacher-to-student ratios to ensure individual attention: 1:6 for toddlers, 1:8 for preschool, and 1:10 for pre-K.',
                'order': 4
            },
            {
                'question': 'Do you offer financial assistance?',
                'answer': 'Yes, we offer need-based financial assistance and accept various childcare subsidy programs. Please contact our office for more information about available options.',
                'order': 5
            },
            {
                'question': 'What safety measures do you have in place?',
                'answer': 'We have comprehensive safety protocols including secure entry systems, regular safety drills, background-checked staff, and a nurse on-site during school hours.',
                'order': 6
            },
            {
                'question': 'How do you handle special needs children?',
                'answer': 'We welcome children with special needs and work with families to create individualized support plans. Our staff is trained in inclusive education practices.',
                'order': 7
            },
            {
                'question': 'What is your policy on sick children?',
                'answer': 'We follow strict health guidelines to protect all children. Children with fever, contagious illnesses, or other symptoms must stay home until they are symptom-free for 24 hours.',
                'order': 8
            }
        ]

        faq_count = 0
        for item in faq_data:
            FAQ.objects.create(
                question=item['question'],
                answer=item['answer'],
                order=item['order']
            )
            faq_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {faq_count} FAQ items'))
        self.stdout.write(self.style.SUCCESS('FAQ data population completed!'))
