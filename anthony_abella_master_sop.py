from fpdf import FPDF

class ProxyManual(FPDF):
    def header(self):
        # Professional Header with Logo and Title
        self.set_font("helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, "Anthony Abella | T2 Support Operations", align="R")
        try:
            # Using your specific Arch Linux path
            self.image("/home/spongebob/Pictures/logo5.png", 10, 8, 40)
        except:
            pass
        self.ln(20)
        self.set_draw_color(0, 102, 204) # Proxy-Cheap Blue
        self.line(10, 25, 200, 25)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "Prepared for Proxy-Cheap / Internal teams reference", align="L")
        self.cell(0, 10, f"Page {self.page_no()}", align="R")

def create_manual():
    pdf = ProxyManual()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- TITLE ---
    pdf.set_font("helvetica", "B", 22)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, "The 360 Degree Proxy & Infrastructure Protocol", ln=True, align="C")
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(0, 5, "Comprehensive Tier 2 Diagnostic Standard Operating Procedure", ln=True, align="C")
    pdf.ln(10)

    # --- 1. QUICK REFERENCE MAPPING ---
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "1.0 | Quick Complaint Mapping", ln=True)
    pdf.set_font("helvetica", "B", 9)
    pdf.set_fill_color(220, 235, 255)
    
    mapping = [
        ("Auth/Login Fail", "Credentials/ACL", "curl -v (Check 407/403)"),
        ("Slow Connection", "Noisy Neighbor", "curl -w (Measure TTFB)"),
        ("Buffering Issues", "Range Throttling", "curl -H 'Range: bytes...'"),
        ("Access Denied", "Target WAF/Fingerprint", "curl -v -L (Check Ref ID)"),
        ("Dropped Packets", "ISP/Carrier Issue", "mtr -rw (Trace Hops)"),
        ("Site Down (502)", "Node Offline", "nc -zv [IP] [Port]"),
        ("Geo-Location Fail", "IP Mismatch", "curl (Check icanhazip.com)")
    ]
    for comp, hyp, tool in mapping:
        pdf.cell(45, 8, comp, border=1)
        pdf.cell(45, 8, hyp, border=1)
        pdf.cell(100, 8, tool, border=1, ln=True)
    pdf.ln(10)

    # --- 2. CORE DIAGNOSTIC SUITE (CUMULATIVE) ---
    sections = [
        ("2.1 | Connectivity Isolation (The Heartbeat)", 
         "Standard verification of gateway health and authentication. SOCKS5 bypasses the HTTP logic to isolate the protocol.",
         "curl -v -x http://U:P@IP:PORT https://icanhazip.com\ncurl -v -x socks5://U:P@IP:PORT https://icanhazip.com",
         "200 OK: Healthy. 407: Auth Error. 502: Gateway Down."),

        ("2.2 | Layer 7 WAF Detective Work (The 403 Solution)", 
         "Essential for 'Access Denied' errors. Determines if a target (e.g., Papa Johns, Nike) is blocking the bot fingerprint.",
         "curl -v -L -x http://U:P@IP:PORT -H \"User-Agent: Chrome/122.0\" \"https://site.com\"",
         "Search for 'Edgesuite' or 'Ray ID'. If found, the proxy is delivering data, but the WAF is blocking the client."),

        ("2.3 | Infrastructure: Noisy Neighbors & Vendor Caps", 
         "Identifies if server CPU is locked (Wait Time) or if the ISP is throttling throughput.",
         "curl -o /dev/null -s -w \"TTFB: %{time_starttransfer}s\" -x [Proxy] [URL]\ncurl --limit-rate 500k -o /dev/null [Target_File]",
         "TTFB > 2s = Server Overload. Flatline speed = ISP Bandwidth Cap."),

        ("2.4 | Global Compliance & Platform Health", 
         "Checks if the residential node is flagged for high-security targets.",
         "curl -I -x [Proxy] https://www.binance.com\ncurl -I -x [Proxy] https://www.paypal.com\ncurl -I -x [Proxy] https://www.instagram.com",
         "A 403 here usually indicates the IP is 'Dirty' or flagged for that specific exchange/platform."),

        ("2.5 | Advanced Network Toolkit (Non-Curl)", 
         "Layer 3 and Layer 4 diagnostics for routing and DNS stability.",
         "mtr -rw [Proxy_IP]\nnc -zv [Proxy_IP] [Port]\ndig @8.8.8.8 [Target_Host]",
         "Use MTR for latency/drops. Use NC to check for ISP-level port blocking.")
    ]

    for title, desc, cmd, diag in sections:
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 10, title, fill=True, ln=True)
        pdf.set_font("helvetica", "", 10); pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, desc)
        pdf.set_fill_color(30, 30, 30); pdf.set_text_color(255, 255, 255)
        pdf.set_font("courier", "B", 9); pdf.multi_cell(0, 7, f"\n {cmd} \n", fill=True)
        pdf.ln(1); pdf.set_font("helvetica", "I", 9); pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 5, f"Analysis: {diag}"); pdf.ln(8)

    # --- 3. NOC ENGINEER'S CHEAT SHEET ---
    pdf.add_page()
    pdf.set_font("helvetica", "B", 14); pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "3.0 | The NOC Engineer's Cheat Sheet (Log Logic)", ln=True)
    pdf.set_font("helvetica", "", 10); pdf.set_text_color(0,0,0)
    
    codes = [
        ("TCP_DENIED / 403", "Local Squid ACL Rule", "The proxy itself is blocking. Check internal blacklists."),
        ("TCP_MISS / 403", "Target-Side WAF Block", "Target (Akamai/CF) is blocking the client fingerprint."),
        ("502 Bad Gateway", "Node / Exit Point Offline", "The end-point IP has lost connectivity."),
        ("504 Timeout", "Infrastructure Congestion", "Noisy neighbor or server-side CPU lockup."),
        ("Empty Reply", "ISP Port Block / DPI", "Carrier is dropping traffic via Deep Packet Inspection.")
    ]
    for code, cause, action in codes:
        pdf.set_font("helvetica", "B", 10); pdf.cell(0, 6, code, ln=True)
        pdf.set_font("helvetica", "", 10); pdf.multi_cell(0, 5, f"Cause: {cause} | Action: {action}")
        pdf.ln(3)

    pdf.output("Master_Diagnostic_Protocol_Abella.pdf")
    print("\n[SUCCESS] Consolidated 4-page SOP generated: Master_Diagnostic_Protocol_Abella.pdf")

if __name__ == "__main__":
    create_manual()
