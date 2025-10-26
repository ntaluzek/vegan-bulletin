from django.contrib import admin
from django.utils.html import format_html
from .models import Organization, Image, News, Event, Special, Promotion, Resource


class ImageInline(admin.TabularInline):
    """Inline admin for managing images."""
    model = None  # Will be set per model
    extra = 1
    fields = ('image', 'caption', 'alt_text')


class NewsImageInline(admin.TabularInline):
    model = News.images.through
    extra = 1
    verbose_name = "Image"
    verbose_name_plural = "Images"


class EventImageInline(admin.TabularInline):
    model = Event.images.through
    extra = 1
    verbose_name = "Image"
    verbose_name_plural = "Images"


class SpecialImageInline(admin.TabularInline):
    model = Special.images.through
    extra = 1
    verbose_name = "Image"
    verbose_name_plural = "Images"


class PromotionImageInline(admin.TabularInline):
    model = Promotion.images.through
    extra = 1
    verbose_name = "Image"
    verbose_name_plural = "Images"


class ResourceImageInline(admin.TabularInline):
    model = Resource.images.through
    extra = 1
    verbose_name = "Image"
    verbose_name_plural = "Images"


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'city', 'state', 'website_link', 'created_at')
    list_filter = ('category', 'state', 'city')
    search_fields = ('name', 'description', 'city')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Contact Information', {
            'fields': ('website', 'email', 'phone')
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram', 'twitter')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Media', {
            'fields': ('logo',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">View</a>', obj.website)
        return "-"
    website_link.short_description = "Website"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'alt_text', 'image_preview', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('caption', 'alt_text')
    readonly_fields = ('uploaded_at', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'published_date', 'is_published', 'author')
    list_filter = ('is_published', 'published_date', 'organization')
    search_fields = ('title', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('images',)

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'summary', 'content')
        }),
        ('Relationships', {
            'fields': ('organization', 'images')
        }),
        ('Publishing', {
            'fields': ('author', 'published_date', 'is_published', 'source_url')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'city', 'organization', 'is_published')
    list_filter = ('is_published', 'start_date', 'city', 'state')
    search_fields = ('title', 'description', 'venue_name', 'city')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('images',)

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'summary', 'description')
        }),
        ('Date & Time', {
            'fields': ('start_date', 'end_date', 'start_time', 'end_time')
        }),
        ('Location', {
            'fields': ('venue_name', 'address', 'city', 'state', 'zip_code')
        }),
        ('Relationships', {
            'fields': ('organization', 'images')
        }),
        ('Additional Info', {
            'fields': ('website', 'registration_url', 'cost')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Special)
class SpecialAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'start_date', 'end_date', 'is_active', 'is_published')
    list_filter = ('is_published', 'start_date', 'organization')
    search_fields = ('title', 'description', 'organization__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'is_active')
    filter_horizontal = ('images',)

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'summary', 'description')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
        ('Relationships', {
            'fields': ('organization', 'images')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'recurrence_type', 'valid_from', 'valid_until', 'is_published')
    list_filter = ('is_published', 'recurrence_type', 'organization')
    search_fields = ('title', 'description', 'organization__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('images',)

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'summary', 'description')
        }),
        ('Recurrence', {
            'fields': ('recurrence_type', 'recurrence_pattern')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until', 'start_time', 'end_time')
        }),
        ('Relationships', {
            'fields': ('organization', 'images')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'published_date', 'is_published', 'author')
    list_filter = ('is_published', 'resource_type', 'published_date')
    search_fields = ('title', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('organizations', 'images')

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'resource_type', 'summary', 'content')
        }),
        ('Relationships', {
            'fields': ('organizations', 'images')
        }),
        ('Publishing', {
            'fields': ('author', 'published_date', 'is_published')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
