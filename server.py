import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import cgi
import io

from agent_core.pipeline import RetailAgentPipeline
from agent_core.llm_client import GeminiAgentLLM

# Initialize global pipeline instance
pipeline = RetailAgentPipeline()
llm_agent = GeminiAgentLLM()

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
UPLOADS_DIR = os.path.join(BASE_DIR, "data", "uploads")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

class RetailAgentHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def _set_json_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/status":
            self._set_json_headers()
            summary = {
                "state": pipeline.state,
                "rules_applied": pipeline.logger.rules_applied,
                "quarantined_count": len(pipeline.state.get("quarantined_records", [])),
                "logs_recent": pipeline.logger.logs[-30:] if pipeline.logger.logs else []
            }
            self.wfile.write(json.dumps(summary, ensure_ascii=False, default=str).encode("utf-8"))
            return

        elif path == "/api/download-report":
            report_path = pipeline.state.get("report_paths", {}).get("excel_path")
            if report_path and os.path.exists(report_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                self.send_header("Content-Disposition", f"attachment; filename=\"{os.path.basename(report_path)}\"")
                self.end_headers()
                with open(report_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, "Chưa có tệp báo cáo Excel nào được xuất.")
                return

        elif path == "/api/download-audit":
            audit_path = pipeline.state.get("report_paths", {}).get("audit_path")
            if audit_path and os.path.exists(audit_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Disposition", f"attachment; filename=\"{os.path.basename(audit_path)}\"")
                self.end_headers()
                with open(audit_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, "Chưa có tệp audit log nào được xuất.")
                return

        # Serve static web files
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))

        if path == "/api/load-sample":
            # Load pre-generated sample data for Phuc An
            global pipeline
            pipeline = RetailAgentPipeline()
            try:
                sample_tx = os.path.join(BASE_DIR, "data", "sample", "transactions.csv")
                sample_ret = os.path.join(BASE_DIR, "data", "sample", "returns.csv")
                sample_prod = os.path.join(BASE_DIR, "data", "sample", "products_cogs.csv")
                sample_stores = os.path.join(BASE_DIR, "data", "sample", "stores_info.csv")
                sample_targets = os.path.join(BASE_DIR, "data", "sample", "stores_targets.csv")

                summary = pipeline.step_1_ingest_data(
                    tx_source=sample_tx,
                    ret_source=sample_ret,
                    prod_source=sample_prod,
                    stores_source=sample_stores,
                    targets_source=sample_targets,
                    period_report="2026-10",
                    period_compare="2026-09"
                )

                # Auto-run AI steps 2 to 4
                auto_res = pipeline.run_automated_steps_2_to_4()

                self._set_json_headers()
                res_body = {
                    "status": "SUCCESS",
                    "message": "Đã nạp bộ dữ liệu mẫu Phúc An (18 cửa hàng, 2 kỳ so sánh) và thực thi AI Agent Bước 2 -> Bước 4 thành công!",
                    "ingest_summary": summary,
                    "auto_res": auto_res,
                    "state": pipeline.state
                }
                self.wfile.write(json.dumps(res_body, ensure_ascii=False, default=str).encode("utf-8"))
            except Exception as e:
                self._set_json_headers(500)
                self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/run-pipeline":
            # Read JSON body for files or Google Sheet links
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}

            tx_src = data.get("transactions_source")
            ret_src = data.get("returns_source")
            prod_src = data.get("products_source")
            stores_src = data.get("stores_source")
            targets_src = data.get("targets_source")
            period_rep = data.get("period_report", "2026-10")
            period_cmp = data.get("period_compare", "2026-09")

            try:
                pipeline.step_1_ingest_data(
                    tx_source=tx_src,
                    ret_source=ret_src,
                    prod_source=prod_src,
                    stores_source=stores_src,
                    targets_source=targets_src,
                    period_report=period_rep,
                    period_compare=period_cmp
                )
                auto_res = pipeline.run_automated_steps_2_to_4()

                self._set_json_headers()
                self.wfile.write(json.dumps({
                    "status": "SUCCESS",
                    "auto_res": auto_res,
                    "state": pipeline.state
                }, ensure_ascii=False, default=str).encode("utf-8"))
            except Exception as e:
                self._set_json_headers(500)
                self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/step-5":
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            is_valid = data.get("is_valid", True)
            feedback = data.get("feedback", "")

            res = pipeline.step_5_human_validation(is_valid, feedback)
            self._set_json_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "result": res, "state": pipeline.state}, ensure_ascii=False, default=str).encode("utf-8"))
            return

        elif path == "/api/step-6":
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            selected_stores = data.get("selected_stores", [])
            director_notes = data.get("director_notes", "")

            res = pipeline.step_6_director_decision(selected_stores, director_notes)
            self._set_json_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "result": res, "state": pipeline.state}, ensure_ascii=False, default=str).encode("utf-8"))
            return

        elif path == "/api/ask-agent":
            # Q&A with Gemini Agent about retail analytics
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            question = data.get("question", "")

            analytics = pipeline.state.get("analytics_result", {})
            chain_kpi = analytics.get("chain_kpi", {})
            priority_stores = analytics.get("top_priority_stores", [])
            categories = analytics.get("category_metrics", [])

            context_prompt = (
                f"Dữ liệu hiệu quả kinh doanh chuỗi 18 cửa hàng Phúc An:\n"
                f"- Doanh thu thuần toàn chuỗi: {chain_kpi.get('total_net_revenue', 0):,} ₫ (Đạt {chain_kpi.get('revenue_completion_pct', 0)}% chỉ tiêu)\n"
                f"- Lợi nhuận gộp toàn chuỗi: {chain_kpi.get('total_gross_profit', 0):,} ₫ (Đạt {chain_kpi.get('profit_completion_pct', 0)}% chỉ tiêu)\n"
                f"- Biên LN gộp TB: {chain_kpi.get('average_margin_pct', 0)}%, Tỷ lệ đổi trả: {chain_kpi.get('chain_return_rate_pct', 0)}%\n"
                f"- Top 3 cửa hàng cần hỗ trợ: " + ", ".join([f"{s.get('store_name')} (Đạt {s.get('target_rev_completion_pct')}% DT, Biên LN {s.get('gross_margin_pct')}%, Đổi trả {s.get('return_rate_pct')}%)" for s in priority_stores]) + "\n"
                f"- Cơ cấu ngành hàng: " + ", ".join([f"{c.get('category')} (Biên LN {c.get('margin_pct')}%, DT {c.get('net_revenue'):,} ₫)" for c in categories]) + "\n\n"
                f"Câu hỏi của người quản lý: {question}\n\n"
                f"Hãy trả lời súc tích, chuyên nghiệp dựa trên đúng số liệu thực tế ở trên."
            )

            system_instruction = (
                "Bạn là Trợ lý AI Phân tích Hiệu quả Kinh doanh Chuỗi Bán lẻ Phúc An. "
                "Chỉ dựa vào các con số thực tế được cung cấp, không suy diễn thiếu căn cứ, không tự tạo giá vốn hay mục tiêu."
            )

            answer = llm_agent.generate_content(context_prompt, system_instruction)
            if not answer:
                answer = "Hệ thống đang hoạt động ở chế độ phân tích quy tắc nội bộ. Vui lòng rà soát bảng chỉ số trên màn hình hoặc kiểm tra kết nối mạng ngoài sandbox."

            self._set_json_headers()
            self.wfile.write(json.dumps({
                "status": "SUCCESS",
                "question": question,
                "answer": answer
            }, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/step-7":
            # Generate Management Report
            try:
                report_summary = pipeline.step_7_generate_management_report(REPORTS_DIR)
                handover = pipeline.step_8_conclude_and_handover()
                self._set_json_headers()
                self.wfile.write(json.dumps({
                    "status": "SUCCESS",
                    "report_summary": report_summary,
                    "handover": handover,
                    "state": pipeline.state
                }, ensure_ascii=False, default=str).encode("utf-8"))
            except Exception as e:
                self._set_json_headers(500)
                self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/upload":
            # Multipart file upload handler
            try:
                content_type = self.headers.get("Content-Type")
                if not content_type or not content_type.startswith("multipart/form-data"):
                    self._set_json_headers(400)
                    self.wfile.write(b'{"status":"ERROR","message":"Invalid Content-Type"}')
                    return

                # Parse multipart
                environ = {'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': content_type}
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ=environ)

                saved_files = {}
                for key in ["transactions_file", "returns_file", "products_file", "stores_file", "targets_file"]:
                    if key in form and form[key].file and form[key].filename:
                        item = form[key]
                        safe_name = os.path.basename(item.filename)
                        dest_path = os.path.join(UPLOADS_DIR, safe_name)
                        with open(dest_path, "wb") as f_out:
                            f_out.write(item.file.read())
                        saved_files[key] = dest_path

                self._set_json_headers()
                self.wfile.write(json.dumps({"status": "SUCCESS", "saved_files": saved_files}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self._set_json_headers(500)
                self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}, ensure_ascii=False).encode("utf-8"))
            return

        else:
            self.send_error(404, "Endpoint not found")

def run(port=PORT):
    server_address = ("", port)
    httpd = HTTPServer(server_address, RetailAgentHandler)
    print(f"================================================================")
    print(f"  PHÚC AN RETAIL CHAIN - AI AGENT BUSINESS ANALYTICS SYSTEM")
    print(f"  Hệ thống đang chạy tại: http://localhost:{port}")
    print(f"================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()

if __name__ == "__main__":
    port_to_use = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run(port_to_use)

