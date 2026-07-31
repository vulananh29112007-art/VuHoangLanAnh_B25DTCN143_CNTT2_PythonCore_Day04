# Dataset raw_registers & orders:
raw_registers = [
    {"name": "  Nguyen Van An  ", "email": "an.nguyen@gmail.com", "phone": "0987654321"},
    {"name": "Tran Thi Bich", "email": "bich_gmail.com", "phone": "0912345678"},
    {"name": "Le Hoang Cuong", "email": "cuong@rikkei.edu.vn", "phone": "0123456789"},
    {"name": "  Pham Minh Dung ", "email": "dung@gmail.com  ", "phone": "0355667788"}
]

orders = [
    {"id": "DH01", "total": "12500000", "discount_code": "VIP10", "is_vip": True},
    {"id": "DH02", "total": "450000", "discount_code": "INVALID", "is_vip": False},
    {"id": "DH03", "total": "ABC_ERROR", "discount_code": "", "is_vip": False},
    {"id": "DH04", "total": "8500000", "discount_code": "VIP20", "is_vip": True}
]


# bai1
def validate_registration_input(name, email, phone):
    result_email = None
    result_phone = None
    name_clean = name.strip()
    email_clean = email.strip().lower()
    phone_clean = phone.strip()
    def_phone = ("03", "05", "07", "08", "09")

    if "@" not in email_clean:
        result_email =  "Trạng thái: KHÔNG HỢP LỆ (Thiếu '@')"

    if not (email_clean.endswith(".com") or email_clean.endswith(".edu.vn")):
        result_email = "Trạng thái: KHÔNG HỢP LỆ (Sai đuôi)"

    if len(phone_clean) != 10 or not phone_clean.startswith(def_phone):
        result_phone = "Trạng thái: KHÔNG HỢP LỆ (Sai đầu số VN/ Sai độ dài)"

    return name_clean,email_clean, phone_clean, result_email, result_phone

print("BÁO CÁO CHUẨN HÓA & VALIDATE THÔNG TIN ĐĂNG KÝ")
for i in range(len(raw_registers)):
    name, email, phone, email_status, phone_status = validate_registration_input(raw_registers[i]["name"], raw_registers[i]["email"], raw_registers[i]["phone"])
    print(f"""[{i+1}] {name} | Email: {email} | SDT: {phone} -> {email_status or phone_status or "TRẠNG THÁI: HỢP LỆ"} """)


# bai2
def safe_process_invoice(order_id, raw_total, discount_code, is_vip):
    try:
        total = float(raw_total)
        discount = 0
        # Trong try: Ép kiểu float(raw_total), tính chiết khấu VIP (VIP10 giảm 10%, VIP20 giảm 20%), cộng thuế VAT 10%, phân loại đơn hàng.
        if is_vip:
            if discount_code == "VIP10":
                discount = total * 0.1
            elif discount_code == "VIP20":
                discount = total * 0.2

        after_discount = total - discount
        vat = after_discount * 0.1
        final = after_discount + vat

        tier = "HÓA ĐƠN LỚN (VIP)" if final >= 10000000 else "HÓA ĐƠN THƯỜNG"
        return total, discount, vat, final, tier

    except ValueError:
        print(f"Xử lý lỗi [{order_id}]: Số tiền '{raw_total}' không hợp lệ! Bỏ qua đơn hàng.")
        return None

print("\nBÁO CÁO XỬ LÝ HÓA ĐƠN AN TOÀN (TRY-EXCEPT & VAT)")

for order in orders:
    result = safe_process_invoice(order["id"], order["total"], order["discount_code"], order["is_vip"])

    if result is not None:
        total, discount, vat, final, tier = result

        print(f"""[{order['id']}] Tiền hàng: {total} | CK ({order['discount_code']}): {discount} | VAT 10%: {vat} -> Tổng: {final} VNĐ [{tier}]""")
