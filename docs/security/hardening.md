# Security & Hardening

## Platform Security
The eSolutions Platform is built with "Secure by Design" principles.

### 1. Encryption
*   **Data in Transit**: All traffic between Agents, Collectors, and Core is encrypted via **TLS 1.3**.
*   **Data at Rest**: Database volumes should be encrypted using LUKS (Linux) or BitLocker (Windows).

### 2. Authentication
*   **Core Access**: Integrated with Active Directory / LDAP.
*   **Agent Auth**: Agents authenticate to Core using a 2048-bit Certificate generated during installation.

### 3. Least Privilege
*   **Linux Agents**: Run as user `esol_agent` (No sudo required).
*   **Windows Agents**: Run as `Network Service`.

## Secrets Management
Passwords used in probes (e.g., DB Connectors) are stored in the **Encrypted Vault**.
*   **Command**: `esol-vault add --key DB_PASS`
*   **Usage**: The agent retrieves the secret into memory only at runtime.
