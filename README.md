# E-Commerce Website

A full-featured e-commerce web application built with Django, featuring product management, shopping cart, wishlist, user authentication, and payment integration.

## 🚀 Features

### Core Features
- **Product Management**
  - Product catalog with categories
  - Product images and multiple image support
  - Product tags for better organization
  - Product reviews and ratings
  - Discount pricing support
  - Stock management

- **Shopping Experience**
  - Browse products by category
  - Search functionality
  - Filter products by category and price range
  - Product detail pages with related products
  - Tag-based product browsing

- **Shopping Cart**
  - Add/remove items from cart
  - Update item quantities
  - Session-based cart management
  - Real-time cart updates via AJAX

- **User Features**
  - User registration and authentication
  - User profiles with customizable information
  - Wishlist functionality
  - Order history
  - Multiple shipping addresses management
  - Default address selection

- **Checkout & Payments**
  - Secure checkout process
  - PayPal payment integration
  - Order management
  - Order tracking

- **Additional Features**
  - Newsletter subscription
  - Product reviews and ratings system
  - Responsive design
  - Admin panel for product management

## 🛠️ Technology Stack

- **Backend Framework**: Django 5.2.6
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS, JavaScript
- **Additional Packages**:
  - `django-taggit` - For product tagging
  - `shortuuid` - For unique ID generation

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecomprj
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install django
   pip install django-taggit
   pip install shortuuid
   ```

   Or create a `requirements.txt` file with:
   ```
   Django==5.2.6
   django-taggit==5.0.0
   shortuuid==1.0.11
   Pillow==10.0.0
   ```
   
   Then install:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
ecomprj/
├── core/                    # Main application
│   ├── models.py           # Database models (Product, Category, Cart, Order, etc.)
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   ├── forms.py            # Form definitions
│   ├── admin.py            # Admin configuration
│   └── migrations/         # Database migrations
│
├── userauth/                # User authentication app
│   ├── models.py           # Custom User model
│   ├── views.py            # Authentication views
│   ├── urls.py             # Auth URL routing
│   └── forms.py            # Registration/login forms
│
├── templates/               # HTML templates
│   ├── core/               # Core app templates
│   ├── userauth/           # Auth templates
│   └── partials/           # Reusable template components
│
├── static/                  # Static files (CSS, JS, images)
│   └── assets/
│       ├── css/
│       └── js/
│
├── media/                   # User-uploaded files
│   ├── products/           # Product images
│   ├── category/           # Category images
│   └── user_images/        # User profile images
│
├── ecomprj/                 # Project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
│
└── manage.py                # Django management script
```

## 🗄️ Database Models

### Core Models

- **Category**: Product categories with images
- **Product**: Products with title, description, price, images, and tags
- **ProductImage**: Multiple images per product
- **ProductReview**: User reviews and ratings for products
- **CartOrder**: Shopping cart orders
- **OrderedItems**: Items within an order
- **Wishlist**: User wishlist items
- **Address**: User shipping addresses
- **Mail**: Newsletter subscription emails

### User Model

- Custom User model extending AbstractUser
- Email-based authentication
- User profile with image, title, and description

## 🔐 User Authentication

- **Registration**: `/user/sign-up/`
- **Login**: `/user/login/`
- **Logout**: `/user/logout/`

## 📍 Key URLs

- **Home**: `/` or `/home/`
- **All Products**: `/all-products/`
- **Categories**: `/category/`
- **Category Products**: `/category/<id>/`
- **Product Detail**: `/product/<id>/`
- **Tagged Products**: `/tag/<tag_slug>/`
- **Search**: `/search/?q=<query>`
- **Cart**: `/cart/`
- **Checkout**: `/checkout/`
- **Wishlist**: `/wishlist/`
- **Profile**: `/profile/`

## 🎯 Usage

### For Administrators

1. Access the admin panel at `/admin/`
2. Add categories and products
3. Manage orders and user accounts
4. View and manage product reviews

### For Users

1. **Browse Products**
   - View all products on the home page
   - Filter by category or price range
   - Search for specific products
   - Browse products by tags

2. **Shopping**
   - Add products to cart
   - Update quantities in cart
   - Add products to wishlist
   - View product details and reviews

3. **Checkout**
   - Review cart items
   - Add/select shipping address
   - Complete payment via PayPal
   - Track orders in profile

4. **Account Management**
   - Update profile information
   - Manage shipping addresses
   - View order history
   - Manage wishlist

## 🔒 Security Notes

⚠️ **Important**: Before deploying to production:

1. Change the `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Set up proper database (PostgreSQL recommended)
5. Configure static files serving
6. Set up HTTPS
7. Configure email backend for production
8. Review and update security settings

## 🚀 Deployment

For production deployment:

1. Use a production-ready database (PostgreSQL)
2. Configure environment variables for sensitive data
3. Set up a web server (Nginx + Gunicorn)
4. Configure static and media file serving
5. Set up SSL certificates
6. Configure email backend
7. Set up proper logging

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Developed as an e-commerce solution using Django.

## 📞 Support

For issues, questions, or contributions, please open an issue on the repository.

---

