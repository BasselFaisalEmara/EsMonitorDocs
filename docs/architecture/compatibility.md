# OS Compatibility Matrix

The eSolutions Monitoring Platform is built with Python and packaged as standalone executables.

> This page documents **verified** and **planned** platform support. Items marked ✅ are tested; items marked 🔴 are planned.

---

## Monitoring Core

| Operating System | Version | Status | Packaging | Notes |
| :--- | :--- | :---: | :--- | :--- |
| **Windows** | 10, 11, Server 2016-2022 | ✅ Verified | PyInstaller `.exe` | Primary development platform |
| **Red Hat Enterprise Linux** | 8.x, 9.x | 🟡 Expected | PyInstaller binary | Python psutil supports RHEL; not yet tested |
| **Ubuntu LTS** | 20.04, 22.04 | 🟡 Expected | PyInstaller binary | Python psutil supports Ubuntu; not yet tested |

## eSolutions Agent

| Operating System | Versions | Status | Notes |
| :--- | :--- | :---: | :--- |
| **Windows** | 10, 11, Server 2016-2022 | ✅ Verified | Standalone `.exe` via PyInstaller |
| **RHEL / CentOS** | 7, 8, 9 | 🟡 Expected | Requires Linux build of PyInstaller binary |
| **Ubuntu / Debian** | 18.04+ | 🟡 Expected | Requires Linux build of PyInstaller binary |
| **AIX** | 7.1, 7.2 | 🔴 Not Supported | No PowerPC binaries; would require `psutil` AIX build |

## Packaging Formats

| Format | Status | Notes |
| :--- | :--- | :--- |
| **PyInstaller `.exe` (Windows)** | ✅ Implemented | `build_all.bat` produces `EsMonitorCore.exe` and `EsMonitorAgent.exe` |
| **PyInstaller binary (Linux)** | 🔴 Not Built Yet | Requires building on a Linux machine |
| **MSI Installer (Windows)** | 🔴 Not Implemented | Planned for enterprise rollout via SCCM/GPO |
| **RPM Package (RHEL/CentOS)** | 🔴 Not Implemented | Planned for Ansible-based deployment |
| **DEB Package (Ubuntu/Debian)** | 🔴 Not Implemented | Planned |
| **Docker Container** | 🔴 Not Implemented | Planned for cloud deployments |

---

## Runtime Dependencies

### Target Servers (Agent)
| Dependency | Required? | Notes |
| :--- | :--- | :--- |
| **Python** | ❌ Not required | Agent is packaged as standalone executable |
| **Java JDK 8+** | Only for JMX | Required only if Maximo/WebSphere JMX monitoring is enabled |

### Core Server
| Dependency | Required? | Notes |
| :--- | :--- | :--- |
| **Python** | ❌ Not required | Core is packaged as standalone executable |
| **PostgreSQL** | ❌ Not required | Core uses SQLite (file-based, zero-config) |
| **Web Server** | ❌ Not required | FastAPI serves the dashboard directly |

---

## Network Requirements

| Source | Destination | Port | Protocol | Required |
| :--- | :--- | :--- | :--- | :--- |
| **Agent** | **Core** | 8444 | TCP (HTTP) | ✅ Required |
| **Browser** | **Core** | 8444 | TCP (HTTP) | ✅ For dashboard access |
| **Core** | **SMTP Server** | 587 | TCP (TLS) | Only if email alerts enabled |
