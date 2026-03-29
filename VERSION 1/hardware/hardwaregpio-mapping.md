\# GPIO Mapping



\## 🔁 Relay Outputs (Active LOW)



| Relay | GPIO Pin | Function |

|-------|---------|---------|

| R1    | GPIO19  | System1 Control |

| R2    | GPIO26  | System2 Control |

| R3    | GPIO2   | System1 Disk1 Select |

| R4    | GPIO3   | System1 Disk2 Select |

| R5    | GPIO4   | System1 Disk1 Line |

| R6    | GPIO17  | System1 Disk2 Line |

| R7    | GPIO14  | System2 Disk1 Select |

| R8    | GPIO15  | System2 Disk2 Select |

| R9    | GPIO18  | System2 Disk1 Line |

| R10   | GPIO23  | System2 Disk2 Line |

| R11   | GPIO24  | System1 Power Trigger |

| R12   | GPIO25  | System2 Power Trigger |



\---



\## ⚡ Optocoupler Inputs (System Status)



| Signal             | GPIO Pin |

|--------------------|---------|

| SYSTEM1\_STATUS     | GPIO5   |

| SYSTEM2\_STATUS     | GPIO6   |



\---



\## 💽 Disk Detection Sensors



| Signal            | GPIO Pin |

|-------------------|---------|

| SYS1\_DISK1        | GPIO21  |

| SYS1\_DISK2        | GPIO16  |

| SYS2\_DISK1        | GPIO20  |

| SYS2\_DISK2        | GPIO12  |



\---



\## ⚙️ Logic Notes



\- Relays are \*\*active LOW\*\*

\- Optocouplers default active state = `GPIO.LOW`

\- Pull configuration is dynamic based on active state

\- Disk switching is \*\*blocked during power ON\*\*

\- LOCAL mode overrides remote control if manual switching detecteds

