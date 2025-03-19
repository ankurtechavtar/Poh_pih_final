from django.contrib import admin
from .models import CustomUser, DanceLevel, Interest, Style, UserInterest, SubscriptionPlan, UserSubscription, UsageTracking, Payment, PasswordResetOTP
# PasswordResetToken

# Register the CustomUser model
admin.site.register(CustomUser)

# Register DanceLevel, Interest, and Style models
admin.site.register(DanceLevel)
admin.site.register(Interest)
admin.site.register(Style)

# Register UserInterest model with custom display (Optional: Add list display for clarity)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_interests')

    def get_interests(self, obj):
        return ", ".join([interest.name for interest in obj.interests.all()])
    get_interests.short_description = 'Interests'

admin.site.register(UserInterest, UserInterestAdmin)

# Register SubscriptionPlan model with custom display
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'monthly_fee', 'video_analysis_limit', 'reference_comparison_available', 'process_tracking_available')

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)

# Register UserSubscription model with custom display
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active', 'created_at')
    list_filter = ('plan', 'is_active')

admin.site.register(UserSubscription, UserSubscriptionAdmin)

# Register UsageTracking model with custom display
class UsageTrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'videos_analyzed')
    list_filter = ('month',)

admin.site.register(UsageTracking, UsageTrackingAdmin)

# Register Payment model with custom display
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_type', 'subscription_start_date', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'plan_type')

admin.site.register(Payment, PaymentAdmin)

# Register PasswordResetToken model
# class PasswordResetTokenAdmin(admin.ModelAdmin):
#     list_display = ('user', 'token', 'created_at')
#     search_fields = ('token',)

# admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)

class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at')
    search_fields = ('otp',)

admin.site.register(PasswordResetOTP, PasswordResetOTPAdmin)
