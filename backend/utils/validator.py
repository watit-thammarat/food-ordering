from datetime import datetime, timedelta
from django.utils import timezone

from utils import errors
from utils.http_exception import HttpException
from food_ordering.settings import ORDER_DATE_DELTA


def validate_sign_up_sign_in_fields(request):
    email = request.data.get('email')
    if email is None or len(email) == 0:
        raise HttpException(errors.EMAIL_IS_REQUIRED)
    password = request.data.get('password')
    if email is None or len(email) == 0:
        raise HttpException(errors.PASSWORD_IS_REQUIRED)
    return (email, password)


def validate_menu_name_field(request):
    name = request.data.get('name')
    if name is None or len(name) == 0:
        raise HttpException(errors.NAME_IS_REQUIRED)
    return name


def get_date_from_timestamp(request):
    try:
        ts = request.data.get('orderDate')
        date = datetime.fromtimestamp(int(ts))
        return timezone.make_aware(date).date()
    except Exception:
        raise HttpException(errors.INVALID_DATE)


def validate_order_date(request):
    order_date = get_date_from_timestamp(request)
    start_date = timezone.make_aware(datetime.now()).date()
    end_date = start_date + timedelta(days=ORDER_DATE_DELTA)
    if order_date < start_date or order_date > end_date:
        raise HttpException(errors.INVALID_ORDER_DATE)
    return order_date


def validate_menu_id(request):
    menu_id = request.data.get('menuId')
    if menu_id is None or type(menu_id) != int:
        raise HttpException(errors.INVALID_MENU_ID)
    return menu_id


def validate_admin(request):
    if request.user.is_superuser:
        raise HttpException(errors.INVALID_ADMIN)
