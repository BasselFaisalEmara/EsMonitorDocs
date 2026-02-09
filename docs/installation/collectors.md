# Collectors Strategy

Collectors are deployed in **Edge Zones** to strictly control traffic flow back to the Core.

## Topography
*   **DMZ Collector**: Aggregates data from Public Web Servers.
*   **Secure Zone Collector**: Aggregates data from DB2 and Internal App Servers.

## Deployment Steps

1.  **Provision VM**: Minimal OS (RHEL/Windows Core).
2.  **Install Binary**: `esolutions-collector`.
3.  **Key Exchange**:
    Generated a unique `connector_token` from the Core UI.
    Paste this token into the Collector setup wizard.

## Traffic Shaping
Collectors compress payloads to reduce WAN bandwidth.
*   **Compression**: GZIP (Level 6).
*   **Batch Size**: 1000 metrics per packet.
*   **Port**: Outbound connection to Core on **TCP 8443**.
