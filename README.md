# University Platform

A comprehensive university management system that provides tools for managing students, professors, courses, and administrative functions.

## Features

- **Student Management**: Register, view, update, and manage student records
- **Professor Management**: Manage faculty profiles and assignments  
- **Course Management**: Create and organize academic courses
- **Admin Dashboard**: Administrative interface for university management
- **Authentication System**: Secure login for students, professors, and administrators

## Architecture

- **Backend**: Python FastAPI with MySQL database
- **Admin Frontend**: Angular application for administrative functions
- **Student Frontend**: Student portal interface
- **Favorites Service**: Java Spring Boot microservice for user preferences

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Admin Frontend  
```bash
cd admin-frontend
npm install
ng serve
```

## API Endpoints

The University Platform API provides endpoints for:
- Student registration and management
- Professor management
- Course creation and enrollment
- Administrative functions