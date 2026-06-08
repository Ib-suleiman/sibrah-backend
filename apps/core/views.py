"""
SIBRAH Core App — Views
apps/core/views.py
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone


SERVICES_FULL = [
    {'icon': '💻', 'title': 'Computer Sales', 'desc': 'We supply brand new and certified refurbished hardware from leading global brands with genuine warranty.', 'tags': ['Laptops (HP, Dell, Lenovo)', 'Desktop Computers', 'Keyboards & Mice', 'Printers', 'Monitors', 'Accessories']},
    {'icon': '🔧', 'title': 'Repairs & Maintenance', 'desc': 'Certified technicians diagnose and fix all hardware and software issues quickly. We service all brands and models.', 'tags': ['Laptop Repair', 'Motherboard Repair', 'Screen Replacement', 'Printer Repair', 'Data Recovery', 'Virus Removal', 'OS Installation']},
    {'icon': '💻', 'title': 'Software Development', 'desc': 'We build robust, scalable software solutions tailored to your specific business needs.', 'tags': ['Website Development', 'Mobile Apps', 'School Portals', 'E-Commerce Platforms', 'Business Management Systems', 'API Development']},
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
     'desc': 'Comprehensive portal for student enrollment, results, attendance, and fees.',
     'tech': ['Django', 'Python', 'PostgreSQL', 'Bootstrap']},
    {'icon': '📱', 'title': 'Citizen Reporting App',
     'desc': 'Mobile and web app enabling citizens to report infrastructure issues with GPS mapping.',
     'tech': ['React Native', 'Django REST', 'Maps API']},
    {'icon': '🎓', 'title': 'Polytechnic Website',
     'desc': 'Responsive institutional website with admissions portal and news management.',
     'tech': ['React', 'Node.js', 'MongoDB', 'Tailwind']},
    {'icon': '🏢', 'title': 'Business Websites',
     'desc': 'Portfolio of professional websites for retail, logistics, NGOs, and real estate firms.',
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
     'a': 'Yes! We offer fully online training via Zoom or Google Meet with recorded lessons. All online students receive the same certification as in-person students.'},
    {'q': 'Do you issue certificates after training?',
     'a': 'Yes — all graduates receive verifiable certificates with a unique code that can be verified on our website.'},
    {'q': 'Do you repair all laptop brands?',
     'a': 'Yes. Our certified technicians repair HP, Dell, Lenovo, Acer, Asus, Apple MacBook, Samsung, Toshiba, and all other major brands.'},
    {'q': 'How long does a laptop repair take?',
     'a': 'Most common repairs are completed within 24–48 hours. Complex motherboard repairs may take 3–5 working days.'},
    {'q': 'How do I pay for products or courses?',
     'a': 'We accept bank transfer to ACCESS BANK — Account Name: IBRAHIM BABA SULEIMAN, Account Number: 1227425306. After payment, send your receipt to +234 808 110 1992 on WhatsApp.'},
    {'q': 'Can I buy a laptop on an installment plan?',
     'a': 'Yes, we offer flexible payment plans for qualifying customers. Contact us to discuss your needs.'},
    {'q': 'Do you develop mobile apps for businesses?',
     'a': 'Absolutely. We develop mobile applications for both Android and iOS platforms using React Native.'},
    {'q': 'How can I verify a training certificate?',
     'a': 'Visit the Certificate Verification page on our website and enter the unique code printed on the certificate.'},
]

CONTACT_ITEMS = [
    {'icon': '📍', 'label': 'Address',         'value': 'SIBRAH Technology Hub, Abuja, Nigeria'},
    {'icon': '📞', 'label': 'Phone / WhatsApp', 'value': '+234 808 110 1992'},
    {'icon': '✉️', 'label': 'Email',            'value': 'info@sibrahtech.com.ng'},
    {'icon': '🕒', 'label': 'Business Hours',   'value': 'Mon–Sat: 8:00AM – 6:00PM'},
    {'icon': '🏦', 'label': 'Bank Transfer',    'value': 'ACCESS BANK | IBRAHIM BABA SULEIMAN | 1227425306'},
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


# ── SEO FILES ─────────────────────────────────────────────────────────

def sitemap(request):
    """Generate XML sitemap for Google."""
    from apps.blog.models import Post
    from apps.training.models import Course

    posts   = Post.objects.filter(is_published=True)
    courses = Course.objects.filter(is_active=True)
    now     = timezone.now().strftime('%Y-%m-%d')

    static_urls = [
        {'url': '/',            'priority': '1.0', 'freq': 'weekly'},
        {'url': '/about/',      'priority': '0.8', 'freq': 'monthly'},
        {'url': '/services/',   'priority': '0.9', 'freq': 'monthly'},
        {'url': '/training/',   'priority': '0.9', 'freq': 'weekly'},
        {'url': '/shop/',       'priority': '0.8', 'freq': 'weekly'},
        {'url': '/blog/',       'priority': '0.8', 'freq': 'daily'},
        {'url': '/contact/',    'priority': '0.7', 'freq': 'monthly'},
        {'url': '/portfolio/',  'priority': '0.7', 'freq': 'monthly'},
        {'url': '/certificates/verify/', 'priority': '0.6', 'freq': 'monthly'},
    ]

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    base = 'https://sibrahtech.com.ng'

    for item in static_urls:
        xml += f'  <url>\n'
        xml += f'    <loc>{base}{item["url"]}</loc>\n'
        xml += f'    <lastmod>{now}</lastmod>\n'
        xml += f'    <changefreq>{item["freq"]}</changefreq>\n'
        xml += f'    <priority>{item["priority"]}</priority>\n'
        xml += f'  </url>\n'

    for post in posts:
        date = post.published_at.strftime('%Y-%m-%d') if post.published_at else now
        xml += f'  <url>\n'
        xml += f'    <loc>{base}/blog/{post.slug}/</loc>\n'
        xml += f'    <lastmod>{date}</lastmod>\n'
        xml += f'    <changefreq>monthly</changefreq>\n'
        xml += f'    <priority>0.7</priority>\n'
        xml += f'  </url>\n'

    for course in courses:
        xml += f'  <url>\n'
        xml += f'    <loc>{base}/training/{course.slug}/</loc>\n'
        xml += f'    <lastmod>{now}</lastmod>\n'
        xml += f'    <changefreq>monthly</changefreq>\n'
        xml += f'    <priority>0.8</priority>\n'
        xml += f'  </url>\n'

    xml += '</urlset>'

    return HttpResponse(xml, content_type='application/xml')


def robots_txt(request):
    """Generate robots.txt for search engines."""
    content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /portal/admin-panel/
Disallow: /portal/dashboard/
Disallow: /api/

Sitemap: https://sibrahtech.com.ng/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')
