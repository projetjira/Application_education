# Application Education

An educational management platform with collaboration features for students, professors, and administrators.

## Features

### Core Management
- **Student Management**: Register, manage, and track student profiles
- **Professor Management**: Manage professor accounts and departments  
- **Course Management**: Create and manage educational courses
- **Administrative Dashboard**: Complete admin interface for system management

### Collaboration System 🆕
- **Student Groups**: Create and join collaborative study groups
- **Discussions**: Forum-style discussions within groups
- **Real-time Messaging**: Chat functionality for group communications
- **Group Management**: Administrative oversight of collaboration activities

## Architecture

### Backend Services
- **Main API**: Python FastAPI server with MySQL database
- **Favorites Service**: Java Spring Boot microservice for managing user favorites
- **Admin Frontend**: Angular-based administrative interface

### Database
- **MySQL Database**: Stores students, professors, courses, admins, and collaboration data
- **RESTful APIs**: JSON-based API endpoints for all operations
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Configure MySQL connection in main.py
python main.py
```

### Frontend Setup
```bash
cd admin-frontend  
npm install
ng serve
```

### Access Points
- **Admin Dashboard**: http://localhost:4200
- **API Documentation**: http://localhost:8000/docs
- **Favorites Service**: http://localhost:9090

## New Collaboration Features

The application now includes comprehensive collaboration tools:

- **Group Creation**: Students can create study groups
- **Member Management**: Join groups and manage roles (member/admin)
- **Discussion Forums**: Create discussion topics within groups
- **Messaging System**: Post and reply to messages in discussions
- **Administrative Oversight**: Admins can monitor all collaboration activities

See [COLLABORATION.md](COLLABORATION.md) for detailed documentation of the collaboration system.

## API Endpoints

### Authentication & Management
- `POST /admin/login` - Admin authentication
- `GET /students` - List all students
- `GET /professors` - List all professors  
- `POST /addstudent` - Register new student
- `POST /addcourse` - Create new course

### Collaboration Endpoints 🆕
- `POST /collaboration/groups` - Create collaboration group
- `GET /collaboration/groups` - List groups
- `POST /collaboration/groups/{group_id}/members` - Join group
- `POST /collaboration/groups/{group_id}/discussions` - Create discussion
- `POST /collaboration/discussions/{discussion_id}/messages` - Post message

## Development

### Technology Stack
- **Backend**: Python FastAPI, MySQL, SQLAlchemy
- **Frontend**: Angular 19, Angular Material, TypeScript
- **Services**: Java Spring Boot (Favorites)
- **Database**: MySQL with relationship management

### Recent Updates
- ✅ Added collaboration database schema
- ✅ Implemented group management APIs  
- ✅ Created Angular collaboration components
- ✅ Updated navigation and dashboard
- ✅ Added comprehensive documentation
