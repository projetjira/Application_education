-- Sample data for testing collaboration features
-- Run this after the main database setup to have test data

-- First, let's add some sample students if they don't exist
INSERT IGNORE INTO STUDENTS (students_id, name, age, email, department, password) VALUES
(1, 'Alice Johnson', 20, 'alice@example.com', 'Computer Science', 'hashed_password_1'),
(2, 'Bob Smith', 21, 'bob@example.com', 'Computer Science', 'hashed_password_2'),
(3, 'Carol Wilson', 19, 'carol@example.com', 'Mathematics', 'hashed_password_3'),
(4, 'David Brown', 22, 'david@example.com', 'Physics', 'hashed_password_4'),
(5, 'Eva Davis', 20, 'eva@example.com', 'Computer Science', 'hashed_password_5');

-- Create sample collaboration groups
INSERT INTO collaboration_groups (group_id, name, description, created_by, created_at, is_active) VALUES
(1, 'Data Structures Study Group', 'Weekly study sessions for CS 301 - Data Structures and Algorithms', 1, '2024-01-15 10:00:00', TRUE),
(2, 'Calculus Help Group', 'Peer tutoring and problem solving for Calculus I', 3, '2024-01-16 14:30:00', TRUE),
(3, 'Physics Lab Partners', 'Collaboration group for Physics 201 laboratory experiments', 4, '2024-01-17 09:15:00', TRUE),
(4, 'Web Development Team', 'Full-stack web development project collaboration', 2, '2024-01-18 16:45:00', TRUE),
(5, 'Machine Learning Research', 'Advanced topics in ML and AI research discussions', 1, '2024-01-19 11:20:00', TRUE);

-- Add members to groups
INSERT INTO group_members (group_id, student_id, role, joined_at) VALUES
-- Data Structures Study Group members
(1, 1, 'admin', '2024-01-15 10:00:00'),  -- Creator (Alice)
(1, 2, 'member', '2024-01-15 11:30:00'), -- Bob
(1, 5, 'member', '2024-01-16 08:45:00'), -- Eva

-- Calculus Help Group members  
(2, 3, 'admin', '2024-01-16 14:30:00'),  -- Creator (Carol)
(2, 1, 'member', '2024-01-16 15:00:00'), -- Alice
(2, 4, 'member', '2024-01-17 10:15:00'), -- David

-- Physics Lab Partners members
(3, 4, 'admin', '2024-01-17 09:15:00'),  -- Creator (David)
(3, 3, 'member', '2024-01-17 09:45:00'), -- Carol
(3, 2, 'member', '2024-01-18 13:20:00'), -- Bob

-- Web Development Team members
(4, 2, 'admin', '2024-01-18 16:45:00'),  -- Creator (Bob)
(4, 5, 'admin', '2024-01-18 17:00:00'),  -- Eva (promoted to admin)
(4, 1, 'member', '2024-01-19 09:30:00'), -- Alice

-- Machine Learning Research members
(5, 1, 'admin', '2024-01-19 11:20:00'),  -- Creator (Alice)
(5, 5, 'member', '2024-01-19 12:00:00'); -- Eva

-- Create sample discussions
INSERT INTO discussions (discussion_id, group_id, title, created_by, created_at, is_pinned) VALUES
-- Data Structures Group discussions
(1, 1, 'Welcome to Data Structures Study Group!', 1, '2024-01-15 10:30:00', TRUE),
(2, 1, 'Binary Trees - Chapter 5 Questions', 2, '2024-01-16 19:15:00', FALSE),
(3, 1, 'Assignment 3 Collaboration', 5, '2024-01-18 14:20:00', FALSE),

-- Calculus Group discussions
(4, 2, 'Group Guidelines and Schedule', 3, '2024-01-16 15:00:00', TRUE),
(5, 2, 'Limits and Continuity Help', 1, '2024-01-17 20:30:00', FALSE),
(6, 2, 'Practice Problems for Midterm', 4, '2024-01-19 16:45:00', FALSE),

-- Physics Lab discussions
(7, 3, 'Lab Safety and Procedures', 4, '2024-01-17 09:30:00', TRUE),
(8, 3, 'Experiment 4: Pendulum Motion', 3, '2024-01-18 11:15:00', FALSE),

-- Web Development discussions  
(9, 4, 'Project Planning and Tech Stack', 2, '2024-01-18 17:15:00', TRUE),
(10, 4, 'Frontend vs Backend Responsibilities', 5, '2024-01-19 10:00:00', FALSE),
(11, 4, 'Database Schema Discussion', 1, '2024-01-20 13:30:00', FALSE),

-- ML Research discussions
(12, 5, 'Research Paper Reviews', 1, '2024-01-19 11:45:00', TRUE),
(13, 5, 'TensorFlow vs PyTorch Discussion', 5, '2024-01-20 15:20:00', FALSE);

-- Create sample messages
INSERT INTO messages (discussion_id, author_id, content, created_at, is_edited) VALUES
-- Welcome discussion messages
(1, 1, 'Welcome everyone! This group is for helping each other with Data Structures coursework. Please introduce yourselves!', '2024-01-15 10:30:00', FALSE),
(1, 2, 'Hi! I\'m Bob, second year CS major. Looking forward to collaborating on assignments and studying together.', '2024-01-15 11:45:00', FALSE),
(1, 5, 'Hey! I\'m Eva. I find trees and graphs challenging, hoping to get better with group practice!', '2024-01-16 08:50:00', FALSE),

-- Binary Trees discussion
(2, 2, 'I\'m having trouble with the inorder traversal implementation. Can someone help explain the recursion?', '2024-01-16 19:15:00', FALSE),
(2, 1, 'Sure! The key is understanding the base case and recursive calls. Let me share some pseudocode...', '2024-01-16 19:45:00', FALSE),
(2, 5, 'This visualization helped me: https://example.com/tree-traversal. The animated examples are really clear!', '2024-01-17 12:30:00', FALSE),

-- Assignment collaboration
(3, 5, 'Anyone want to form study pairs for Assignment 3? I think working together would help us understand the concepts better.', '2024-01-18 14:20:00', FALSE),
(3, 2, 'I\'m interested! I\'ve already started on the first few problems. Want to meet tomorrow?', '2024-01-18 15:10:00', FALSE),

-- Calculus group messages
(4, 3, 'Welcome to our Calculus help group! Let\'s meet every Tuesday and Thursday at 7 PM in the library study room 203.', '2024-01-16 15:00:00', FALSE),
(4, 1, 'Sounds great! Should we create a shared document for practice problems?', '2024-01-16 16:20:00', FALSE),
(4, 4, 'Yes! I can set up a Google Doc and share the link here.', '2024-01-17 09:00:00', FALSE),

-- Limits help discussion
(5, 1, 'I\'m struggling with epsilon-delta proofs. The concept makes sense but the formal proofs are confusing.', '2024-01-17 20:30:00', FALSE),
(5, 3, 'Those are tricky! The key is breaking down the definition step by step. Want to work through an example together?', '2024-01-17 21:15:00', FALSE),

-- Physics lab messages
(7, 4, 'Important: Please review the safety manual before our next lab session. We\'ll be working with electrical equipment.', '2024-01-17 09:30:00', FALSE),
(7, 3, 'Thanks for the reminder! I\'ll also bring safety goggles for everyone just in case.', '2024-01-17 10:00:00', FALSE),

-- Pendulum experiment
(8, 3, 'For the pendulum experiment, should we use the digital timer or the manual stopwatch for more accurate measurements?', '2024-01-18 11:15:00', FALSE),
(8, 4, 'Digital timer would be more precise. We should also do multiple trials to minimize error.', '2024-01-18 12:30:00', FALSE),

-- Web development planning
(9, 2, 'I\'m thinking we should use React for frontend and Node.js with Express for backend. What do you all think?', '2024-01-18 17:15:00', FALSE),
(9, 5, 'Sounds good! I\'m comfortable with that stack. Should we use MongoDB or PostgreSQL for the database?', '2024-01-18 17:30:00', FALSE),
(9, 1, 'I vote for PostgreSQL - it\'s more structured and we can practice SQL queries.', '2024-01-19 09:45:00', FALSE),

-- Frontend vs Backend discussion
(10, 5, 'I\'d like to focus more on frontend development. I\'m interested in learning about responsive design and UX.', '2024-01-19 10:00:00', FALSE),
(10, 2, 'Perfect! I prefer backend work anyway. I can handle the API development and database design.', '2024-01-19 10:15:00', FALSE),
(10, 1, 'I can help with both ends and handle the integration. This division of work should be efficient!', '2024-01-19 11:00:00', FALSE),

-- ML Research messages
(12, 1, 'I found this interesting paper on transformers: "Attention Is All You Need". Should we review it next week?', '2024-01-19 11:45:00', FALSE),
(12, 5, 'Definitely! That\'s a foundational paper. I can prepare a summary of the key concepts to share with the group.', '2024-01-19 13:20:00', FALSE),

-- TensorFlow vs PyTorch
(13, 5, 'What are everyone\'s thoughts on TensorFlow vs PyTorch for our research projects?', '2024-01-20 15:20:00', FALSE),
(13, 1, 'I prefer PyTorch for research - it\'s more intuitive and pythonic. TensorFlow is better for production deployment though.', '2024-01-20 16:45:00', FALSE);

-- Display summary of inserted data
SELECT 
    'Groups Created' as Summary, COUNT(*) as Count 
FROM collaboration_groups
UNION ALL
SELECT 
    'Total Members', COUNT(*) 
FROM group_members
UNION ALL  
SELECT 
    'Discussions Created', COUNT(*) 
FROM discussions
UNION ALL
SELECT 
    'Messages Posted', COUNT(*) 
FROM messages;