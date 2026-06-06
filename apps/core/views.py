"""
SIBRAH Core App — Views
apps/core/views.py
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings


SERVICES_FULL = [
    {'icon': '💻', 'title': 'Computer Sales', 'desc': 'We supply brand new and certified refurbished hardware from leading global brands with genuine warranty.', 'tags': ['Laptops (HP, Dell, Lenovo)', 'Desktop Computers', 'Keyboards & Mice', 'Printers', 'Monitors', 'Accessories']},
    {'icon': '🔧', 'title': 'Repairs & Maintenance', 'desc': 'Certified technicians diagnose and fix all hardware and software issues quickly. We service all brands and models.', 'tags': ['Laptop Repair', 'Motherboard Repair', 'Screen Replacement', 'Printer Repair', 'Data Recovery', 'Virus Removal', 'OS Installation']},
    {'icon': '💻', 'title': 'Software Development', 'desc': 'We build robust, scalable software solutions tailored to your specific business needs — from websites to enterprise applications.', 'tags': ['Website Development', 'Mobile Apps', 'School Portals', 'E-Commerce Platforms', 'Business Management Systems', 'API Development']},
    {'icon': '🎓', 'title': 'ICT Training', 'desc': 'Structured training programs equip learners with practical, market-relevant skills. All courses come with verifiable certificates.', 'tags': ['Computer Basics', 'Microsoft Office', 'Graphics Design', 'Web Design', 'Python', 'Django', 'React', 'Data Analysis', 'AI']},
    {'icon': '🖨️', 'title': 'Business Center', 'desc': 'A fully equipped business center providing a complete range of document and office services.', 'tags': ['Printing (Color & B&W)', 'Scanning', 'Photocopying', 'Lamination', 'Typing Services', 'Binding & Packaging', 'ID Card Printing']},
    {'icon': '📈', 'title': 'ICT Consultancy', 'desc': 'Strategic technology consulting to help organizations leverage digital tools and achieve their technology goals.', 'tags': ['Technology Roadmap', 'Cybersecurity Advisory', 'Cloud Migration', 'Network Setup', 'Digital Transformation']},
]

SERVICES_LIST = [
    {'icon': '💻', 'title': 'Computer Sales',        'desc': 'Brand new and refurbished laptops, desktops, and accessories at competitive prices.'},
    {'icon': '🔧', 'title': 'Repairs & Maintenance', 'desc': 'Expert repair for laptops, desktops, printers, and all peripherals. All brands.'},
    {'icon': '💻', 'title': 'Software Development',  'desc': 'Custom web apps, mobile apps, school portals, and business management systems.'},
    {'icon': '🎓', 'title': 'ICT Training',           'desc': 'From basic computing to advanced programming — all courses are certified.'},
    {'icon': '🖨️', 'title': 'Business Center',       'desc': 'Printing, scanning, lamination, typing, and all business support services.'},
    {'icon': '📈', 'title': 'ICT Consultancy',        'desc': 'Strategic technology consulting to help businesses go digital and grow faster.'},
]

WHY_LIST = [
    {'icon': '👨‍💻', 'title': 'Experienced Professionals', 'desc': 'Certified engineers with years of experience.'},
    {'icon': '💰',  'title': 'Affordable Services',        'desc': 'Competitive pricing without compromising quality.'},
    {'icon': '✅',  'title': 'Quality Products',           'desc': 'Only genuine, tested, certified products.'},
    {'icon': '😊',  'title': 'Customer Satisfaction',      'desc': 'Your satisfaction is our top priority.'},
    {'icon': '⚡',  'title': 'Fast Delivery',              'desc': 'Prompt service and quick turnaround times.'},
    {'icon': '🛡️', 'title': 'Reliable Support',           'desc': 'After-sales support always available.'},
]

VALUES = [
    {'icon': '🏆', 'name': 'Excellence'},
    {'icon': '🤝', 'name': 'Integrity'},
    {'icon': '💡', 'name': 'Innovation'},
    {'icon': '👔', 'name': 'Professionalism'},
    {'icon': '❤️', 'name': 'Customer Focus'},
]

PROJECTS = [
    {'icon': '🏫', 'title': 'School Management System',
     'desc': 'Comprehensive portal for student enrollment, results, attendance, and fees for a federal secondary school.',
     'tech': ['Django', 'Python', 'PostgreSQL', 'Bootstrap']},
    {'icon': '📱', 'title': 'Citizen Reporting App',
     'desc': 'Mobile and web app enabling citizens to report infrastructure and security issues to authorities with GPS mapping.',
     'tech': ['React Native', 'Django REST', 'Maps API']},
    {'icon': '🎓', 'title': 'Polytechnic Website',
     'desc': 'Responsive institutional website with course listings, admissions portal, staff directory, and news management.',
     'tech': ['React', 'Node.js', 'MongoDB', 'Tailwind']},
    {'icon': '🏢', 'title': 'Business Websites',
     'desc': 'Portfolio of professional websites for retail, logistics, NGOs, and real estate firms across Nigeria.',
     'tech': ['HTML/CSS', 'JavaScript', 'WordPress', 'SEO']},
]

GALLERY_ITEMS = [
    {'icon': '🎓', 'label': 'Training Session'},
    {'icon': '🖥️', 'label': 'Computer Setup'},
    {'icon': '🔧', 'label': 'Repair Workshop'},
    {'icon': '💼', 'label': 'Office Space'},
    {'icon': '👨‍💻', 'label': 'Coding Bootcamp'},
    {'icon': '🏆', 'label': 'Graduation Ceremony'},
    {'icon': '📡', 'label': 'Network Installation'},
    {'icon': '🖨️', 'label': 'Business Center'},
    {'icon': '🤝', 'label': 'Client Meeting'},
    {'icon': '💻', 'label': 'Product Display'},
    {'icon': '📊', 'label': 'Data Analysis Class'},
    {'icon': '🎯', 'label': 'Workshop Session'},
]

FAQS = [
    {'q': 'Do you offer online training courses?',
     'a': 'Yes! We offer fully online training via Zoom or Google Meet with recorded lessons and an online student portal. All online students receive the same certification as in-person students.'},
    {'q': 'Do you issue certificates after training?',
     'a': 'Yes — all graduates receive verifiable certificates with a unique code that can be verified on our website. Certificates carry our official seal, student name, course details, and completion date.'},
    {'q': 'Do you repair all laptop brands?',
     'a': 'Yes. Our certified technicians repair HP, Dell, Lenovo, Acer, Asus, Apple MacBook, Samsung, Toshiba, and all other major brands — hardware, screens, keyboards, motherboards, and software.'},
    {'q': 'How long does a laptop repair take?',
     'a': 'Most common repairs are completed within 24–48 hours. Complex motherboard repairs may take 3–5 working days. We provide a free diagnosis within 2 hours of receiving your device.'},
    {'q': 'How do I pay for products or courses?',
     'a': 'We accept bank transfer to ACCESS BANK — Account Name: IBRAHIM BABA SULEIMAN, Account Number: 1227425306. After payment, send your receipt to +234 808 110 1992 on WhatsApp for instant confirmation.'},
    {'q': 'Can I buy a laptop on an installment plan?',
     'a': 'Yes, we offer flexible payment plans for qualifying customers. Contact us to discuss your needs and we will work out a suitable arrangement. A minimum deposit is required upfront.'},
    {'q': 'Do you develop mobile apps for businesses?',
     'a': 'Absolutely. We develop mobile applications for both Android and iOS platforms using React Native. Our apps include business management tools, e-commerce platforms, delivery apps, and custom enterprise solutions.'},
    {'q': 'How can I verify a training certificate?',
     'a': 'Visit the Certificate Verification page on our website, enter the unique code printed on the certificate, and the system will instantly confirm the student name, course, grade, and date of issue.'},
]

CONTACT_ITEMS = [
    {'icon': '📍', 'label': 'Address',          'value': 'SIBRAH Technology Hub, Abuja, Nigeria'},
    {'icon': '📞', 'label': 'Phone / WhatsApp',  'value': '+234 808 110 1992'},
    {'icon': '✉️', 'label': 'Email',             'value': 'info@sibrahtech.com.ng'},
    {'icon': '🕒', 'label': 'Business Hours',    'value': 'Mon–Sat: 8:00AM – 6:00PM'},
    {'icon': '🏦', 'label': 'Bank Transfer',     'value': 'ACCESS BANK | IBRAHIM BABA SULEIMAN | 1227425306'},
]


def home(request):
    from apps.training.models import Course
    from apps.shop.models import Product
    from apps.blog.models import Post

    courses  = Course.objects.filter(is_active=True, is_featured=True)[:6]
    products = Product.objects.filter(is_active=True, is_featured=True)[:4]
    posts    = Post.objects.filter(is_published=True)[:3]

    return render(request, 'core/home.html', {
        'courses':       courses,
        'products':      products,
        'posts':         posts,
        'services_list': SERVICES_LIST,
        'why_list':      WHY_LIST,
        'company':       settings.SIBRAH_COMPANY,
    })


def about(request):
    return render(request, 'core/about.html', {
        'values':  VALUES,
        'company': settings.SIBRAH_COMPANY,
    })


def services(request):
    return render(request, 'core/services.html', {
        'services_full': SERVICES_FULL,
        'company':       settings.SIBRAH_COMPANY,
    })


def portfolio(request):
    return render(request, 'core/portfolio.html', {
        'projects': PROJECTS,
        'company':  settings.SIBRAH_COMPANY,
    })


def gallery(request):
    return render(request, 'core/gallery.html', {
        'gallery_items': GALLERY_ITEMS,
        'company':       settings.SIBRAH_COMPANY,
    })


def faq(request):
    return render(request, 'core/faq.html', {
        'faqs':    FAQS,
        'company': settings.SIBRAH_COMPANY,
    })


def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        phone   = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            from django.core.mail import send_mail
            try:
                send_mail(
                    subject    = f"[SIBRAH Contact] {subject} — from {name}",
                    message    = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\n{message}",
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    recipient_list = [settings.SIBRAH_COMPANY['email']],
                    fail_silently  = True,
                )
            except Exception:
                pass
            messages.success(request,
                f"Thank you {name}! Your message has been received. We will reply within 24 hours.")
            return redirect('core:contact')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'core/contact.html', {
        'contact_items': CONTACT_ITEMS,
        'company':       settings.SIBRAH_COMPANY,
    })
