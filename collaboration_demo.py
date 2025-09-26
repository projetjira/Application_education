#!/usr/bin/env python3
"""
Collaboration Features Demo Script

This script demonstrates the collaboration functionality added to the Education Application.
It shows how the APIs work and provides examples of creating groups, discussions, and messages.

Note: This is a demonstration script. In production, you would need:
1. MySQL database running
2. Proper authentication system
3. Input validation and error handling
"""

import json
from datetime import datetime


class CollaborationDemo:
    def __init__(self):
        self.groups = []
        self.group_members = []
        self.discussions = []
        self.messages = []
        self.group_id_counter = 1
        self.discussion_id_counter = 1
        self.message_id_counter = 1
        self.member_id_counter = 1
        
        # Sample students
        self.students = [
            {"students_id": 1, "name": "Alice Johnson", "email": "alice@example.com", "department": "Computer Science"},
            {"students_id": 2, "name": "Bob Smith", "email": "bob@example.com", "department": "Computer Science"},
            {"students_id": 3, "name": "Carol Wilson", "email": "carol@example.com", "department": "Mathematics"},
            {"students_id": 4, "name": "David Brown", "email": "david@example.com", "department": "Physics"},
            {"students_id": 5, "name": "Eva Davis", "email": "eva@example.com", "department": "Computer Science"}
        ]

    def get_student_name(self, student_id):
        """Get student name by ID"""
        for student in self.students:
            if student["students_id"] == student_id:
                return student["name"]
        return "Unknown Student"

    def create_group(self, name, description, created_by):
        """Create a new collaboration group"""
        print(f"\n🏗️  Creating group: '{name}'")
        
        # Simulate API: POST /collaboration/groups?created_by={created_by}
        group = {
            "group_id": self.group_id_counter,
            "name": name,
            "description": description,
            "created_by": created_by,
            "creator_name": self.get_student_name(created_by),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "is_active": True
        }
        
        self.groups.append(group)
        
        # Auto-add creator as admin member
        self.add_group_member(self.group_id_counter, created_by, "admin")
        
        self.group_id_counter += 1
        
        print(f"   ✅ Group created successfully!")
        print(f"   📋 Group ID: {group['group_id']}")
        print(f"   👤 Creator: {group['creator_name']}")
        
        return group

    def add_group_member(self, group_id, student_id, role="member"):
        """Add a student to a collaboration group"""
        student_name = self.get_student_name(student_id)
        print(f"   👥 Adding {student_name} as {role}")
        
        # Simulate API: POST /collaboration/groups/{group_id}/members
        member = {
            "member_id": self.member_id_counter,
            "group_id": group_id,
            "student_id": student_id,
            "role": role,
            "name": student_name,
            "joined_at": datetime.now().isoformat()
        }
        
        self.group_members.append(member)
        self.member_id_counter += 1
        
        return member

    def list_groups(self, student_id=None):
        """List collaboration groups"""
        print(f"\n📋 Listing collaboration groups:")
        
        # Simulate API: GET /collaboration/groups?student_id={student_id}
        if student_id:
            # Filter groups where student is a member
            student_groups = []
            for group in self.groups:
                for member in self.group_members:
                    if member["group_id"] == group["group_id"] and member["student_id"] == student_id:
                        group_copy = group.copy()
                        group_copy["member_role"] = member["role"]
                        group_copy["member_count"] = len([m for m in self.group_members if m["group_id"] == group["group_id"]])
                        student_groups.append(group_copy)
                        break
            groups_to_show = student_groups
        else:
            # Show all groups
            groups_to_show = self.groups.copy()
            for group in groups_to_show:
                group["member_count"] = len([m for m in self.group_members if m["group_id"] == group["group_id"]])
        
        for group in groups_to_show:
            print(f"   🔸 {group['name']} (ID: {group['group_id']})")
            print(f"      📝 {group['description']}")
            print(f"      👤 Created by: {group['creator_name']}")
            print(f"      👥 Members: {group['member_count']}")
            if 'member_role' in group:
                print(f"      🎭 Your role: {group['member_role']}")
            print()

    def create_discussion(self, group_id, title, created_by):
        """Create a new discussion in a group"""
        print(f"\n💬 Creating discussion: '{title}' in group {group_id}")
        
        # Check if user is group member
        is_member = any(m["group_id"] == group_id and m["student_id"] == created_by for m in self.group_members)
        if not is_member:
            print(f"   ❌ Error: Student {created_by} is not a member of group {group_id}")
            return None
        
        # Simulate API: POST /collaboration/groups/{group_id}/discussions?created_by={created_by}
        discussion = {
            "discussion_id": self.discussion_id_counter,
            "group_id": group_id,
            "title": title,
            "created_by": created_by,
            "creator_name": self.get_student_name(created_by),
            "created_at": datetime.now().isoformat(),
            "is_pinned": False
        }
        
        self.discussions.append(discussion)
        self.discussion_id_counter += 1
        
        print(f"   ✅ Discussion created successfully!")
        print(f"   💬 Discussion ID: {discussion['discussion_id']}")
        print(f"   👤 Creator: {discussion['creator_name']}")
        
        return discussion

    def post_message(self, discussion_id, content, author_id):
        """Post a message to a discussion"""
        author_name = self.get_student_name(author_id)
        print(f"\n📝 {author_name} posting message to discussion {discussion_id}")
        
        # Check if discussion exists and user has access
        discussion = next((d for d in self.discussions if d["discussion_id"] == discussion_id), None)
        if not discussion:
            print(f"   ❌ Error: Discussion {discussion_id} not found")
            return None
        
        is_member = any(m["group_id"] == discussion["group_id"] and m["student_id"] == author_id for m in self.group_members)
        if not is_member:
            print(f"   ❌ Error: Student {author_id} doesn't have access to this discussion")
            return None
        
        # Simulate API: POST /collaboration/discussions/{discussion_id}/messages?author_id={author_id}
        message = {
            "message_id": self.message_id_counter,
            "discussion_id": discussion_id,
            "author_id": author_id,
            "author_name": author_name,
            "content": content,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "is_edited": False
        }
        
        self.messages.append(message)
        self.message_id_counter += 1
        
        print(f"   💬 Message: {content[:50]}{'...' if len(content) > 50 else ''}")
        print(f"   ✅ Message posted successfully!")
        
        return message

    def get_discussion_messages(self, discussion_id, student_id):
        """Get messages from a discussion"""
        print(f"\n💬 Getting messages from discussion {discussion_id}")
        
        # Check if user has access
        discussion = next((d for d in self.discussions if d["discussion_id"] == discussion_id), None)
        if not discussion:
            print(f"   ❌ Error: Discussion {discussion_id} not found")
            return []
        
        is_member = any(m["group_id"] == discussion["group_id"] and m["student_id"] == student_id for m in self.group_members)
        if not is_member:
            print(f"   ❌ Error: Access denied")
            return []
        
        # Simulate API: GET /collaboration/discussions/{discussion_id}/messages?student_id={student_id}
        discussion_messages = [m for m in self.messages if m["discussion_id"] == discussion_id]
        discussion_messages.sort(key=lambda x: x["created_at"])
        
        print(f"   📨 Found {len(discussion_messages)} messages:")
        for message in discussion_messages:
            timestamp = message["created_at"][:16].replace('T', ' ')
            print(f"   └─ [{timestamp}] {message['author_name']}: {message['content']}")
        
        return discussion_messages

    def run_demo(self):
        """Run the complete collaboration demo"""
        print("🎓 Education Application - Collaboration Features Demo")
        print("=" * 60)
        
        # Create some groups
        group1 = self.create_group(
            "Data Structures Study Group", 
            "Weekly study sessions for CS 301",
            1  # Alice creates
        )
        
        group2 = self.create_group(
            "Web Development Team",
            "Full-stack web development project collaboration", 
            2  # Bob creates
        )
        
        # Add members to groups
        print(f"\n👥 Adding members to groups:")
        self.add_group_member(group1["group_id"], 2)  # Bob joins Alice's group
        self.add_group_member(group1["group_id"], 5)  # Eva joins Alice's group
        
        self.add_group_member(group2["group_id"], 1)  # Alice joins Bob's group
        self.add_group_member(group2["group_id"], 5)  # Eva joins Bob's group
        
        # List all groups
        self.list_groups()
        
        # List groups for specific student
        self.list_groups(student_id=1)  # Alice's groups
        
        # Create discussions
        discussion1 = self.create_discussion(
            group1["group_id"],
            "Binary Trees - Chapter 5 Questions",
            2  # Bob creates discussion in Alice's group
        )
        
        discussion2 = self.create_discussion(
            group2["group_id"],
            "Project Planning and Tech Stack",
            2  # Bob creates discussion in his own group
        )
        
        # Post messages
        if discussion1:
            self.post_message(
                discussion1["discussion_id"],
                "I'm having trouble with inorder traversal. Can someone help?",
                2  # Bob posts
            )
            
            self.post_message(
                discussion1["discussion_id"],
                "Sure! The key is understanding the recursive calls. Let me explain...",
                1  # Alice responds
            )
            
            self.post_message(
                discussion1["discussion_id"],
                "Thanks! That visualization really helped me understand it.",
                2  # Bob responds
            )
        
        if discussion2:
            self.post_message(
                discussion2["discussion_id"],
                "I think we should use React for frontend and Node.js for backend.",
                2  # Bob suggests
            )
            
            self.post_message(
                discussion2["discussion_id"],
                "Sounds good! I'm comfortable with that stack.",
                5  # Eva agrees
            )
        
        # Get messages from discussions
        if discussion1:
            self.get_discussion_messages(discussion1["discussion_id"], 1)  # Alice views messages
        
        if discussion2:
            self.get_discussion_messages(discussion2["discussion_id"], 5)  # Eva views messages
        
        # Summary
        print("\n📊 Demo Summary:")
        print(f"   🏫 Groups created: {len(self.groups)}")
        print(f"   👥 Total memberships: {len(self.group_members)}")
        print(f"   💬 Discussions created: {len(self.discussions)}")
        print(f"   📝 Messages posted: {len(self.messages)}")
        
        print("\n✅ Collaboration features demo completed successfully!")
        print("\n🔗 Next steps:")
        print("   1. Set up MySQL database")
        print("   2. Run the FastAPI backend server")
        print("   3. Start the Angular frontend")
        print("   4. Test the features through the web interface")


if __name__ == "__main__":
    demo = CollaborationDemo()
    demo.run_demo()