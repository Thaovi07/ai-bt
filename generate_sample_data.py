import os
import random
import datetime
import pandas as pd
import numpy as np

def generate_phuc_an_data(output_dir: str = "data/sample"):
    os.makedirs(output_dir, exist_ok=True)
    random.seed(42)
    np.random.seed(42)

    # 1. Danh sách 18 Cửa hàng
    stores = [
        {"store_id": "PA_HN01", "store_name": "Phúc An Hoàn Kiếm", "region": "Miền Bắc"},
        {"store_id": "PA_HN02", "store_name": "Phúc An Cầu Giấy", "region": "Miền Bắc"},
        {"store_id": "PA_HN03", "store_name": "Phúc An Đống Đa", "region": "Miền Bắc"},
        {"store_id": "PA_HN04", "store_name": "Phúc An Hai Bà Trưng", "region": "Miền Bắc"},
        {"store_id": "PA_HN05", "store_name": "Phúc An Hà Đông", "region": "Miền Bắc"},
        {"store_id": "PA_HP01", "store_name": "Phúc An Hải Phòng", "region": "Miền Bắc"},
        {"store_id": "PA_DN01", "store_name": "Phúc An Hải Châu (Đà Nẵng)", "region": "Miền Trung"},
        {"store_id": "PA_DN02", "store_name": "Phúc An Thanh Khê (Đà Nẵng)", "region": "Miền Trung"},
        {"store_id": "PA_HUE01", "store_name": "Phúc An TP Huế", "region": "Miền Trung"},
        {"store_id": "PA_NT01", "store_name": "Phúc An Nha Trang", "region": "Miền Trung"},
        {"store_id": "PA_HCM01", "store_name": "Phúc An Quận 1", "region": "Miền Nam"},
        {"store_id": "PA_HCM02", "store_name": "Phúc An Quận 3", "region": "Miền Nam"},
        {"store_id": "PA_HCM03", "store_name": "Phúc An Bình Thạnh", "region": "Miền Nam"},
        {"store_id": "PA_HCM04", "store_name": "Phúc An Tân Bình", "region": "Miền Nam"},
        {"store_id": "PA_HCM05", "store_name": "Phúc An Gò Vấp", "region": "Miền Nam"},
        {"store_id": "PA_HCM06", "store_name": "Phúc An Quận 7", "region": "Miền Nam"},
        {"store_id": "PA_BD01", "store_name": "Phúc An Thủ Dầu Một", "region": "Miền Nam"},
        {"store_id": "PA_CT01", "store_name": "Phúc An Ninh Kiều (Cần Thơ)", "region": "Miền Nam"},
    ]
    df_stores = pd.DataFrame(stores)
    df_stores.to_csv(os.path.join(output_dir, "stores_info.csv"), index=False, encoding="utf-8-sig")

    # 2. Danh mục sản phẩm & Giá vốn (Products & COGS)
    categories = {
        "Điện gia dụng": [
            ("SP_DGD_01", "Nồi chiên không dầu Lock&Lock 5.2L", 2190000, 1420000),
            ("SP_DGD_02", "Nồi cơm điện tử Philips 1.8L", 1450000, 950000),
            ("SP_DGD_03", "Máy xay sinh tố đa năng Sunhouse", 680000, 420000),
            ("SP_DGD_04", "Bàn ủi hơi nước cầm tay Tefal", 890000, 560000),
            ("SP_DGD_05", "Máy lọc không khí Xiaomi 4 Compact", 2490000, 1750000),
        ],
        "Thời trang & Phụ kiện": [
            ("SP_TT_01", "Áo sơ mi Oxford nam Phúc An Premium", 450000, 220000),
            ("SP_TT_02", "Quần âu Slimfit co giãn cao cấp", 580000, 290000),
            ("SP_TT_03", "Đầm công sở nữ thiết kế", 720000, 340000),
            ("SP_TT_04", "Áo khoác gió trượt nước", 520000, 250000),
            ("SP_TT_05", "Thắt lưng da bò tự nhiên", 390000, 160000),
        ],
        "Hóa mỹ phẩm & Chăm sóc cá nhân": [
            ("SP_MP_01", "Sữa rửa mặt Cetaphil dịu lành 500ml", 360000, 240000),
            ("SP_MP_02", "Kem chống nắng La Roche-Posay Anthelios", 495000, 320000),
            ("SP_MP_03", "Dầu gội bưởi ngăn rụng tóc Cocoon 500ml", 285000, 170000),
            ("SP_MP_04", "Nước tẩy trang Bioderma hồng 500ml", 420000, 280000),
            ("SP_MP_05", "Serum dưỡng ẩm phục hồi B5 La Roche-Posay", 790000, 510000),
        ],
        "Thiết bị số & Phụ kiện": [
            ("SP_TB_01", "Tai nghe không dây chống ồn Baseus Bowie", 750000, 430000),
            ("SP_TB_02", "Sạc dự phòng Anker 20.000mAh 20W", 690000, 420000),
            ("SP_TB_03", "Cáp sạc nhanh Type-C to Lightning Ugreen", 180000, 90000),
            ("SP_TB_04", "Loa Bluetooth di động Marshall Willen", 2650000, 1850000),
            ("SP_TB_05", "Bàn phím cơ không dây RK Royal Kludge", 950000, 580000),
        ],
        "Tiêu dùng & Thực phẩm đóng gói": [
            ("SP_TD_01", "Cà phê sấy lạnh Phúc An Signature 200g", 195000, 110000),
            ("SP_TD_02", "Hạt dinh dưỡng Granola mật ong 500g", 165000, 90000),
            ("SP_TD_03", "Trà ô long thượng hạng 150g", 240000, 130000),
            ("SP_TD_04", "Bánh quy bơ hộp thiếc nhập khẩu", 185000, 105000),
            ("SP_TD_05", "Mật ong hoa rừng nguyên chất 500ml", 220000, 120000),
        ]
    }

    products_list = []
    for cat, items in categories.items():
        for sku, name, price, cogs in items:
            products_list.append({
                "sku": sku,
                "product_name": name,
                "category": cat,
                "unit_price": price,
                "cogs": cogs
            })
    df_products = pd.DataFrame(products_list)
    df_products.to_csv(os.path.join(output_dir, "products_cogs.csv"), index=False, encoding="utf-8-sig")

    # 3. Mục tiêu kinh doanh theo kỳ (Targets)
    # Kỳ so sánh: 2026-09 | Kỳ báo cáo: 2026-10
    targets = []
    for s in stores:
        sid = s["store_id"]
        # Phân tầng quy mô cửa hàng
        base_rev = 800000000 if "HCM" in sid or "HN01" in sid or "HN02" in sid else 500000000
        
        # Tháng 9
        target_rev_sep = base_rev + random.randint(-50000000, 50000000)
        target_gp_sep = int(target_rev_sep * 0.38)
        targets.append({
            "store_id": sid,
            "period": "2026-09",
            "target_revenue": target_rev_sep,
            "target_profit": target_gp_sep
        })
        # Tháng 10 (tăng nhẹ kỳ vọng)
        target_rev_oct = int(target_rev_sep * 1.05)
        target_gp_oct = int(target_rev_oct * 0.38)
        targets.append({
            "store_id": sid,
            "period": "2026-10",
            "target_revenue": target_rev_oct,
            "target_profit": target_gp_oct
        })

    df_targets = pd.DataFrame(targets)
    df_targets.to_csv(os.path.join(output_dir, "stores_targets.csv"), index=False, encoding="utf-8-sig")

    # 4. Sinh Giao Dịch Bán Hàng (Transactions) - ~25,000 dòng chia 2 tháng
    transactions = []
    order_seq = 100000

    # Thiết kế có chủ đích cho 3 cửa hàng gặp khó khăn (đáp ứng Task 1 & Task 2):
    # 1. PA_HN05 (Hà Đông): Doanh thu thấp, đạt ~62% kế hoạch, suy giảm mạnh MoM
    # 2. PA_NT01 (Nha Trang): Tỷ lệ trả hàng rất cao (>8.5%) do sản phẩm thời trang/điện gia dụng bị lỗi
    # 3. PA_HCM05 (Gò Vấp): Doanh thu đạt khá nhưng biên lợi nhuận mỏng (chỉ 22%) do bán lệch nhóm hàng khuyến mãi biên thấp
    
    dates_sep = pd.date_range(start="2026-09-01", end="2026-09-30", freq="h")
    dates_oct = pd.date_range(start="2026-10-01", end="2026-10-31", freq="h")

    all_skus = [p["sku"] for p in products_list]
    sku_price_map = {p["sku"]: p["unit_price"] for p in products_list}

    # Generate transactions for September
    for _ in range(12000):
        order_seq += 1
        tx_id = f"TX-202609-{order_seq}"
        sid = random.choice(stores)["store_id"]
        sku = random.choice(all_skus)
        qty = random.choices([1, 2, 3, 4, 5], weights=[65, 20, 10, 3, 2])[0]
        price = sku_price_map[sku]
        amount = qty * price
        dt = random.choice(dates_sep)
        status = "COMPLETED"

        transactions.append({
            "transaction_id": tx_id,
            "date": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "store_id": sid,
            "sku": sku,
            "quantity": qty,
            "unit_price": price,
            "total_amount": amount,
            "status": status
        })

    # Generate transactions for October
    for _ in range(14000):
        order_seq += 1
        tx_id = f"TX-202610-{order_seq}"
        sid = random.choice(stores)["store_id"]

        # Điều chỉnh sản lượng cho cửa hàng đặc thù
        if sid == "PA_HN05" and random.random() < 0.45:
            continue # giảm số đơn đáng kể cho PA_HN05
        
        if sid == "PA_HCM05":
            # Thiên về nhóm Tiêu dùng đóng gói biên mỏng
            sku = random.choice(["SP_TD_01", "SP_TD_02", "SP_TD_03", "SP_TD_04", "SP_TD_05", "SP_TB_03"])
        else:
            sku = random.choice(all_skus)

        qty = random.choices([1, 2, 3, 4, 5], weights=[65, 20, 10, 3, 2])[0]
        price = sku_price_map[sku]
        amount = qty * price
        dt = random.choice(dates_oct)
        status = "COMPLETED"

        transactions.append({
            "transaction_id": tx_id,
            "date": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "store_id": sid,
            "sku": sku,
            "quantity": qty,
            "unit_price": price,
            "total_amount": amount,
            "status": status
        })

    # Cài đặt các trường hợp thử nghiệm (Test Edge Cases):
    # 1. Trùng lặp mã giao dịch (Exact duplicates): 45 đơn
    for i in range(45):
        dup_row = transactions[i * 20].copy()
        transactions.append(dup_row)

    # 2. Đơn hàng bị HỦY (Cancelled): 85 đơn
    for i in range(85):
        order_seq += 1
        sid = random.choice(stores)["store_id"]
        sku = random.choice(all_skus)
        price = sku_price_map[sku]
        transactions.append({
            "transaction_id": f"TX-CANCEL-{order_seq}",
            "date": random.choice(dates_oct).strftime("%Y-%m-%d %H:%M:%S"),
            "store_id": sid,
            "sku": sku,
            "quantity": 1,
            "unit_price": price,
            "total_amount": price,
            "status": "CANCELLED"
        })

    # 3. Mã cửa hàng không hợp lệ: 12 đơn
    for i in range(12):
        order_seq += 1
        sku = random.choice(all_skus)
        price = sku_price_map[sku]
        transactions.append({
            "transaction_id": f"TX-ERRSTORE-{order_seq}",
            "date": random.choice(dates_oct).strftime("%Y-%m-%d %H:%M:%S"),
            "store_id": "PA_UNKNOWN99",
            "sku": sku,
            "quantity": 2,
            "unit_price": price,
            "total_amount": price * 2,
            "status": "COMPLETED"
        })

    # 4. SKU không tồn tại trong danh mục giá vốn: 18 đơn
    for i in range(18):
        order_seq += 1
        sid = random.choice(stores)["store_id"]
        transactions.append({
            "transaction_id": f"TX-ERRSKU-{order_seq}",
            "date": random.choice(dates_oct).strftime("%Y-%m-%d %H:%M:%S"),
            "store_id": sid,
            "sku": "SP_KHONG_RO_NGUON_GOC",
            "quantity": 1,
            "unit_price": 500000,
            "total_amount": 500000,
            "status": "COMPLETED"
        })

    df_tx = pd.DataFrame(transactions)
    df_tx.to_csv(os.path.join(output_dir, "transactions.csv"), index=False, encoding="utf-8-sig")

    # 5. Sinh Dữ liệu Đổi trả (Returns)
    returns = []
    ret_seq = 5000

    # Lấy các giao dịch hoàn thành để làm căn cứ trả hàng
    completed_tx = [t for t in transactions if t["status"] == "COMPLETED" and "UNKNOWN" not in t["store_id"] and "ERR" not in t["sku"]]

    for t in completed_tx:
        sid = t["store_id"]
        # Tỷ lệ trả hàng cao hơn ở PA_NT01 (Nha Trang)
        ret_prob = 0.085 if sid == "PA_NT01" else 0.022
        if random.random() < ret_prob:
            ret_seq += 1
            # Ngày trả sau ngày mua từ 1 đến 5 ngày
            tx_dt = datetime.datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S")
            ret_dt = tx_dt + datetime.timedelta(days=random.randint(1, 5))
            
            ret_qty = random.randint(1, t["quantity"])
            refund = ret_qty * t["unit_price"]

            returns.append({
                "return_id": f"RET-{ret_seq}",
                "original_order_id": t["transaction_id"],
                "store_id": sid,
                "sku": t["sku"],
                "date": ret_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "quantity_returned": ret_qty,
                "refund_amount": refund
            })

    # Cài đặt Edge cases cho đổi trả:
    # 1. Trả hàng không có mã hóa đơn gốc: 15 đơn
    for i in range(15):
        ret_seq += 1
        returns.append({
            "return_id": f"RET-NO-ORIG-{ret_seq}",
            "original_order_id": f"TX-NON-EXISTENT-{ret_seq}",
            "store_id": "PA_HN01",
            "sku": "SP_DGD_01",
            "date": "2026-10-15 14:00:00",
            "quantity_returned": 1,
            "refund_amount": 2190000
        })

    # 2. Số lượng trả vượt quá số lượng mua: 8 đơn
    target_sample = completed_tx[0]
    for i in range(8):
        ret_seq += 1
        returns.append({
            "return_id": f"RET-OVERQTY-{ret_seq}",
            "original_order_id": target_sample["transaction_id"],
            "store_id": target_sample["store_id"],
            "sku": target_sample["sku"],
            "date": "2026-10-20 10:00:00",
            "quantity_returned": 999, # Vượt quá số lượng mua
            "refund_amount": 999 * target_sample["unit_price"]
        })

    df_ret = pd.DataFrame(returns)
    df_ret.to_csv(os.path.join(output_dir, "returns.csv"), index=False, encoding="utf-8-sig")

    print(f"Generated sample datasets successfully:")
    print(f"- Stores: {len(df_stores)}")
    print(f"- Products: {len(df_products)}")
    print(f"- Targets: {len(df_targets)}")
    print(f"- Transactions: {len(df_tx)}")
    print(f"- Returns: {len(df_ret)}")

if __name__ == "__main__":
    generate_phuc_an_data()
