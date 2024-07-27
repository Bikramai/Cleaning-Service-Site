from src.core.bll import get_or_create_application
from src.services.whisper.main import NotificationService


def notify_user_on_service_create(obj):
    description = f'Hi {obj.name}! Your Service Request has been Submitted.'
    notifier = NotificationService(description, description, obj)
    notifier.send_email_notification(
        template="payments/email/service_request_created_user.html",
        context={'obj': obj, 'description': description}, email=[obj.email]
    )


def notify_admin_on_service_create(obj):
    application = get_or_create_application()
    description = f'Hi Admin! New Request has been arrived.'
    notifier = NotificationService(description, description, obj)
    notifier.send_email_notification(
        template="payments/email/service_request_admin.html",
        context={'obj': obj, 'description': description}, email=[application.admin_email]
    )


def notify_admin_and_user_on_service_create(obj):
    notify_user_on_service_create(obj)
    notify_admin_on_service_create(obj)