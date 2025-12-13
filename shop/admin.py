from django.contrib import admin
from .models import *

# class CategoryAdmin(admin.ModelAdmin):
#     list_display=['name','description','status','image']

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Favourite)

class OrderItemInline(admin.TabularInline):
    """Inline view for order items"""
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'total']
    can_delete = True
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Enhanced Order Admin"""
    list_display = [
        'order_number', 
        'user', 
        'full_name', 
        'total_amount', 
        'status', 
        'payment_mode',
        'created_at'
    ]
    
    list_filter = [
        'status', 
        'payment_mode', 
        'created_at',
        'updated_at'
    ]
    
    search_fields = [
        'order_number', 
        'full_name', 
        'email', 
        'phone',
        'user__username'
    ]
    
    readonly_fields = [
        'order_number', 
        'user', 
        'total_amount',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_mode', 'total_amount')
        }),
        ('Customer Details', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('address', 'city', 'state', 'pincode')
        }),
        ('Additional Information', {
            'fields': ('order_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [OrderItemInline]
    
    # Actions
    actions = ['mark_as_confirmed', 'mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='Confirmed')
        self.message_user(request, f'{updated} order(s) marked as Confirmed.')
    mark_as_confirmed.short_description = "Mark selected orders as Confirmed"
    
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='Processing')
        self.message_user(request, f'{updated} order(s) marked as Processing.')
    mark_as_processing.short_description = "Mark selected orders as Processing"
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='Shipped')
        self.message_user(request, f'{updated} order(s) marked as Shipped.')
    mark_as_shipped.short_description = "Mark selected orders as Shipped"
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='Delivered')
        self.message_user(request, f'{updated} order(s) marked as Delivered.')
    mark_as_delivered.short_description = "Mark selected orders as Delivered"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='Cancelled')
        self.message_user(request, f'{updated} order(s) marked as Cancelled.')
    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"
    
    # Custom styling
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Order Item Admin"""
    list_display = [
        'id',
        'order',
        'product',
        'quantity',
        'price',
        'total',
        'created_at'
    ]
    
    list_filter = ['created_at']
    
    search_fields = [
        'order__order_number',
        'product__name'
    ]
    
    readonly_fields = [
        'order',
        'product',
        'quantity',
        'price',
        'total',
        'created_at'
    ]
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True
