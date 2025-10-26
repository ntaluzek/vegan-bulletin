#!/usr/bin/env python
"""
Helper script for common management tasks.
Run this to get started quickly with the vegan bulletin site.
"""

import os
import sys
import subprocess


def main():
    print("=" * 60)
    print("Vegan Bulletin - Setup Helper")
    print("=" * 60)
    print()

    # Check if .env exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found!")
        create_env = input("Would you like to create one from the template? (y/n): ")
        if create_env.lower() == 'y':
            import shutil
            shutil.copy('.env.template', '.env')
            print("✓ Created .env file from template")
            print("  Please edit .env with your configuration before continuing.")
            return
        else:
            print("  Please create a .env file before continuing.")
            return

    print("Select an option:")
    print()
    print("1. Run migrations")
    print("2. Create superuser")
    print("3. Collect static files")
    print("4. Start development server")
    print("5. Run all setup steps (1-3)")
    print("6. Exit")
    print()

    choice = input("Enter your choice (1-6): ")

    if choice == '1':
        run_migrations()
    elif choice == '2':
        create_superuser()
    elif choice == '3':
        collect_static()
    elif choice == '4':
        run_server()
    elif choice == '5':
        run_migrations()
        create_superuser()
        collect_static()
        print("\n✓ Setup complete!")
        print("  Run option 4 to start the development server.")
    elif choice == '6':
        print("Goodbye!")
        return
    else:
        print("Invalid choice. Please try again.")


def run_migrations():
    print("\n📊 Running database migrations...")
    subprocess.run([sys.executable, 'manage.py', 'migrate'])
    print("✓ Migrations complete")


def create_superuser():
    print("\n👤 Creating superuser account...")
    subprocess.run([sys.executable, 'manage.py', 'createsuperuser'])
    print("✓ Superuser created")


def collect_static():
    print("\n📁 Collecting static files...")
    subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'])
    print("✓ Static files collected")


def run_server():
    print("\n🚀 Starting development server...")
    print("   Access the site at http://localhost:8000")
    print("   Admin panel at http://localhost:8000/admin")
    print("   Press Ctrl+C to stop the server")
    print()
    subprocess.run([sys.executable, 'manage.py', 'runserver'])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)
