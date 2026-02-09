# OS Compatibility Matrix

The eSolutions Monitoring Platform is designed to be infrastructure-agnostic.

## Monitoring Core & Collectors

| Operating System | Version | Supported Architectures | Notes |
| :--- | :--- | :--- | :--- |
| **Red Hat Enterprise Linux** | 8.x, 9.x | x86_64, ARM64 | Recommended for large deployments. |
| **Ubuntu LTS** | 20.04, 22.04 | x86_64, ARM64 | |
| **Windows Server** | 2016, 2019, 2022 | x86_64 | Standard Desktop Experience or Core. |

## eSolutions Agent

| Operating System | Versions | Notes |
| :--- | :--- | :--- |
| **Windows Server** | 2012 R2 - 2022 | MSI Installer available. |
| **RHEL / CentOS** | 7, 8, 9 | RPM packages. |
| **Ubuntu / Debian** | 18.04+ | DEB packages. |
| **AIX** | 7.1, 7.2 | PowerPC binaries available on request. |

## Dependencies

*   **Database**: PostgreSQL 13+ (Preferred) or MySQL 8.0+.
*   **Web Server**: Nginx or Apache (for Dashboard Service).
*   **Runtime**: internal Go runtime (no external Java/Python dependence for Core).
