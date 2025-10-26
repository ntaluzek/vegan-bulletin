# Quick Start Guide

Get your Vegan Bulletin site up and running in minutes!

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git

## Quick Setup (Local Development)

### Option 1: Using the Helper Script (Recommended)

1. **Clone and navigate to the project**
   ```bash
   git clone https://github.com/yourusername/vegan-bulletin.git
   cd vegan-bulletin
   ```

2. **Install dependencies**
   ```bash
   pip install django pillow python-decouple django-recurrence
   ```

3. **Run the setup helper**
   ```bash
   python manage_site.py
   ```

   The script will guide you through:
   - Creating the `.env` file
   - Running migrations
   - Creating a superuser account
   - Collecting static files
   - Starting the server

### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/vegan-bulletin.git
   cd vegan-bulletin
   ```

2. **Install dependencies**
   ```bash
   pip install django pillow python-decouple django-recurrence
   ```

3. **Create environment file**
   ```bash
   cp .env.template .env
   ```
   Edit `.env` if needed (defaults work for local development)

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Start the server**
   ```bash
   python manage.py runserver
   ```

8. **Access the site**
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin

## Quick Setup (Docker)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/vegan-bulletin.git
   cd vegan-bulletin
   ```

2. **Create environment file**
   ```bash
   cp .env.template .env
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the site**
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin

## First Steps After Setup

1. **Log into the admin panel** at http://localhost:8000/admin

2. **Add an organization** (e.g., a local vegan restaurant)
   - Go to Organizations → Add Organization
   - Fill in the details

3. **Create your first news post**
   - Go to News → Add News
   - Write a post about something happening in your city
   - Add images if desired

4. **Add an upcoming event**
   - Go to Events → Add Event
   - Fill in date, time, location details

5. **View your site** at http://localhost:8000
   - See your content displayed on the homepage!

## Common Tasks

### Adding Images
1. Go to Images → Add Image
2. Upload an image file
3. Add caption and alt text
4. Save
5. When creating News/Events/etc, select this image from the list

### Creating a Recurring Promotion
1. Go to Promotions → Add Promotion
2. Set the recurrence type (e.g., "Weekly")
3. Configure the recurrence pattern
4. Set valid from/until dates
5. Save

### Viewing Past Events
- Events page has a toggle to show past events
- By default, only upcoming events are shown

## Customizing for Your City

Edit the `.env` file:

```env
CITY_NAME=YourCity
CITY_STATE=XX
CITY_TIMEZONE=America/YourTimezone
CONTACT_EMAIL=youremail@example.com
```

Restart the server to see changes.

## Troubleshooting

### Static files not loading?
```bash
python manage.py collectstatic --noinput
```

### Database issues?
```bash
python manage.py migrate
```

### Port 8000 already in use?
```bash
python manage.py runserver 8080
```
Then access at http://localhost:8080

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Open an issue on GitHub
- Email: chicagoveganbulletin@gmail.com

## Next Steps

- Explore the admin panel to see all available models
- Customize the templates in `templates/bulletin/`
- Add your own styling in `static/`
- Set up for production deployment (see README.md)
