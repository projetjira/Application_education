# Collaboration Features

This document describes the collaboration features added to the Education Application, enabling students to work together in groups, participate in discussions, and share knowledge.

## Overview

The collaboration system consists of:

1. **Collaboration Groups** - Student groups for collaborative work
2. **Discussions** - Forum-like discussions within groups
3. **Messaging** - Real-time messaging within discussions
4. **Group Management** - Administrative controls for group oversight

## Database Schema

### Tables Added

#### `collaboration_groups`
- `group_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `name` (VARCHAR(100), NOT NULL) - Group name
- `description` (TEXT) - Optional group description
- `created_by` (INT, NOT NULL) - Student ID who created the group
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- `updated_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)
- `is_active` (BOOLEAN, DEFAULT TRUE) - Whether group is active

#### `group_members`
- `member_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `group_id` (INT, NOT NULL) - Reference to collaboration_groups
- `student_id` (INT, NOT NULL) - Reference to STUDENTS table
- `role` (ENUM('member', 'admin'), DEFAULT 'member') - Member role
- `joined_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

#### `discussions`
- `discussion_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `group_id` (INT, NOT NULL) - Reference to collaboration_groups
- `title` (VARCHAR(200), NOT NULL) - Discussion title
- `created_by` (INT, NOT NULL) - Student ID who created the discussion
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- `is_pinned` (BOOLEAN, DEFAULT FALSE) - Whether discussion is pinned

#### `messages`
- `message_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `discussion_id` (INT, NOT NULL) - Reference to discussions
- `author_id` (INT, NOT NULL) - Student ID who wrote the message
- `content` (TEXT, NOT NULL) - Message content
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- `updated_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)
- `is_edited` (BOOLEAN, DEFAULT FALSE) - Whether message was edited

## API Endpoints

### Group Management

#### Create Group
- **POST** `/collaboration/groups?created_by={student_id}`
- **Body**: `{ "name": "Group Name", "description": "Optional description" }`
- **Response**: Group details with creator information

#### List Groups
- **GET** `/collaboration/groups?student_id={student_id}` (optional filter)
- **Response**: Array of groups with member counts and creator info

#### Join Group
- **POST** `/collaboration/groups/{group_id}/members`
- **Body**: `{ "student_id": 123, "role": "member" }`
- **Response**: Success message

#### List Group Members
- **GET** `/collaboration/groups/{group_id}/members`
- **Response**: Array of group members with student details

### Discussion Management

#### Create Discussion
- **POST** `/collaboration/groups/{group_id}/discussions?created_by={student_id}`
- **Body**: `{ "title": "Discussion Title", "group_id": 1 }`
- **Response**: Discussion details with creator information

#### List Group Discussions
- **GET** `/collaboration/groups/{group_id}/discussions`
- **Response**: Array of discussions with message counts

### Message Management

#### Post Message
- **POST** `/collaboration/discussions/{discussion_id}/messages?author_id={student_id}`
- **Body**: `{ "content": "Message content", "discussion_id": 1 }`
- **Response**: Message details with author information

#### Get Discussion Messages
- **GET** `/collaboration/discussions/{discussion_id}/messages?student_id={student_id}`
- **Response**: Array of messages with author details

## Frontend Components

### Angular Components Created

1. **CollaborationGroupsComponent** (`/collaboration/groups`)
   - Lists all collaboration groups
   - Provides group creation functionality
   - Shows group details and member counts

2. **CreateGroupDialogComponent**
   - Modal dialog for creating new groups
   - Form validation for group name and description
   - Integration with collaboration service

3. **CollaborationService**
   - Angular service for API communication
   - Methods for group, discussion, and message management
   - Error handling and response typing

### Navigation Updates

- Added "Collaboration" menu item to the dashboard navigation
- Added collaboration card to the dashboard overview
- Integrated with existing Angular routing system

## Features

### Group Features
- **Create Groups**: Students can create collaboration groups
- **Join Groups**: Students can join existing groups
- **Group Roles**: Support for member and admin roles
- **Group Management**: Admins can manage group settings and members

### Discussion Features
- **Forum-style Discussions**: Create topics within groups
- **Message Threading**: Organized message display
- **Real-time Updates**: Messages update in real-time
- **Discussion Moderation**: Pin important discussions

### Administrative Features
- **Group Oversight**: Admins can view all groups
- **Member Management**: View and manage group memberships
- **Content Moderation**: Monitor discussions and messages
- **Usage Analytics**: Track collaboration activity

## Security Features

- **Access Control**: Only group members can access group content
- **Authentication**: All endpoints require valid student authentication
- **Data Validation**: Input validation on all forms
- **SQL Injection Prevention**: Parameterized queries used throughout

## Usage Examples

### Creating a Study Group
```typescript
const newGroup = {
  name: "Data Structures Study Group",
  description: "Weekly study sessions for CS 201"
};

this.collaborationService.createGroup(newGroup, studentId).subscribe(
  response => console.log('Group created:', response.group)
);
```

### Joining a Group
```typescript
const memberRequest = {
  student_id: 123,
  role: 'member'
};

this.collaborationService.joinGroup(groupId, memberRequest).subscribe(
  response => console.log('Joined group successfully')
);
```

### Starting a Discussion
```typescript
const discussion = {
  title: "Chapter 5 Questions",
  group_id: 1
};

this.collaborationService.createDiscussion(discussion, studentId).subscribe(
  response => console.log('Discussion created:', response.discussion)
);
```

## Installation and Setup

### Backend Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set up MySQL database with connection details in `main.py`
3. Run the FastAPI server: `python main.py`
4. Database tables will be created automatically on first run

### Frontend Setup
1. Navigate to admin-frontend directory
2. Install dependencies: `npm install`
3. Start development server: `ng serve`
4. Access application at `http://localhost:4200`

## Testing

### Manual Testing Steps
1. Start backend server with MySQL connection
2. Start Angular frontend
3. Login as admin
4. Navigate to Collaboration section
5. Create a new group
6. Add members to the group
7. Create discussions and messages
8. Verify all functionality works end-to-end

### API Testing
Use tools like Postman or curl to test the API endpoints directly:

```bash
# Create a group
curl -X POST "http://localhost:8000/collaboration/groups?created_by=1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Group", "description": "Testing collaboration"}'

# List groups
curl -X GET "http://localhost:8000/collaboration/groups"
```

## Future Enhancements

1. **Real-time Notifications** - WebSocket integration for live updates
2. **File Sharing** - Upload and share files within groups
3. **Video Conferencing** - Integrate video calls for virtual meetings
4. **Calendar Integration** - Schedule group meetings and events
5. **Mobile App** - Dedicated mobile application for collaboration
6. **Search Functionality** - Search messages and discussions
7. **Advanced Moderation** - Content filtering and reporting features

## Support

For issues or questions regarding the collaboration features:
1. Check the API documentation for endpoint details
2. Review the database schema for data structure
3. Examine the Angular components for frontend implementation
4. Test with sample data to verify functionality