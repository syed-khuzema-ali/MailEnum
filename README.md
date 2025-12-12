# MailEnum
MailEnum is a Python‑based email enumeration utility designed strictly for educational and authorized security research. It is intended for ethical hacking practice in controlled and legally permitted environments only.
<!-- PROJECT HEADER -->
<h1 align="center">📧 MailEnum – Email Enumeration Tool</h1>

<p align="center">
  A Python-based educational utility for understanding email enumeration techniques in authorized and controlled environments.
</p>

---

## 📘 Overview
MailEnum is a lightweight, Python-powered tool created for **educational cybersecurity training** and **authorized security research**. It offers a structured way to study how email enumeration works, emphasizing responsible and permission-based testing practices.

---

## ⚠️ Legal Disclaimer

### **Important Notice**
MailEnum is intended strictly for:

- Educational learning  
- Ethical hacking training  
- Security testing with **explicit written authorization**

You may use this tool **only** on:

- Systems you personally own  
- Systems where you have verified written permission  
- Controlled lab or testing environments  

Unauthorized use is prohibited. The author, **Syed Khuzema Ali**, does not endorse or support illegal activity. Users are fully responsible for complying with all relevant laws and regulations.

---

## 🛠️ Tool Information

| Field     | Value                                   |
|-----------|------------------------------------------|
| **Name**  | MailEnum – Email Enumeration Tool        |
| **Author**| Syed Khuzema Ali                         |
| **Version** | 1.0                                    |
| **Language** | Python 2.7                            |
| **License** | Educational Use Only                   |
| **Purpose** | Security Research & Ethical Training   |

---

## ✨ Features

- Uses only built-in Python modules (no external dependencies)  
- Multi-threaded crawling for improved speed  
- Smart same-domain URL discovery  
- Supports **TXT** and **JSON** result formats  
- Request delay configuration  
- Quick Scan mode  
- Color-coded terminal output  
- Built-in help documentation  

---

## 📥 Installation

### Clone the repository
```git clone https://github.com/syed-khuzema-ali/MailEnum```

### Move into the directory
```cd mailenum```

### Make executable (Linux/macOS)
```chmod +x mailenum.py```
🚀 Usage
📄 Show Help
```python mailenum.py -h```

## 🔍 Basic Scan
```python mailenum.py -u https://target-website.com```

## ⚙️ Advanced Usage
Run with 20 Threads + Output to File
```python mailenum.py -u https://example.com -t 20 -o results.txt```

Quick Scan + JSON Output
```python mailenum.py -u https://example.com -q -o emails.json```

Add Delay Between Requests
```python mailenum.py -u https://example.com -d 0.5 -t 5```

## 👤 Author

Syed Khuzema Ali
Educational Cybersecurity Research

## ⭐ Contribution & Feedback

This project is for learning and responsible research. Feel free to suggest improvements or enhancements.
