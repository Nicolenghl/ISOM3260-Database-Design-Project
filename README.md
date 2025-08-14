# ISOM3260-Database-Design-Project

# Vincent Mobile Online System

## Project Overview
This repository contains the implementation of an online mobile device purchasing system for Vincent Mobile, an O2O (Online-to-Offline) organization. The system was developed as a group project for HKUST ISOM 3260 course, based on the business case requirements outlined in the Case.md file.

## System Architecture
The system consists of two main components:

### Frontend (Frontend_real.py)
The frontend handles the user interface and interaction for three main user roles:
- **Customers/Members**: Registration, product browsing, shopping cart management, checkout and order tracking
- **Administrators/Managers**: Product management, officer account management, order processing, and report generation
- **Officers**: Processing trade-in requests and managing orders with trade-in services

The frontend is built using Python with interactive Jupyter widgets for a responsive web-like experience.

### Backend (Backend_real.py)
The backend provides data management and business logic functions including:
- Database connectivity with Oracle
- Product inventory management
- User authentication and authorization
- Order processing and management
- Trade-in service handling
- Report generation for management

## Key Features
- Customer registration and account management
- Product search and browsing
- Shopping cart functionality
- Secure checkout process
- Trade-in service for old devices
- Order tracking and management
- Administrator dashboard with real-time metrics
- Comprehensive reporting system

## Project Contributors
This project was developed as a collaborative effort by Group 205 for ISOM 3260 in Spring 24-25.
Final Grade: A

## Technical Implementation
The system is implemented using:
- Python for both frontend and backend
- Oracle database for data storage
- Jupyter widgets for the user interface
- IPython for interactive display elements
