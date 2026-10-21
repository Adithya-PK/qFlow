import re

report_path = r"c:\Projects\QFlow\scripts\build_full_report_docx.py"
with open(report_path, "r", encoding="utf-8") as f:
    text = f.read()

# Update TOC
new_toc = '''    toc_data = [
        ("", "ABSTRACT", "iv"),
        ("", "ACKNOWLEDGEMENT", "v"),
        ("", "LIST OF TABLES", "viii"),
        ("", "LIST OF FIGURES", "ix"),
        ("1", "INTRODUCTION", "1"),
        ("", "1.1 OVERVIEW", "1"),
        ("", "1.1.1 Need for a Centralized Queue and Token Management System", "1"),
        ("", "1.1.2 Limitations of Existing Manual and Physical Token Systems", "1"),
        ("", "1.2 OBJECTIVE", "2"),
        ("", "1.3 SCOPE OF THE PROJECT", "3"),
        ("", "1.4 MOTIVATION", "4"),
        ("", "1.5 ORGANIZATION OF THE REPORT", "4"),
        ("2", "RELATED WORK", "6"),
        ("", "2.1 LITERATURE REVIEW", "6"),
        ("", "2.2 EXISTING SYSTEMS", "7"),
        ("", "2.3 INFERENCE FROM LITERATURE REVIEW", "8"),
        ("", "2.4 EXTRACTION FROM LITERATURE REVIEW", "9"),
        ("3", "SYSTEM ANALYSIS", "10"),
        ("", "3.1 PROBLEM DEFINITION", "10"),
        ("", "3.2 PROPOSED SOLUTION", "10"),
        ("", "3.2.1 Functional Requirements", "11"),
        ("", "3.2.2 Non-Functional Requirements", "12"),
        ("", "3.3 SOFTWARE COMPONENTS", "13"),
        ("", "3.4 HARDWARE COMPONENTS", "14"),
        ("", "3.5 USE CASES", "14"),
        ("4", "IMPLEMENTATION", "17"),
        ("", "4.1 SYSTEM ARCHITECTURE AND EXPERIMENTAL SETUP", "17"),
        ("", "4.1.1 High-Level System Architecture", "17"),
        ("", "4.1.2 System Deployment and Network Topology", "19"),
        ("", "4.2 MODULE IMPLEMENTATION DETAILS", "21"),
        ("", "4.2.1 Data Source Module", "21"),
        ("", "4.2.2 Steps of Algorithm", "22"),
        ("", "4.2.3 Data Processing Module", "23"),
        ("", "4.2.4 Explainability Module", "24"),
        ("", "4.2.5 Visualization and Dashboard Module", "24"),
        ("", "4.3 CLASS DIAGRAM / DATA MODEL", "24"),
        ("", "4.4 SEQUENCE DIAGRAM", "25"),
        ("", "4.5 TESTING AND RESULTS", "26"),
        ("5", "CONCLUSION AND FUTURE ENHANCEMENTS", "29"),
        ("", "5.1 CONCLUSION", "29"),
        ("", "5.2 FUTURE ENHANCEMENTS", "30"),
        ("", "APPENDIX 1: SAMPLE CODE", "31"),
        ("", "1. Project Directory Structure", "31"),
        ("", "2. Installation and Execution Commands", "31"),
        ("", "3. Server Environment Configuration", "31"),
        ("", "4. Database Models and Schema Architecture", "32"),
        ("", "5. Main Server Entry Point and WebSocket Setup", "34"),
        ("", "6. Token Controller and Atomic Number Generation", "35"),
        ("", "7. Authentication Controller and JWT Middleware", "36"),
        ("", "8. AI Prediction Engine and Duration Calculation", "37"),
        ("", "9. Dynamic Counter Recommendation Scoring", "38"),
        ("", "10. Socket.IO Real-Time Multiplexing and Broadcasts", "39"),
        ("", "PROJECT SCREENSHOTS", "39"),
        ("", "REFERENCES", "50")
    ]'''

# Update LOT
new_lot = '''    tables_list = [
        ("2.1", "Comparison of Existing Approaches to Queue and Token Management", "7"),
        ("2.2", "Design Principles Extracted from Literature and Their Use in QFlow", "8"),
        ("3.1", "Functional Requirements of QFlow", "10"),
        ("3.2", "Software Components of QFlow", "12"),
        ("3.3", "Hardware Components for Development and Deployment", "13"),
        ("3.4", "Description of Main Use Cases", "14"),
        ("4.1", "REST API Endpoints of QFlow", "17"),
        ("4.2", "Experimental Setup Used for Building and Testing", "19"),
        ("4.3", "Summary of QFlow Modules", "20"),
        ("4.4", "Service Catalog and Base Parameters Accepted by the Data Source Module", "20"),
        ("4.5", "MongoDB Collections Used by QFlow", "23"),
        ("4.6", "Functional Test Cases and Results", "25"),
        ("4.7", "Technical Observations and Edge Cases Observed During Testing", "26")
    ]'''

# Update LOF
new_lof = '''    figures_list = [
        ("3.1", "Use Case Diagram of QFlow", "15"),
        ("4.1", "System Architecture of QFlow", "16"),
        ("4.2", "System Deployment and Network Topology of QFlow", "19"),
        ("4.3", "Class Diagram / Entity-Relationship Schema of the QFlow Data Model", "24"),
        ("A.1", "Staff and Administrative Authentication Portal", "39"),
        ("A.2", "Live Staff Operations Dashboard with Active Counters", "39"),
        ("A.3", "Customer QR Code Registration Poster and Modal", "40"),
        ("A.4", "Mobile Customer Portal - Welcome and Value Proposition", "41"),
        ("A.5", "Mobile Customer Registration Form with Service Selection", "42"),
        ("A.6", "Mobile Service Catalogue Modal Dialog", "43"),
        ("A.7", "Live Mobile Customer Ticket - Waiting Status with AI Estimation", "44"),
        ("A.8", "Real-Time Mobile Haptic & Visual Turn Alert Screen", "45"),
        ("A.9", "Active Mobile Consultation In-Service Status Monitor", "46"),
        ("A.10", "Service Completion Confirmation Screen", "47"),
        ("A.11", "Counter Management and Dynamic Fleet Allocation Workspace", "47"),
        ("A.12", "Real-Time Queue Inspection and Live Token Roster", "48"),
        ("A.13", "Executive Operational Analytics Dashboard with Traffic Distributions", "48"),
        ("A.14", "Active Counter Workspace Telemetry Detail Cards", "48")
    ]'''

toc_pattern = re.compile(r'    toc_data = \[.*?\]', re.DOTALL)
lot_pattern = re.compile(r'    tables_list = \[.*?\]', re.DOTALL)
lof_pattern = re.compile(r'    figures_list = \[.*?\]', re.DOTALL)

text = toc_pattern.sub(new_toc.strip(), text)
text = lot_pattern.sub(new_lot.strip(), text)
text = lof_pattern.sub(new_lof.strip(), text)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(text)

print("TOC, LOT, LOF page numbers updated successfully!")
