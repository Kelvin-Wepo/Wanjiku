from django.core.management.base import BaseCommand
from services.models import GovernmentService, ServiceFAQ
from chat.models import SwahiliIntent


class Command(BaseCommand):
    help = 'Load initial data for Wanjiku 2.0'

    def handle(self, *args, **options):
        self.stdout.write('Loading initial government services...')
        
        # Government Services
        services_data = [
            {
                'name': 'Birth Certificate',
                'name_swahili': 'Cheti cha Kuzaliwa',
                'description': 'Official birth certificate for Kenyan citizens',
                'description_swahili': 'Cheti rasmi cha kuzaliwa kwa raia wa Kenya',
                'category': 'identity',
                'requirements': ['Parent ID', 'Hospital records', 'Witness'],
                'requirements_swahili': ['Kitambulisho cha mzazi', 'Rekodi za hospitali', 'Shahidi'],
                'processing_time': '7-14 days',
                'processing_time_swahili': 'Siku 7-14',
                'cost': 50.00
            },
            {
                'name': 'National ID Card',
                'name_swahili': 'Kitambulisho cha Taifa',
                'description': 'National identification card for Kenyan citizens',
                'description_swahili': 'Kitambulisho cha taifa kwa raia wa Kenya',
                'category': 'identity',
                'requirements': ['Birth certificate', 'Passport photo', 'Fingerprints'],
                'requirements_swahili': ['Cheti cha kuzaliwa', 'Picha ya pasipoti', 'Alama za vidole'],
                'processing_time': '14-21 days',
                'processing_time_swahili': 'Siku 14-21',
                'cost': 100.00
            },
            {
                'name': 'Business License',
                'name_swahili': 'Leseni ya Biashara',
                'description': 'License to operate a business in Kenya',
                'description_swahili': 'Leseni ya kufanya biashara nchini Kenya',
                'category': 'business',
                'requirements': ['Business name', 'KRA PIN', 'Location permit'],
                'requirements_swahili': ['Jina la biashara', 'Nambari ya KRA', 'Leseni ya eneo'],
                'processing_time': '21-30 days',
                'processing_time_swahili': 'Siku 21-30',
                'cost': 1000.00
            },
            {
                'name': 'Driving License',
                'name_swahili': 'Leseni ya Kuendesha',
                'description': 'License to drive motor vehicles in Kenya',
                'description_swahili': 'Leseni ya kuendesha magari nchini Kenya',
                'category': 'transport',
                'requirements': ['ID Card', 'Medical certificate', 'Test results'],
                'requirements_swahili': ['Kitambulisho', 'Cheti cha afya', 'Matokeo ya mtihani'],
                'processing_time': '14-21 days',
                'processing_time_swahili': 'Siku 14-21',
                'cost': 3000.00
            },
            {
                'name': 'Passport',
                'name_swahili': 'Pasipoti',
                'description': 'International travel document for Kenyan citizens',
                'description_swahili': 'Hati ya kusafiri kimataifa kwa raia wa Kenya',
                'category': 'identity',
                'requirements': ['ID Card', 'Birth certificate', 'Passport photo'],
                'requirements_swahili': ['Kitambulisho', 'Cheti cha kuzaliwa', 'Picha ya pasipoti'],
                'processing_time': '21-30 days',
                'processing_time_swahili': 'Siku 21-30',
                'cost': 4500.00
            }
        ]

        for service_data in services_data:
            service, created = GovernmentService.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'Created service: {service.name_swahili}')
            else:
                self.stdout.write(f'Service already exists: {service.name_swahili}')

        # Swahili Intents
        self.stdout.write('Loading Swahili intents...')
        
        intents_data = [
            {
                'intent_name': 'birth_certificate_inquiry',
                'intent_name_swahili': 'Utafiti wa Cheti cha Kuzaliwa',
                'keywords': ['cheti cha kuzaliwa', 'uzaliwa', 'birth certificate'],
                'response_template': 'To get a birth certificate, you need to visit the civil registry office with your parent\'s ID and hospital records.',
                'response_template_swahili': 'Ili kupata cheti cha kuzaliwa, unahitaji kwenda ofisi ya usajili wa raia na kitambulisho cha mzazi na rekodi za hospitali.',
                'service_category': 'identity'
            },
            {
                'intent_name': 'business_license_inquiry',
                'intent_name_swahili': 'Utafiti wa Leseni ya Biashara',
                'keywords': ['leseni ya biashara', 'biashara', 'business license'],
                'response_template': 'To get a business license, you need to register your business name, get a KRA PIN, and obtain a location permit.',
                'response_template_swahili': 'Ili kupata leseni ya biashara, unahitaji kusajili jina la biashara yako, kupata nambari ya KRA, na kupata leseni ya eneo.',
                'service_category': 'business'
            },
            {
                'intent_name': 'id_card_inquiry',
                'intent_name_swahili': 'Utafiti wa Kitambulisho',
                'keywords': ['kitambulisho', 'id card', 'kitambulisho cha taifa'],
                'response_template': 'To get a national ID card, you need your birth certificate, passport photo, and fingerprints.',
                'response_template_swahili': 'Ili kupata kitambulisho cha taifa, unahitaji cheti cha kuzaliwa, picha ya pasipoti, na alama za vidole.',
                'service_category': 'identity'
            },
            {
                'intent_name': 'driving_license_inquiry',
                'intent_name_swahili': 'Utafiti wa Leseni ya Kuendesha',
                'keywords': ['leseni ya kuendesha', 'driving license', 'kuendesha'],
                'response_template': 'To get a driving license, you need your ID card, medical certificate, and pass the driving test.',
                'response_template_swahili': 'Ili kupata leseni ya kuendesha, unahitaji kitambulisho chako, cheti cha afya, na kupita mtihani wa kuendesha.',
                'service_category': 'transport'
            },
            {
                'intent_name': 'passport_inquiry',
                'intent_name_swahili': 'Utafiti wa Pasipoti',
                'keywords': ['pasipoti', 'passport', 'kusafiri'],
                'response_template': 'To get a passport, you need your ID card, birth certificate, and passport photo.',
                'response_template_swahili': 'Ili kupata pasipoti, unahitaji kitambulisho chako, cheti cha kuzaliwa, na picha ya pasipoti.',
                'service_category': 'identity'
            }
        ]

        for intent_data in intents_data:
            intent, created = SwahiliIntent.objects.get_or_create(
                intent_name=intent_data['intent_name'],
                defaults=intent_data
            )
            if created:
                self.stdout.write(f'Created intent: {intent.intent_name_swahili}')
            else:
                self.stdout.write(f'Intent already exists: {intent.intent_name_swahili}')

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded initial data!')
        )

