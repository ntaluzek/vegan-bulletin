# Vegan Bulletin

A Django-based web application to display an aggregated set of news and events related to veganism in a specific city. The first implementation is for Chicago, IL, but the application is designed to be easily configured for other cities.

## Features

- **News**: Blog-style posts about restaurant openings/closings, product releases, and policy updates
- **Events**: One-off and multi-day events like festivals, markets, and meetups
- **Specials**: Time-limited offerings from businesses (rotating flavors, seasonal items)
- **Promotions**: Recurring or one-time sales and deals with flexible recurrence patterns
- **Resources**: Guides and directories of local vegan resources
- **Organizations**: Central database of vegan businesses and organizations
- **Admin Panel**: Django admin interface for content management
- **Responsive Design**: Built with Bulma CSS framework

## Tech Stack

- **Backend**: Django 5.x
- **Database**: SQLite (easily swappable)
- **Frontend**: Server-side rendering with Bulma CSS
- **Images**: Pillow for image handling
- **Recurrence**: django-recurrence for promotion scheduling
- **Deployment**: Docker & Docker Compose

## Project Structure

```
vegan-bulletin/
├── bulletin/              # Main Django app
│   ├── models.py         # Data models
│   ├── views.py          # View logic
│   ├── admin.py          # Admin configuration
│   ├── urls.py           # URL routing
│   └── context_processors.py  # Template context
├── config/               # Django project configuration
│   ├── settings.py       # Settings
│   └── urls.py           # Root URL config
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   └── bulletin/        # App templates
├── static/              # Static files (CSS, JS)
├── media/               # User-uploaded content
├── docker-compose.yml   # Docker composition
├── Dockerfile           # Docker image definition
├── .env.template        # Environment variables template
└── pyproject.toml       # Python dependencies
```

## Installation and Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/vegan-bulletin.git
   cd vegan-bulletin
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow python-decouple django-recurrence
   ```

4. **Create environment file**
   ```bash
   cp .env.template .env
   ```
   Edit `.env` and update the values as needed.

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Website: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

### Docker Deployment

1. **Create environment file**
   ```bash
   cp .env.template .env
   ```
   Edit `.env` with your production settings.

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Create a superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Access the application**
   - Website: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

### Portainer Deployment

1. In Portainer, go to **Stacks** > **Add Stack**
2. Name your stack (e.g., "vegan-bulletin")
3. Upload or paste the `docker-compose.yml` content
4. Add environment variables from `.env.template`
5. Deploy the stack
6. Access the container console to create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Configuration

The application uses environment variables for city-specific configuration. Edit the `.env` file:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# City Configuration
CITY_NAME=Chicago
CITY_STATE=IL
CITY_TIMEZONE=America/Chicago
CONTACT_EMAIL=chicagoveganbulletin@gmail.com

# Database
DATABASE_NAME=db.sqlite3
```

### Configuring for a Different City

To use this application for a different city:

1. Update the environment variables in `.env`:
   - `CITY_NAME`: Name of the city (e.g., "Los Angeles")
   - `CITY_STATE`: Two-letter state code (e.g., "CA")
   - `CITY_TIMEZONE`: Timezone (e.g., "America/Los_Angeles")
   - `CONTACT_EMAIL`: Contact email for the city's bulletin

2. No code changes required! The application will automatically use these values throughout.

## Usage

### Adding Content

All content is managed through the Django admin panel at `/admin`:

1. **Organizations**: Add businesses, restaurants, sanctuaries, etc.
2. **Images**: Upload images to be used in posts
3. **News**: Create news articles
4. **Events**: Add upcoming events
5. **Specials**: Post time-limited offerings
6. **Promotions**: Set up recurring deals
7. **Resources**: Publish guides and directories

### Creating Recurring Events

For recurring events (like weekly farmers markets):
1. Create the first event with all details
2. Manually create additional event instances for each occurrence
3. Each event can be edited independently after creation

### Setting Up Promotion Recurrence

Promotions support complex recurrence patterns:
- Daily
- Weekly (specific days of the week)
- Bi-weekly
- Monthly
- Custom patterns using django-recurrence

## Data Models

### Organization
Business or organization with contact info, location, and social media

### News
Blog-style posts with title, content, images, and optional organization link

### Event
Single or multi-day events with date/time, location, and registration info

### Special
Limited-time offerings with start/end dates

### Promotion
Recurring or one-time deals with recurrence patterns

### Resource
Guides and directories with multiple organization associations

### Image
Reusable images with captions and alt text

## Security Notes

- Keep `SECRET_KEY` secret and unique in production
- Set `DEBUG=False` in production
- The `.gitignore` file prevents sensitive files from being committed
- Media files are stored in a separate volume in Docker
- Admin panel requires authentication

## Future Enhancements

- User accounts and customization (filters, favorites)
- Frontend forms for content submission (currently admin-only)
- Email notifications for new events
- Calendar integration
- Mobile app
- Multi-city support in a single instance
- SEO optimizations

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
- Open an issue on GitHub
- Email: chicagoveganbulletin@gmail.com

## Credits

Built with:
- [Django](https://www.djangoproject.com/)
- [Bulma CSS](https://bulma.io/)
- [Font Awesome](https://fontawesome.com/)
- [django-recurrence](https://github.com/django-recurrence/django-recurrence)
