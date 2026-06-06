"""
Management command to seed SIBRAH database with initial data.
Run with:  python manage.py seed_sibrah
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the SIBRAH database with initial courses, products, and admin user.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n🚀 Seeding SIBRAH database...\n'))
        self._create_superuser()
        self._create_courses()
        self._create_products()
        self._create_blog_posts()
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!\n'))
        self.stdout.write('   Admin login → http://127.0.0.1:8000/admin/')
        self.stdout.write('   Username: admin | Password: sibrah@2025\n')

    # ── SUPERUSER ──────────────────────────────────────────
    def _create_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username   = 'admin',
                email      = 'info@sibrahtech.com.ng',
                password   = 'sibrah@2025',
                first_name = 'SIBRAH',
                last_name  = 'Admin',
                role       = 'admin',
            )
            self.stdout.write('  ✔ Superuser created (admin / sibrah@2025)')
        else:
            self.stdout.write('  — Superuser already exists')

    # ── COURSES ────────────────────────────────────────────
    def _create_courses(self):
        from apps.training.models import Course, CourseCategory

        cat_general, _ = CourseCategory.objects.get_or_create(
            name='General Computing', defaults={'slug': 'general'}
        )
        cat_dev, _ = CourseCategory.objects.get_or_create(
            name='Software Development', defaults={'slug': 'software-dev'}
        )
        cat_design, _ = CourseCategory.objects.get_or_create(
            name='Design', defaults={'slug': 'design'}
        )
        cat_data, _ = CourseCategory.objects.get_or_create(
            name='Data & AI', defaults={'slug': 'data-ai'}
        )

        courses = [
            # Beginner
            dict(title='Computer Basics',        slug='computer-basics',        level='beginner',
                 category=cat_general,  fee=15000,  duration='4 Weeks',  icon='🖥️',
                 tools='Windows, MS Office', schedule='Weekdays / Weekend',
                 description='Learn the fundamentals of computers and basic computing skills.'),
            dict(title='Microsoft Office Suite', slug='microsoft-office',        level='beginner',
                 category=cat_general,  fee=20000,  duration='6 Weeks',  icon='📊',
                 tools='Word, Excel, PowerPoint, Outlook', schedule='Flexible',
                 description='Master Microsoft Office tools used in every modern workplace.'),
            # Intermediate
            dict(title='Graphics Design',        slug='graphics-design',         level='intermediate',
                 category=cat_design,   fee=35000,  duration='8 Weeks',  icon='🎨',
                 tools='Photoshop, CorelDraw', schedule='Weekdays / Weekend',
                 description='Learn professional graphic design from scratch using industry tools.'),
            dict(title='Web Design',             slug='web-design',              level='intermediate',
                 category=cat_dev,      fee=40000,  duration='8 Weeks',  icon='🌐',
                 tools='HTML, CSS, JavaScript', schedule='Weekdays / Weekend',
                 description='Build beautiful, responsive websites with modern HTML, CSS, and JS.'),
            # Advanced
            dict(title='Python Programming',     slug='python-programming',      level='advanced',
                 category=cat_dev,      fee=55000,  duration='10 Weeks', icon='🐍',
                 tools='Python 3, OOP, Libraries', schedule='Weekdays / Weekend',
                 description='Master Python programming from basics to Object-Oriented Programming.'),
            dict(title='Django Web Framework',   slug='django-framework',        level='advanced',
                 category=cat_dev,      fee=60000,  duration='10 Weeks', icon='⚙️',
                 tools='Python, Django, PostgreSQL, REST', schedule='Weekdays',
                 description='Build full-stack web applications with Django, the leading Python framework.'),
            dict(title='React Development',      slug='react-development',       level='advanced',
                 category=cat_dev,      fee=65000,  duration='10 Weeks', icon='⚛️',
                 tools='React, Hooks, Redux, Tailwind', schedule='Weekdays',
                 description='Build modern, fast frontend applications with React.js.'),
            dict(title='Data Analysis',          slug='data-analysis',           level='advanced',
                 category=cat_data,     fee=70000,  duration='12 Weeks', icon='📊',
                 tools='Python, Pandas, Matplotlib, Power BI', schedule='Weekdays / Weekend',
                 description='Analyse real-world data using Python, Pandas, and Power BI.'),
            dict(title='Artificial Intelligence', slug='artificial-intelligence', level='advanced',
                 category=cat_data,     fee=85000,  duration='14 Weeks', icon='🤖',
                 tools='Python, TensorFlow, Scikit-learn, NLP', schedule='Weekdays',
                 description='Learn Machine Learning, Deep Learning, and AI applications.'),
        ]

        count = 0
        for i, data in enumerate(courses):
            _, created = Course.objects.get_or_create(
                slug=data['slug'],
                defaults={**data, 'is_active': True, 'is_featured': True, 'order': i}
            )
            if created:
                count += 1

        self.stdout.write(f'  ✔ {count} courses created ({Course.objects.count()} total)')

    # ── PRODUCTS ───────────────────────────────────────────
    def _create_products(self):
        from apps.shop.models import Product, ProductCategory

        cat_laptop, _  = ProductCategory.objects.get_or_create(name='Laptop',     defaults={'slug': 'laptop',     'icon': '💻'})
        cat_printer, _ = ProductCategory.objects.get_or_create(name='Printer',    defaults={'slug': 'printer',    'icon': '🖨️'})
        cat_access, _  = ProductCategory.objects.get_or_create(name='Accessory',  defaults={'slug': 'accessory',  'icon': '⌨️'})
        cat_net, _     = ProductCategory.objects.get_or_create(name='Networking', defaults={'slug': 'networking', 'icon': '📡'})

        products = [
            dict(name='HP EliteBook 840 G8',      slug='hp-elitebook-840-g8',    category=cat_laptop,
                 price=420000,  old_price=480000,  stock=5, badge='New',
                 icon='💻', description='HP EliteBook 840 G8 — Core i5, 8GB RAM, 256GB SSD. Professional grade laptop.'),
            dict(name='Dell Inspiron 15 3520',    slug='dell-inspiron-15-3520',  category=cat_laptop,
                 price=280000,  old_price=320000,  stock=8, badge='Hot',
                 icon='💻', description='Dell Inspiron 15 3520 — Core i3, 4GB RAM, 1TB HDD. Great student laptop.'),
            dict(name='Lenovo ThinkPad T14',      slug='lenovo-thinkpad-t14',    category=cat_laptop,
                 price=620000,  old_price=None,    stock=3, badge='',
                 icon='💻', description='Lenovo ThinkPad T14 — Core i7, 16GB RAM, 512GB SSD. Premium business laptop.'),
            dict(name='HP LaserJet Pro M404n',    slug='hp-laserjet-pro-m404n',  category=cat_printer,
                 price=145000,  old_price=165000,  stock=6, badge='',
                 icon='🖨️', description='HP LaserJet Pro M404n — Fast monochrome laser printer with network support.'),
            dict(name='Epson EcoTank L3250',      slug='epson-ecotank-l3250',    category=cat_printer,
                 price=95000,   old_price=115000,  stock=10, badge='Sale',
                 icon='🖨️', description='Epson EcoTank L3250 — Colour inkjet with Wi-Fi and ultra-low cost per page.'),
            dict(name='Logitech MK345 Combo',     slug='logitech-mk345-combo',   category=cat_access,
                 price=18500,   old_price=None,    stock=20, badge='',
                 icon='⌨️', description='Logitech MK345 — Wireless keyboard and mouse combo with long battery life.'),
            dict(name='Seagate External HDD 1TB', slug='seagate-external-1tb',   category=cat_access,
                 price=28000,   old_price=None,    stock=15, badge='',
                 icon='💾', description='Seagate Portable 1TB External Hard Drive — USB 3.0 for fast transfers.'),
            dict(name='TP-Link Archer C6 Router', slug='tp-link-archer-c6',      category=cat_net,
                 price=35000,   old_price=None,    stock=12, badge='',
                 icon='📡', description='TP-Link Archer C6 — Dual Band AC1200 Wi-Fi Router for home and office.'),
        ]

        count = 0
        for data in products:
            _, created = Product.objects.get_or_create(
                slug=data['slug'],
                defaults={**data, 'is_active': True, 'is_featured': True}
            )
            if created:
                count += 1

        self.stdout.write(f'  ✔ {count} products created ({Product.objects.count()} total)')

    # ── BLOG POSTS ─────────────────────────────────────────
    def _create_blog_posts(self):
        from apps.blog.models import Post, PostCategory
        import django.utils.timezone as tz

        cat_hw, _   = PostCategory.objects.get_or_create(name='Hardware',    defaults={'slug': 'hardware'})
        cat_prog, _ = PostCategory.objects.get_or_create(name='Programming', defaults={'slug': 'programming'})
        cat_tech, _ = PostCategory.objects.get_or_create(name='Technology',  defaults={'slug': 'technology'})
        cat_sec, _  = PostCategory.objects.get_or_create(name='Security',    defaults={'slug': 'security'})

        admin = User.objects.filter(username='admin').first()

        posts = [
            dict(title='Best Laptops for Students in Nigeria (2025 Guide)',
                 slug='best-laptops-students-nigeria-2025',
                 category=cat_hw, icon='💻', read_time=5,
                 excerpt='Choosing the right laptop can make or break your academic journey. We review the top picks for Nigerian students across different budgets.',
                 content='Full article content goes here. Add via Django Admin.'),
            dict(title='The Complete Python Programming Guide for Beginners',
                 slug='python-programming-guide-beginners',
                 category=cat_prog, icon='🐍', read_time=8,
                 excerpt='Python is the world\'s most beginner-friendly language. Learn how to get started on your coding journey.',
                 content='Full article content goes here. Add via Django Admin.'),
            dict(title='AI Trends Reshaping Businesses in Africa in 2025',
                 slug='ai-trends-africa-2025',
                 category=cat_tech, icon='🤖', read_time=6,
                 excerpt='Discover how Nigerian businesses are leveraging AI for customer service, fraud detection, and logistics.',
                 content='Full article content goes here. Add via Django Admin.'),
            dict(title='Cybersecurity Tips Every Nigerian Business Must Know',
                 slug='cybersecurity-tips-nigerian-business',
                 category=cat_sec, icon='🔒', read_time=7,
                 excerpt='With cybercrime on the rise, protecting your digital assets has never been more critical.',
                 content='Full article content goes here. Add via Django Admin.'),
        ]

        count = 0
        for data in posts:
            _, created = Post.objects.get_or_create(
                slug=data['slug'],
                defaults={**data, 'author': admin, 'is_published': True,
                          'is_featured': True, 'published_at': tz.now()}
            )
            if created:
                count += 1

        self.stdout.write(f'  ✔ {count} blog posts created ({Post.objects.count()} total)')
