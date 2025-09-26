-- Création de la base de données
CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

-- Table des étudiants
CREATE TABLE IF NOT EXISTS STUDENTS (
    students_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    department VARCHAR(100) NOT NULL
);

-- Table des cours
CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_field VARCHAR(100) NOT NULL,
    course_duration VARCHAR(50) NOT NULL,
    course_price DECIMAL(10, 2) NOT NULL
); 
-- Table des administrateurs
CREATE TABLE IF NOT EXISTS admins (
  admin_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des professeurs
CREATE TABLE IF NOT EXISTS professors (
  professor_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  department VARCHAR(100),
  password VARCHAR(255) NOT NULL
);

-- Table des groupes de collaboration
CREATE TABLE IF NOT EXISTS collaboration_groups (
  group_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  created_by INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (created_by) REFERENCES STUDENTS(students_id) ON DELETE CASCADE
);

-- Table des membres de groupe
CREATE TABLE IF NOT EXISTS group_members (
  member_id INT AUTO_INCREMENT PRIMARY KEY,
  group_id INT NOT NULL,
  student_id INT NOT NULL,
  role ENUM('member', 'admin') DEFAULT 'member',
  joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (group_id) REFERENCES collaboration_groups(group_id) ON DELETE CASCADE,
  FOREIGN KEY (student_id) REFERENCES STUDENTS(students_id) ON DELETE CASCADE,
  UNIQUE KEY unique_group_member (group_id, student_id)
);

-- Table des discussions
CREATE TABLE IF NOT EXISTS discussions (
  discussion_id INT AUTO_INCREMENT PRIMARY KEY,
  group_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  created_by INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_pinned BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (group_id) REFERENCES collaboration_groups(group_id) ON DELETE CASCADE,
  FOREIGN KEY (created_by) REFERENCES STUDENTS(students_id) ON DELETE CASCADE
);

-- Table des messages
CREATE TABLE IF NOT EXISTS messages (
  message_id INT AUTO_INCREMENT PRIMARY KEY,
  discussion_id INT NOT NULL,
  author_id INT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  is_edited BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (discussion_id) REFERENCES discussions(discussion_id) ON DELETE CASCADE,
  FOREIGN KEY (author_id) REFERENCES STUDENTS(students_id) ON DELETE CASCADE
);
