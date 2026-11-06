import os
import django
import uuid
from datetime import date, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traceback_bd.settings')
django.setup()

from accounts.models import User
from items.models import Category, ItemReport, ClaimRequest
from custody.models import LostFoundDesk, CustodyRecord, CustodyLog
from matching.engine import run_ai_matching_for_item


def seed_database():
    print("[*] Seeding TraceBack AI database with authentic DIU student belongings...")

    # 1. Create Users
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@traceback.ai',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'is_verified_staff': True,
            'institution_name': 'TraceBack AI Central Moderation',
            'phone': '01711-000001',
        }
    )
    admin_user.set_password('admin123')
    admin_user.save()

    desk_officer, _ = User.objects.get_or_create(
        username='desk_officer',
        defaults={
            'email': 'library.desk@daffodilvarsity.edu.bd',
            'role': 'staff',
            'is_verified_staff': True,
            'institution_name': 'Daffodil International University (DIU)',
            'student_id_or_badge': 'DIU-STAFF-4091',
            'phone': '01811-000002',
        }
    )
    desk_officer.set_password('staff123')
    desk_officer.save()

    student_seeker, _ = User.objects.get_or_create(
        username='diu_student',
        defaults={
            'email': 'rakib.cse@diu.edu.bd',
            'role': 'student',
            'institution_name': 'Daffodil International University',
            'student_id_or_badge': '211-15-4819',
            'phone': '01911-000003',
        }
    )
    student_seeker.set_password('student123')
    student_seeker.save()

    finder_user, _ = User.objects.get_or_create(
        username='tanvir_finder',
        defaults={
            'email': 'tanvir@diu.edu.bd',
            'role': 'student',
            'institution_name': 'Daffodil International University',
            'student_id_or_badge': '221-15-8942',
            'phone': '01611-000004',
        }
    )
    finder_user.set_password('finder123')
    finder_user.save()

    transport_user, _ = User.objects.get_or_create(
        username='railway_staff',
        defaults={
            'email': 'support@railway.gov.bd',
            'role': 'transport',
            'is_verified_staff': True,
            'institution_name': 'DIU Transport & Transit Authority',
            'phone': '01511-000005',
        }
    )
    transport_user.set_password('transport123')
    transport_user.save()

    print("[OK] Demo Users verified")

    # 2. Categories with student focus
    categories_data = [
        ('Laptops & Computers', 'laptops-computers', 'fas fa-laptop', 'laptop, macbook, notebook, dell, hp, lenovo, asus, charger, keyboard'),
        ('Smartphones & Tablets', 'smartphones-tablets', 'fas fa-mobile-alt', 'mobile, phone, smartphone, iphone, samsung, redmi, xiaomi, oppo, tablet, ipad'),
        ('Backpacks & Bags', 'backpacks-bags', 'fas fa-briefcase', 'backpack, bag, luggage, pouch, handbag, sidebag, duffle, rucksack'),
        ('Wallets & Purses', 'wallets-purses', 'fas fa-wallet', 'wallet, purse, moneybag, cash, cards, coinholder'),
        ('Student & National IDs', 'ids-documents', 'fas fa-id-card', 'id, card, student id, license, nid, passport, admit card, registration, badge'),
        ('Books & Study Materials', 'books-study', 'fas fa-book', 'book, textbook, notebook, syllabus, sheet, diary, pen, calculator, cse, engineering, slides'),
        ('Daily Student Gear & Flasks', 'student-gear', 'fas fa-flask', 'bottle, flask, thermos, umbrella, mug, lunchbox, rain, water, glasses, spectacles'),
        ('Keys & Keyrings', 'keys-keyrings', 'fas fa-key', 'key, keychain, keyset, bike key, room key, bike, lock'),
        ('Electronics & Audio', 'electronics-audio', 'fas fa-headphones', 'headphone, headphones, airpods, earbuds, headset, smart watch, power bank, speaker, camera'),
        ('Watches & Accessories', 'watches-accessories', 'fas fa-clock', 'watch, casio, rolex, bracelet, ring, glasses, sunglasses'),
    ]

    cat_map = {}
    for name, slug, icon, kw in categories_data:
        cat, _ = Category.objects.get_or_create(
            name=name,
            defaults={'slug': slug, 'icon': icon, 'ai_keywords': kw}
        )
        cat_map[slug] = cat
    print("[OK] Categories verified")

    # 3. Institutional Desks inside DIU Ashulia Campus
    diu_library_desk, _ = LostFoundDesk.objects.get_or_create(
        name='DIU Central Library Help Desk',
        organization='Daffodil International University',
        defaults={
            'desk_type': 'university',
            'location_details': 'Library Building, 2nd Floor, Ashulia Smart City',
            'contact_phone': '+880-1847-140001',
            'contact_email': 'library.desk@daffodilvarsity.edu.bd',
            'manager': desk_officer,
            'is_active': True,
        }
    )

    diu_admin_desk, _ = LostFoundDesk.objects.get_or_create(
        name='DIU Main Admin Security Desk',
        organization='Daffodil International University',
        defaults={
            'desk_type': 'university',
            'location_details': 'Ground Floor, Knowledge Tower Building, Ashulia',
            'contact_phone': '+880-1847-140002',
            'contact_email': 'security@daffodilvarsity.edu.bd',
            'manager': desk_officer,
            'is_active': True,
        }
    )

    metro_desk, _ = LostFoundDesk.objects.get_or_create(
        name='DIU Ashulia Shuttle & Transport Depot',
        organization='DIU Transport Section',
        defaults={
            'desk_type': 'transport',
            'location_details': 'Campus Gate 1 Shuttle Stand, Ashulia',
            'contact_phone': '+880-1847-140003',
            'contact_email': 'transport@daffodilvarsity.edu.bd',
            'manager': transport_user,
            'is_active': True,
        }
    )
    print("[OK] DIU Campus Desks verified")

    # 4. Realistic DIU Student Items with REAL PHOTOGRAPHS

    # Item 1: Student Smart ID Card (LOST)
    lost_id_card, _ = ItemReport.objects.update_or_create(
        title='DIU Student Smart ID Card (CSE Dept)',
        report_type='lost',
        user=student_seeker,
        defaults={
            'category': cat_map['ids-documents'],
            'primary_color': 'Green',
            'brand': 'Daffodil International University',
            'description': 'Lost my green DIU Student ID card with green lanyard while attending mid-term exam at DIU Library 3rd floor reading area.',
            'image': 'item_photos/student_id.jpg',
            'incident_date': date(2026, 11, 6),
            'incident_time': time(10, 45),
            'location_name': 'DIU Central Library 3rd Floor Exam Study Zone',
            'safe_area_display': 'DIU Central Library (Ashulia)',
            'latitude': 23.878400,
            'longitude': 90.322100,
            'secret_proof_details': 'Student ID Number: 211-15-4819. Department of Computer Science & Engineering. Has small red holographic seal on back.',
            'status': 'potential_match',
        }
    )

    # Item 2: Student Smart ID Card (FOUND)
    found_id_card, _ = ItemReport.objects.update_or_create(
        title='Found DIU Student Smart ID Card with Lanyard',
        report_type='found',
        user=finder_user,
        defaults={
            'category': cat_map['ids-documents'],
            'primary_color': 'Green',
            'brand': 'Daffodil International University',
            'description': 'Found a DIU student ID card dropped near Library 3rd floor study desk. Deposited at Library Help Desk.',
            'image': 'item_photos/student_id.jpg',
            'incident_date': date(2026, 11, 6),
            'incident_time': time(11, 30),
            'location_name': 'DIU Central Library 3rd Floor',
            'safe_area_display': 'DIU Central Library',
            'latitude': 23.878410,
            'longitude': 90.322110,
            'status': 'potential_match',
        }
    )

    # Custody Record for Found ID Card
    if not hasattr(found_id_card, 'custody_record'):
        token_id = uuid.uuid4().hex[:12].upper()
        custody_id = CustodyRecord.objects.create(
            item=found_id_card,
            desk=diu_library_desk,
            tracking_token=token_id,
            current_status='in_storage',
            storage_bin_or_shelf='ID Tray B-02',
            received_by=desk_officer
        )
        custody_id.generate_qr()
        custody_id.save()
        CustodyLog.objects.create(
            custody_record=custody_id,
            action="Student ID Card deposited at Library Desk",
            actor=desk_officer,
            notes="Cataloged in ID Tray B-02. Ready for verification."
        )

    # Item 3: Important Textbooks & Notebooks (LOST)
    lost_books, _ = ItemReport.objects.update_or_create(
        title='Algorithms Textbook & CSE Lecture Spiral Notebook',
        report_type='lost',
        user=student_seeker,
        defaults={
            'category': cat_map['books-study'],
            'primary_color': 'Blue',
            'brand': 'Pearson / DIU Spiral Note',
            'description': 'Left my Introduction to Algorithms textbook and my semester lecture notebook on the table of DIU Academic Building 3 (Room 402).',
            'image': 'item_photos/important_books.jpg',
            'incident_date': date(2026, 11, 6),
            'incident_time': time(14, 0),
            'location_name': 'DIU Academic Complex AB-3 Room 402',
            'safe_area_display': 'DIU Academic Building 3',
            'latitude': 23.878315,
            'longitude': 90.322056,
            'secret_proof_details': 'First page of notebook has handwritten name Rakib Ahmed and Section F note.',
            'status': 'open',
        }
    )

    # Item 4: Stainless Steel Water Flask (FOUND)
    found_flask, _ = ItemReport.objects.update_or_create(
        title='Milton 750ml Matte Cyan Insulated Water Flask',
        report_type='found',
        user=finder_user,
        defaults={
            'category': cat_map['student-gear'],
            'primary_color': 'Cyan',
            'brand': 'Milton',
            'description': 'Found a premium insulated matte cyan metal water bottle left on a cafeteria lakeside bench.',
            'image': 'item_photos/water_flask.jpg',
            'incident_date': date(2026, 11, 6),
            'incident_time': time(13, 15),
            'location_name': 'DIU Central Cafeteria Lakeside Bench',
            'safe_area_display': 'DIU Cafeteria Lakeside',
            'latitude': 23.875130,
            'longitude': 90.321442,
            'status': 'open',
        }
    )

    # Item 5: Compact Foldable Umbrella (LOST)
    lost_umbrella, _ = ItemReport.objects.update_or_create(
        title='Black Automatic Windproof Foldable Umbrella',
        report_type='lost',
        user=student_seeker,
        defaults={
            'category': cat_map['student-gear'],
            'primary_color': 'Black',
            'brand': 'Citizen',
            'description': 'Left my foldable black rain umbrella on the seat while boarding DIU shuttle bus at Campus Gate 1 depot.',
            'image': 'item_photos/umbrella.jpg',
            'incident_date': date(2026, 11, 5),
            'incident_time': time(17, 30),
            'location_name': 'DIU Shuttle Bus Stand Gate 1',
            'safe_area_display': 'DIU Shuttle Stand',
            'latitude': 23.875467,
            'longitude': 90.321835,
            'is_transit_item': True,
            'transit_vehicle_name': 'DIU Shuttle Bus #07',
            'transit_route': 'DIU Ashulia to Mirpur 10',
            'transit_boarding_point': 'DIU Campus Gate 1',
            'transit_drop_point': 'Mirpur 10',
            'secret_proof_details': 'Small yellow tag on wrist strap with initials RA.',
            'status': 'open',
        }
    )

    # Item 6: Casio Scientific Calculator (LOST)
    lost_calculator, _ = ItemReport.objects.update_or_create(
        title='Casio fx-991EX ClassWiz Scientific Calculator',
        report_type='lost',
        user=student_seeker,
        defaults={
            'category': cat_map['books-study'],
            'primary_color': 'Black',
            'brand': 'Casio',
            'description': 'Left my Casio fx-991EX scientific calculator on desk in Engineering Lab 304 after math class.',
            'image': 'item_photos/scientific_calculator.jpg',
            'incident_date': date(2026, 11, 6),
            'incident_time': time(12, 10),
            'location_name': 'DIU Academic Complex AB-1 Lab 304',
            'safe_area_display': 'DIU Academic Complex AB-1',
            'latitude': 23.878315,
            'longitude': 90.322056,
            'secret_proof_details': 'Small physics formula sticker pasted inside the plastic slide cover.',
            'status': 'open',
        }
    )

    # Item 7: Sony Wireless Headphones (LOST & FOUND - AI MATCH)
    lost_headphones, _ = ItemReport.objects.update_or_create(
        title='Sony WH-1000XM4 Wireless Headphones',
        report_type='lost',
        user=student_seeker,
        defaults={
            'category': cat_map['electronics-audio'],
            'primary_color': 'Black',
            'brand': 'Sony',
            'description': 'Over-ear black Sony noise-canceling headphones left in zippered hard case at DIU Library 2nd floor reading area.',
            'image': 'item_photos/headphones_black.jpg',
            'incident_date': date(2026, 11, 6),
            'incident_time': time(11, 15),
            'location_name': 'DIU Central Library 2nd Floor Reading Room',
            'safe_area_display': 'DIU Library 2nd Floor',
            'latitude': 23.878400,
            'longitude': 90.322100,
            'secret_proof_details': 'Small scratch near left hinge. Custom red acoustic foam insert inside right ear cup.',
            'status': 'potential_match',
        }
    )

    found_headphones, _ = ItemReport.objects.update_or_create(
        title='Found Black Sony Wireless Headphones',
        report_type='found',
        user=finder_user,
        defaults={
            'category': cat_map['electronics-audio'],
            'primary_color': 'Black',
            'brand': 'Sony',
            'description': 'Found black Sony over-ear headphones on study table in library. Deposited at Library Desk.',
            'image': 'item_photos/headphones_black.jpg',
            'incident_date': date(2026, 11, 6),
            'incident_time': time(12, 30),
            'location_name': 'DIU Central Library Reading Desks',
            'safe_area_display': 'DIU Central Library',
            'latitude': 23.878405,
            'longitude': 90.322105,
            'status': 'potential_match',
        }
    )

    # Item 8: HP Pavilion Laptop (LOST & FOUND - AI MATCH)
    lost_laptop, _ = ItemReport.objects.update_or_create(
        title='Black HP Pavilion 15-inch Laptop',
        report_type='lost',
        user=student_seeker,
        defaults={
            'category': cat_map['laptops-computers'],
            'primary_color': 'Black',
            'brand': 'HP',
            'description': 'Left my HP Pavilion laptop on the 3rd floor quiet study area table in DIU Library. Has anime stickers on lid.',
            'image': 'item_photos/laptop_hp.jpg',
            'incident_date': date(2026, 11, 5),
            'incident_time': time(14, 30),
            'location_name': 'DIU Central Library 3rd Floor Quiet Zone',
            'safe_area_display': 'DIU Library 3rd Floor',
            'latitude': 23.878400,
            'longitude': 90.322100,
            'secret_proof_details': 'Sticker of Goku on top lid. Serial number ends in -4829. Desktop wallpaper is Naruto.',
            'status': 'potential_match',
        }
    )

    found_laptop, _ = ItemReport.objects.update_or_create(
        title='Found Black HP Laptop 15-inch',
        report_type='found',
        user=finder_user,
        defaults={
            'category': cat_map['laptops-computers'],
            'primary_color': 'Black',
            'brand': 'HP',
            'description': 'Found a black HP laptop left unattended on study desk at DIU library yesterday afternoon. Deposited at Library Desk.',
            'image': 'item_photos/laptop_hp.jpg',
            'incident_date': date(2026, 11, 5),
            'incident_time': time(16, 0),
            'location_name': 'DIU Central Library Study Room',
            'safe_area_display': 'DIU Central Library',
            'latitude': 23.878395,
            'longitude': 90.322095,
            'status': 'potential_match',
        }
    )

    if not hasattr(found_laptop, 'custody_record'):
        token = uuid.uuid4().hex[:12].upper()
        custody = CustodyRecord.objects.create(
            item=found_laptop,
            desk=diu_library_desk,
            tracking_token=token,
            current_status='in_storage',
            storage_bin_or_shelf='Locker A-04',
            received_by=desk_officer
        )
        custody.generate_qr()
        custody.save()
        CustodyLog.objects.create(
            custody_record=custody,
            action="Laptop deposited at DIU Library Desk",
            actor=desk_officer,
            notes="Stored in Locker A-04."
        )

    # Item 9: College Backpack (FOUND)
    found_backpack, _ = ItemReport.objects.update_or_create(
        title='Grey Arctic Hunter Laptop Backpack',
        report_type='found',
        user=finder_user,
        defaults={
            'category': cat_map['backpacks-bags'],
            'primary_color': 'Grey',
            'brand': 'Arctic Hunter',
            'description': 'Grey water-resistant backpack found on bench outside DIU Academic Building 4.',
            'image': 'item_photos/backpack_college.jpg',
            'incident_date': date(2026, 11, 6),
            'location_name': 'DIU Academic Complex AB-4 Bench',
            'safe_area_display': 'DIU Academic Complex AB-4',
            'latitude': 23.878315,
            'longitude': 90.322056,
            'status': 'open',
        }
    )

    # Item 10: Spectacles / Eyeglasses in Hard Case (FOUND)
    found_specs, _ = ItemReport.objects.update_or_create(
        title='Black Rimmed Reading Eyeglasses in Case',
        report_type='found',
        user=finder_user,
        defaults={
            'category': cat_map['student-gear'],
            'primary_color': 'Black',
            'brand': 'Ray-Ban',
            'description': 'Prescription reading glasses in black matte case found on study table in Library ground floor.',
            'image': 'item_photos/spectacles_case.jpg',
            'incident_date': date(2026, 11, 6),
            'location_name': 'DIU Central Library Ground Floor',
            'safe_area_display': 'DIU Central Library',
            'latitude': 23.878400,
            'longitude': 90.322100,
            'status': 'open',
        }
    )

    # Item 11: Yamaha Bike Keys (LOST)
    lost_keys, _ = ItemReport.objects.update_or_create(
        title='Yamaha Bike Keys on Green DIU Lanyard',
        report_type='lost',
        user=student_seeker,
        defaults={
            'category': cat_map['keys-keyrings'],
            'primary_color': 'Silver',
            'brand': 'Yamaha',
            'description': 'Lost my bike key on green DIU CSE department neck lanyard near motorcycle parking zone near Gate 1.',
            'image': 'item_photos/keys_keychain.jpg',
            'incident_date': date(2026, 11, 6),
            'location_name': 'DIU Motorcycle & Bike Parking Bay Gate 1',
            'safe_area_display': 'DIU Parking Bay',
            'latitude': 23.875700,
            'longitude': 90.320500,
            'secret_proof_details': 'Key tag has blue rubber ring and small miniature helmet pendant.',
            'status': 'open',
        }
    )

    # Item 12: Leather Wallet (LOST & FOUND - JourneyTrace)
    lost_wallet, _ = ItemReport.objects.update_or_create(
        title='Brown Leather Wallet with Cards',
        report_type='lost',
        user=student_seeker,
        defaults={
            'category': cat_map['wallets-purses'],
            'primary_color': 'Brown',
            'brand': 'WildHorn',
            'description': 'Lost my brown leather wallet while traveling from Mirpur 10 to DIU Campus on Bikolpo Bus. Contains Student ID.',
            'image': 'item_photos/wallet_brown.jpg',
            'incident_date': date(2026, 11, 4),
            'location_name': 'Bikolpo Bus Route Mirpur to Ashulia',
            'safe_area_display': 'Bikolpo Bus Transit',
            'latitude': 23.83500,
            'longitude': 90.34500,
            'is_transit_item': True,
            'transit_vehicle_name': 'Bikolpo Bus Line (Dhaka Metro-BA-11-4589)',
            'transit_route': 'Mirpur 10 to DIU Ashulia Campus',
            'transit_boarding_point': 'Mirpur 10 Roundabout',
            'transit_drop_point': 'DIU Smart City Gate 1',
            'transit_seat_number': 'Seat #14 (Window side, middle row)',
            'secret_proof_details': 'Contains DIU student ID for Rakib Ahmed, 1500 Taka in cash, and a blue BRAC Bank debit card.',
            'status': 'potential_match',
        }
    )

    found_wallet, _ = ItemReport.objects.update_or_create(
        title='Brown Men Wallet found on Bus seat',
        report_type='found',
        user=finder_user,
        defaults={
            'category': cat_map['wallets-purses'],
            'primary_color': 'Brown',
            'brand': 'WildHorn',
            'description': 'Conductor gave me a brown wallet picked up from Bikolpo Bus seat near DIU stop.',
            'image': 'item_photos/wallet_brown.jpg',
            'incident_date': date(2026, 11, 4),
            'location_name': 'Bikolpo Bus Ashulia Terminal',
            'safe_area_display': 'Ashulia Transit Terminal',
            'latitude': 23.83600,
            'longitude': 90.34600,
            'is_transit_item': True,
            'transit_vehicle_name': 'Bikolpo Bus Line (Dhaka Metro-BA-11-4589)',
            'transit_route': 'Mirpur 10 to DIU Ashulia Campus',
            'transit_boarding_point': 'Mirpur 10',
            'transit_drop_point': 'DIU Smart City Gate 1',
            'transit_seat_number': 'Middle row window seat',
            'status': 'potential_match',
        }
    )

    # Item 13: Recovered AirPods Case
    recovered_airpods, _ = ItemReport.objects.update_or_create(
        title='Apple AirPods Pro 2nd Gen Case',
        report_type='found',
        user=finder_user,
        defaults={
            'category': cat_map['electronics-audio'],
            'primary_color': 'White',
            'brand': 'Apple',
            'description': 'White AirPods case with blue silicone cover found in DIU cafeteria.',
            'image': 'item_photos/airpods_case.jpg',
            'incident_date': date(2026, 11, 2),
            'location_name': 'DIU Cafeteria Main Hall',
            'safe_area_display': 'DIU Cafeteria',
            'status': 'recovered',
        }
    )

    # Run AI Matching on seeded items
    print("[*] Running AI Multidimensional Matching Engine...")
    run_ai_matching_for_item(lost_id_card)
    run_ai_matching_for_item(lost_headphones)
    run_ai_matching_for_item(lost_laptop)
    run_ai_matching_for_item(lost_wallet)

    print("[SUCCESS] All DIU student items and AI matching populated!")


if __name__ == '__main__':
    seed_database()
