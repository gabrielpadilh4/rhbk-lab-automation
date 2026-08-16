# Red Hat build of Keycloak Laboratory Automation

This repository contains the architecture, configuration files, and deployment code for building a high-availability Red Hat Build of Keycloak laboratory on Red Hat Enterprise Linux.

## Architecture Overview

The lab consists of 4 dedicated RHEL servers configured in a highly available, load-balanced layout:
![network diagram](./docs/diagram.excalidraw.png)

## Topology & Network Specifications

| Hostname | IP Address | OS | Role | Primary Ports |
| :--- | :--- | :--- | :--- | :--- |
| `control-node` | `192.168.122.1` | | Run the ansible automation code | |
| `httpd.lab.local` | `192.168.122.10` | RHEL 10 | Reverse Proxy / Load Balancer (Apache HTTPD) | 443 |
| `keycloak01.lab.local` | `192.168.122.11` | RHEL 10 | RHBK Active Node 1 | 8443, 7800 |
| `keycloak02.lab.local` | `192.168.122.12` | RHEL 10 | RHBK Active Node 2 | 8443, 7800 |
| `keycloak-postgresql-db.lab.local` | `192.168.122.13` | RHEL 10 | Database Backend (PostgreSQL) | 5432 |

## Prerequisites

Before running the playbook, ensure you have the following installed on your local machine:

- **Ansible**: Install Ansible from [Ansible's installation guide](https://docs.ansible.com/ansible/latest/installation_guide/index.html).
- **Ansible Navigator**: Install Ansible Navigator from [Ansible Navigator's installation guid](https://ansible.readthedocs.io/projects/navigator/installation).
- **Podman**: Install Podman from [Podman's official site](https://podman.io/).

## Usage

1. **Clone the Repository**

   ```sh
   git clone https://github.com/gabrielpadilh4/rhbk-lab-automation
   cd rhbk-lab-automation
   ```

2. Run the playbook to start the environment
   ```sh
   ansible-navigator run playbook.yml 
   ```