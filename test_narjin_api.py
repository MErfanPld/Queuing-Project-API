#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import json
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# ==================== تنظیمات اولیه ====================
BASE_URL = "http://localhost:8000"  # آدرس سرورت رو اینجا بذار
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# کاربرهای تست
TEST_USERS = {
    "user_a": {
        "phone": "09912146530",
        "password": "erfan1070",
        # "name": "کاربر A"
    },
    "user_b": {
        "phone": "09912146084",
        "password": "erfan1070",
        # "name": "کاربر B"
    }
}

# متغیرهای سراسری برای ذخیره توکن‌ها و داده‌ها
TOKENS = {}
DATA = {
    "business_a": None,
    "business_b": None,
    "employee_a": None,
    "service_a": None,
    "slot_a": None,
    "appointment_a": None
}

# رنگ‌ها برای خروجی زیباتر
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# ==================== توابع کمکی ====================

def log_test(name: str):
    """لاگ شروع تست"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}🧪 تست: {name}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")

def log_success(message: str):
    """لاگ موفقیت"""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def log_error(message: str):
    """لاگ خطا"""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def log_warning(message: str):
    """لاگ هشدار"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def log_info(message: str):
    """لاگ اطلاعات"""
    print(f"{Colors.BLUE}ℹ {message}{Colors.RESET}")

def make_request(method: str, endpoint: str, data: Optional[Dict] = None, token: Optional[str] = None, expected_status: int = 200) -> tuple:
    """
    ارسال درخواست HTTP
    Returns: (success: bool, response_data: dict, status_code: int)
    """
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"
    headers = HEADERS.copy()
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=data, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=10)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            log_error(f"متد نامعتبر: {method}")
            return False, {}, 0
        
        # لاگ درخواست
        log_info(f"{method.upper()} {url} → Status: {response.status_code}")
        
        try:
            response_data = response.json()
        except:
            response_data = {}
        
        success = response.status_code == expected_status
        
        if not success:
            log_error(f"خطا: {response.status_code}")
            if response_data:
                log_error(f"پاسخ: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        
        return success, response_data, response.status_code
    
    except requests.exceptions.RequestException as e:
        log_error(f"خطا در اتصال: {str(e)}")
        return False, {}, 0

def wait(seconds: float = 0.5):
    """صبر کوتاه بین تست‌ها"""
    time.sleep(seconds)

# ==================== بخش ۱: احراز هویت و کاربر ====================

def test_auth():
    """تست احراز هویت"""
    log_test("بخش ۱: احراز هویت و کاربر")
    
    results = []
    
    # سناریو ۱.۱: ثبت‌نام کاربر جدید
    log_info("سناریو ۱.۱: ثبت‌نام کاربر جدید")
    success, data, status = make_request(
        "POST",
        "/auth/register/",
        data={
            "phone_number": TEST_USERS["user_a"]["phone"],
            "password": TEST_USERS["user_a"]["password"],
            "first_name": "کاربر",
            "last_name": "اول"
        },
        expected_status=201
    )
    results.append(("ثبت‌نام کاربر A", success))
    wait()
    
    # سناریو ۱.۲: ثبت‌نام کاربر دوم
    log_info("سناریو ۱.۲: ثبت‌نام کاربر دوم")
    success, data, status = make_request(
        "POST",
        "/auth/register/",
        data={
            "phone_number": TEST_USERS["user_b"]["phone"],
            "password": TEST_USERS["user_b"]["password"],
            "first_name": "کاربر",
            "last_name": "دوم"
        },
        expected_status=201
    )
    results.append(("ثبت‌نام کاربر B", success))
    wait()
    
    # سناریو ۱.۳: لاگین با شماره درست
    log_info("سناریو ۱.۳: لاگین با شماره درست")
    success, data, status = make_request(
        "POST",
        "/auth/login/",
        data={
            "phone_number": TEST_USERS["user_a"]["phone"],
            "password": TEST_USERS["user_a"]["password"]
        },
        expected_status=200
    )
    if success and "access" in data:
        TOKENS["user_a"] = data["access"]
        log_success(f"توکن دریافت شد: {TOKENS['user_a'][:20]}...")
    results.append(("لاگین کاربر A", success and "access" in data))
    wait()
    
    # سناریو ۱.۴: لاگین با پسورد اشتباه
    log_info("سناریو ۱.۴: لاگین با پسورد اشتباه")
    success, data, status = make_request(
        "POST",
        "/auth/login/",
        data={
            "phone_number": TEST_USERS["user_a"]["phone"],
            "password": "wrong_password"
        },
        expected_status=401
    )
    results.append(("لاگین با پسورد اشتباه", success))
    wait()
    
    # سناریو ۱.۵: لاگین کاربر B
    log_info("سناریو ۱.۵: لاگین کاربر B")
    success, data, status = make_request(
        "POST",
        "/auth/login/",
        data={
            "phone_number": TEST_USERS["user_b"]["phone"],
            "password": TEST_USERS["user_b"]["password"]
        },
        expected_status=200
    )
    if success and "access" in data:
        TOKENS["user_b"] = data["access"]
        log_success(f"توکن دریافت شد: {TOKENS['user_b'][:20]}...")
    results.append(("لاگین کاربر B", success and "access" in data))
    wait()
    
    # سناریو ۱.۶: درخواست بدون توکن
    log_info("سناریو ۱.۶: درخواست بدون توکن")
    success, data, status = make_request(
        "GET",
        "/business/",
        expected_status=401
    )
    results.append(("درخواست بدون توکن", success))
    wait()
    
    return results

# ==================== بخش ۲: مدیریت کسب‌وکار ====================

def test_business():
    """تست مدیریت کسب‌وکار"""
    log_test("بخش ۲: مدیریت کسب‌وکار")
    
    if not TOKENS.get("user_a"):
        log_error("توکن کاربر A موجود نیست!")
        return [("مدیریت کسب‌وکار", False)]
    
    results = []
    
    # سناریو ۲.۱: ایجاد ارایشگاه جدید
    log_info("سناریو ۲.۱: ایجاد ارایشگاه جدید")
    success, data, status = make_request(
        "POST",
        "/business/create/",
        data={
            "name": "آرایشگاه گل",
            "slug": "gol-salon",
            "business_type": "salon",
            "address": "تهران، خیابان ولیعصر، پلاک 123",
            "telephone_number": "02112345678",
            "phone_number": TEST_USERS["user_a"]["phone"],
            "is_coffee_shop": True,
            "is_parking": False
        },
        token=TOKENS["user_a"],
        expected_status=201
    )
    if success:
        DATA["business_a"] = data
        log_success(f"ارایشگاه ایجاد شد! ID: {data.get('id')}, کد: {data.get('random_code')}")
    results.append(("ایجاد ارایشگاه", success))
    wait()
    
    # سناریو ۲.۲: مشاهده لیست ارایشگاه‌های خود
    log_info("سناریو ۲.۲: مشاهده لیست ارایشگاه‌های خود")
    success, data, status = make_request(
        "GET",
        "/business/",
        token=TOKENS["user_a"],
        expected_status=200
    )
    has_business = success and len(data) > 0
    if has_business:
        log_success(f"تعداد ارایشگاه‌ها: {len(data)}")
    results.append(("لیست ارایشگاه‌های خود", has_business))
    wait()
    
    # سناریو ۲.۳: مشاهده ارایشگاه خود (BusinessMe)
    log_info("سناریو ۲.۳: مشاهده ارایشگاه خود")
    success, data, status = make_request(
        "GET",
        "/business/me/",
        token=TOKENS["user_a"],
        expected_status=200
    )
    results.append(("اطلاعات ارایشگاه خود", success))
    wait()
    
    # سناریو ۲.۴: آپدیت ارایشگاه
    log_info("سناریو ۲.۴: آپدیت ارایشگاه")
    if DATA["business_a"]:
        success, data, status = make_request(
            "PUT",
            f"/business/{DATA['business_a']['id']}/",
            data={
                "name": "آرایشگاه گل - نسخه جدید",
                "address": "تهران، فرشته"
            },
            token=TOKENS["user_a"],
            expected_status=200
        )
        results.append(("آپدیت ارایشگاه", success))
    else:
        results.append(("آپدیت ارایشگاه", False))
        log_error("ارایشگاه برای آپدیت موجود نیست!")
    wait()
    
    # ایجاد ارایشگاه برای کاربر B (برای تست امنیت)
    log_info("ایجاد ارایشگاه برای کاربر B (تست امنیت)")
    success, data, status = make_request(
        "POST",
        "/business/create/",
        data={
            "name": "آرایشگاه لاله",
            "slug": "laleh-salon",
            "business_type": "salon",
            "address": "اصفهان، چهارباغ",
            "telephone_number": "03112345678",
            "phone_number": TEST_USERS["user_b"]["phone"],
            "is_coffee_shop": False,
            "is_parking": True
        },
        token=TOKENS["user_b"],
        expected_status=201
    )
    if success:
        DATA["business_b"] = data
        log_success(f"ارایشگاه کاربر B ایجاد شد! کد: {data.get('random_code')}")
    wait()
    
    return results

# ==================== بخش ۳: مدیریت کارمندان ====================

def test_employees():
    """تست مدیریت کارمندان"""
    log_test("بخش ۳: مدیریت کارمندان")
    
    if not TOKENS.get("user_a") or not DATA.get("business_a"):
        log_error("توکن یا ارایشگاه موجود نیست!")
        return [("مدیریت کارمندان", False)]
    
    results = []
    
    # سناریو ۳.۱: ایجاد کارمند جدید
    log_info("سناریو ۳.۱: ایجاد کارمند جدید")
    # اول یه کاربر جدید بسازیم برای کارمند
    success, user_data, status = make_request(
        "POST",
        "/auth/register/",
        data={
            "phone_number": "09121112233",
            "password": "employee123",
            "first_name": "سارا",
            "last_name": "کارمند"
        },
        expected_status=201
    )
    wait()
    
    if success:
        # حالا کارمند رو اضافه کن
        success, data, status = make_request(
            "POST",
            "/business/employees/create/",
            data={
                "user_id": user_data.get("id"),
                "skill": "کارشناس نگاه و ابرو"
            },
            token=TOKENS["user_a"],
            expected_status=201
        )
        if success:
            DATA["employee_a"] = data
            log_success(f"کارمند ایجاد شد! ID: {data.get('id')}")
        results.append(("ایجاد کارمند", success))
    else:
        results.append(("ایجاد کارمند", False))
        log_error("کاربر برای کارمند ایجاد نشد!")
    wait()
    
    # سناریو ۳.۲: لیست کارمندان ارایشگاه
    log_info("سناریو ۳.۲: لیست کارمندان ارایشگاه")
    success, data, status = make_request(
        "GET",
        "/business/employees/",
        token=TOKENS["user_a"],
        expected_status=200
    )
    has_employees = success and len(data) > 0
    if has_employees:
        log_success(f"تعداد کارمندان: {len(data)}")
    results.append(("لیست کارمندان", has_employees))
    wait()
    
    # سناریو ۳.۳: آپدیت کارمند
    log_info("سناریو ۳.۳: آپدیت کارمند")
    if DATA["employee_a"]:
        success, data, status = make_request(
            "PUT",
            f"/business/employees/update/{DATA['employee_a']['id']}/",
            data={
                "skill": "کارشناس ارشد نگاه و ابرو"
            },
            token=TOKENS["user_a"],
            expected_status=200
        )
        results.append(("آپدیت کارمند", success))
    else:
        results.append(("آپدیت کارمند", False))
    wait()
    
    return results

# ==================== بخش ۴: مدیریت سرویس‌ها ====================

def test_services():
    """تست مدیریت سرویس‌ها"""
    log_test("بخش ۴: مدیریت سرویس‌ها")
    
    if not TOKENS.get("user_a") or not DATA.get("business_a"):
        log_error("توکن یا ارایشگاه موجود نیست!")
        return [("مدیریت سرویس‌ها", False)]
    
    results = []
    
    # سناریو ۴.۱: ایجاد سرویس جدید
    log_info("سناریو ۴.۱: ایجاد سرویس جدید")
    service_data = {
        "name": "کوتاهی مو مردانه",
        "description": "کوتاهی مو با تیغ و قیچی",
        "duration": "00:30:00",
        "price": 150000,
        "is_active": True
    }
    
    if DATA.get("employee_a"):
        service_data["employee_id"] = DATA["employee_a"]["id"]
    
    success, data, status = make_request(
        "POST",
        "/business/services/create/",
        data=service_data,
        token=TOKENS["user_a"],
        expected_status=201
    )
    if success:
        DATA["service_a"] = data
        log_success(f"سرویس ایجاد شد! ID: {data.get('id')}, قیمت: {data.get('price')}")
    results.append(("ایجاد سرویس", success))
    wait()
    
    # سناریو ۴.۲: لیست سرویس‌های ارایشگاه
    log_info("سناریو ۴.۲: لیست سرویس‌های ارایشگاه")
    success, data, status = make_request(
        "GET",
        "/business/services/",
        token=TOKENS["user_a"],
        expected_status=200
    )
    has_services = success and len(data) > 0
    if has_services:
        log_success(f"تعداد سرویس‌ها: {len(data)}")
    results.append(("لیست سرویس‌ها", has_services))
    wait()
    
    # سناریو ۴.۳: آپدیت سرویس
    log_info("سناریو ۴.۳: آپدیت سرویس")
    if DATA["service_a"]:
        success, data, status = make_request(
            "PUT",
            f"/business/services/{DATA['service_a']['id']}/",
            data={
                "price": 200000
            },
            token=TOKENS["user_a"],
            expected_status=200
        )
        results.append(("آپدیت سرویس", success))
    else:
        results.append(("آپدیت سرویس", False))
    wait()
    
    return results

# ==================== بخش ۵: مدیریت بازه‌های زمانی ====================

def test_time_slots():
    """تست مدیریت بازه‌های زمانی"""
    log_test("بخش ۵: مدیریت بازه‌های زمانی")
    
    if not TOKENS.get("user_a") or not DATA.get("service_a"):
        log_error("توکن یا سرویس موجود نیست!")
        return [("مدیریت بازه‌های زمانی", False)]
    
    results = []
    
    # تاریخ فردا برای تست
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # سناریو ۵.۱: ایجاد بازه زمانی
    log_info(f"سناریو ۵.۱: ایجاد بازه زمانی (تاریخ: {tomorrow})")
    success, data, status = make_request(
        "POST",
        "/business/slots/create/",
        data={
            "service_id": DATA["service_a"]["id"],
            "date": tomorrow,
            "start_time": "10:00"
        },
        token=TOKENS["user_a"],
        expected_status=201
    )
    if success:
        DATA["slot_a"] = data
        log_success(f"بازه زمانی ایجاد شد! ID: {data.get('id')}, ساعت: {data.get('start_time')}")
    results.append(("ایجاد بازه زمانی", success))
    wait()
    
    # سناریو ۵.۲: لیست بازه‌های زمانی
    log_info("سناریو ۵.۲: لیست بازه‌های زمانی")
    success, data, status = make_request(
        "GET",
        "/business/slots/",
        token=TOKENS["user_a"],
        expected_status=200
    )
    has_slots = success and len(data) > 0
    if has_slots:
        log_success(f"تعداد بازه‌ها: {len(data)}")
    results.append(("لیست بازه‌های زمانی", has_slots))
    wait()
    
    # سناریو ۵.۳: فیلتر بازه‌ها با تاریخ
    log_info("سناریو ۵.۳: فیلتر بازه‌ها با تاریخ")
    success, data, status = make_request(
        "GET",
        f"/business/slots/?date={tomorrow}",
        token=TOKENS["user_a"],
        expected_status=200
    )
    filtered = success and len(data) > 0
    if filtered:
        log_success(f"بازه‌های تاریخ {tomorrow}: {len(data)}")
    results.append(("فیلتر بازه‌ها با تاریخ", filtered))
    wait()
    
    return results

# ==================== بخش ۶: رزرو نوبت (مشتری) ====================

def test_appointments_customer():
    """تست رزرو نوبت توسط مشتری"""
    log_test("بخش ۶: رزرو نوبت (مشتری)")
    
    if not TOKENS.get("user_b") or not DATA.get("business_a") or not DATA.get("slot_a"):
        log_error("داده‌های مورد نیاز موجود نیست!")
        return [("رزرو نوبت (مشتری)", False)]
    
    results = []
    
    # سناریو ۶.۱: مشاهده اطلاعات ارایشگاه با کد
    log_info("سناریو ۶.۱: مشاهده اطلاعات ارایشگاه با کد")
    success, data, status = make_request(
        "GET",
        f"/business/customer/business/{DATA['business_a']['random_code']}/",
        token=TOKENS["user_b"],
        expected_status=200
    )
    has_business_info = success and "business" in data
    if has_business_info:
        log_success(f"نام ارایشگاه: {data['business'].get('name')}")
    results.append(("مشاهده اطلاعات ارایشگاه", has_business_info))
    wait()
    
    # سناریو ۶.۲: رزرو نوبت جدید
    log_info("سناریو ۶.۲: رزرو نوبت جدید")
    appointment_data = {
        "service_id": DATA["service_a"]["id"],
        "time_slot_id": DATA["slot_a"]["id"]
    }
    
    if DATA.get("employee_a"):
        appointment_data["employee_id"] = DATA["employee_a"]["id"]
    
    success, data, status = make_request(
        "POST",
        "/reservations/my-appointments/",
        data=appointment_data,
        token=TOKENS["user_b"],
        expected_status=201
    )
    if success:
        DATA["appointment_a"] = data
        log_success(f"نوبت رزرو شد! ID: {data.get('id')}, وضعیت: {data.get('status')}")
    results.append(("رزرو نوبت جدید", success))
    wait()
    
    # سناریو ۶.۳: لیست نوبت‌های خود
    log_info("سناریو ۶.۳: لیست نوبت‌های خود")
    success, data, status = make_request(
        "GET",
        "/reservations/my-appointments/",
        token=TOKENS["user_b"],
        expected_status=200
    )
    has_appointments = success and len(data) > 0
    if has_appointments:
        log_success(f"تعداد نوبت‌ها: {len(data)}")
    results.append(("لیست نوبت‌های خود", has_appointments))
    wait()
    
    # سناریو ۶.۴: لغو نوبت توسط مشتری
    log_info("سناریو ۶.۴: لغو نوبت توسط مشتری")
    if DATA["appointment_a"]:
        success, data, status = make_request(
            "POST",
            f"/reservations/my-appointments/{DATA['appointment_a']['id']}/cancel/",
            token=TOKENS["user_b"],
            expected_status=200
        )
        results.append(("لغو نوبت توسط مشتری", success))
        wait()
        
        # بعد از لغو، دوباره نوبت بگیریم برای تست‌های بعدی
        log_info("ایجاد نوبت جدید برای تست‌های بعدی...")
        success, data, status = make_request(
            "POST",
            "/reservations/my-appointments/",
            data=appointment_data,
            token=TOKENS["user_b"],
            expected_status=201
        )
        if success:
            DATA["appointment_a"] = data
    else:
        results.append(("لغو نوبت توسط مشتری", False))
    
    return results

# ==================== بخش ۷: مشاهده نوبت‌ها توسط صاحب ارایشگاه ====================

def test_appointments_business():
    """تست مشاهده نوبت‌ها توسط صاحب ارایشگاه"""
    log_test("بخش ۷: مشاهده نوبت‌ها توسط صاحب ارایشگاه")
    
    if not TOKENS.get("user_a") or not DATA.get("appointment_a"):
        log_error("داده‌های مورد نیاز موجود نیست!")
        return [("مشاهده نوبت‌ها (صاحب ارایشگاه)", False)]
    
    results = []
    
    # سناریو ۷.۱: لیست نوبت‌های ارایشگاه
    log_info("سناریو ۷.۱: لیست نوبت‌های ارایشگاه")
    success, data, status = make_request(
        "GET",
        "/reservations/business/appointments/",
        token=TOKENS["user_a"],
        expected_status=200
    )
    has_appointments = success and len(data) > 0
    if has_appointments:
        log_success(f"تعداد نوبت‌های ارایشگاه: {len(data)}")
    results.append(("لیست نوبت‌های ارایشگاه", has_appointments))
    wait()
    
    # سناریو ۷.۲: فیلتر نوبت‌ها با وضعیت
    log_info("سناریو ۷.۲: فیلتر نوبت‌ها با وضعیت")
    success, data, status = make_request(
        "GET",
        "/reservations/business/appointments/?status=confirmed",
        token=TOKENS["user_a"],
        expected_status=200
    )
    filtered = success
    results.append(("فیلتر نوبت‌ها با وضعیت", filtered))
    wait()
    
    # سناریو ۷.۳: تایید نوبت توسط صاحب ارایشگاه
    log_info("سناریو ۷.۳: تایید نوبت توسط صاحب ارایشگاه")
    success, data, status = make_request(
        "PUT",
        f"/reservations/business/appointments/{DATA['appointment_a']['id']}/update/",
        data={"status": "confirmed"},
        token=TOKENS["user_a"],
        expected_status=200
    )
    results.append(("تایید نوبت", success))
    wait()
    
    return results

# ==================== بخش ۸: تست امنیتی ====================

def test_security():
    """تست امنیتی"""
    log_test("بخش ۸: تست امنیتی")
    
    if not TOKENS.get("user_b") or not DATA.get("business_a"):
        log_error("داده‌های مورد نیاز موجود نیست!")
        return [("تست امنیتی", False)]
    
    results = []
    
    # سناریو ۸.۱: دسترسی به ارایشگاه دیگران
    log_info("سناریو ۸.۱: دسترسی به ارایشگاه دیگران")
    success, data, status = make_request(
        "GET",
        f"/business/{DATA['business_a']['id']}/",
        token=TOKENS["user_b"],
        expected_status=403  # یا 404
    )
    # اگه 403 یا 404 برگردونه، موفقیت‌آمیزه
    is_secure = success or status in [403, 404]
    results.append(("دسترسی به ارایشگاه دیگران", is_secure))
    wait()
    
    # سناریو ۸.۲: دسترسی به نوبت‌های دیگران
    log_info("سناریو ۸.۲: دسترسی به نوبت‌های دیگران")
    if DATA.get("appointment_a"):
        success, data, status = make_request(
            "GET",
            f"/reservations/my-appointments/{DATA['appointment_a']['id']}/",
            token=TOKENS["user_a"],  # صاحب ارایشگاه می‌خواد نوبت مشتری رو ببینه
            expected_status=403  # یا 404
        )
        is_secure = success or status in [403, 404]
        results.append(("دسترسی به نوبت‌های دیگران", is_secure))
    else:
        results.append(("دسترسی به نوبت‌های دیگران", False))
    wait()
    
    return results

# ==================== اجرای تست‌ها ====================

def run_all_tests():
    """اجرای همه تست‌ها"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}🚀 شروع تست‌های خودکار نارژین{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.RESET}\n")
    
    all_results = []
    
    # بخش‌های مختلف تست
    tests = [
        ("احراز هویت", test_auth),
        ("مدیریت کسب‌وکار", test_business),
        ("مدیریت کارمندان", test_employees),
        ("مدیریت سرویس‌ها", test_services),
        ("مدیریت بازه‌های زمانی", test_time_slots),
        ("رزرو نوبت (مشتری)", test_appointments_customer),
        ("مشاهده نوبت‌ها (صاحب ارایشگاه)", test_appointments_business),
        ("تست امنیتی", test_security),
    ]
    
    for section_name, test_func in tests:
        try:
            results = test_func()
            all_results.extend(results)
        except Exception as e:
            log_error(f"خطا در بخش {section_name}: {str(e)}")
            all_results.append((f"خطا در {section_name}", False))
    
    # گزارش نهایی
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}📊 گزارش نهایی تست‌ها{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.RESET}\n")
    
    total = len(all_results)
    passed = sum(1 for _, success in all_results if success)
    failed = total - passed
    
    for name, success in all_results:
        status = f"{Colors.GREEN}✓ موفق{Colors.RESET}" if success else f"{Colors.RED}✗ ناموفق{Colors.RESET}"
        print(f"{name}: {status}")
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}جمع کل: {total} تست")
    print(f"{Colors.GREEN}موفق: {passed}{Colors.RESET}")
    print(f"{Colors.RED}ناموفق: {failed}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    # نتیجه نهایی
    if failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 تمام تست‌ها با موفقیت انجام شد!{Colors.RESET}\n")
    else:
        print(f"{Colors.RED}{Colors.BOLD}⚠ {failed} تست ناموفق بود!{Colors.RESET}\n")

if __name__ == "__main__":
    run_all_tests()