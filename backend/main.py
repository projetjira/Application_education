import mysql.connector
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Wrap database connection in try-except to handle connection errors gracefully
try:
    database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="student_db",
        connection_timeout=60
    )
    cursor = database.cursor(dictionary=True)
    
    # Create admins table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    database.commit()

    # Create professors table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professors (
            professor_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            department VARCHAR(255),
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    database.commit()

    # Drop and recreate courses table
    cursor.execute("DROP TABLE IF EXISTS courses")
    database.commit()

    # Create courses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INT AUTO_INCREMENT PRIMARY KEY,
            course_name VARCHAR(255) NOT NULL,
            course_field VARCHAR(255) NOT NULL,
            course_duration VARCHAR(255) NOT NULL,
            course_price VARCHAR(255) NOT NULL,
            professor_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
        )
    """)
    database.commit()

    # Create students table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            department VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    database.commit()
    
    # Create collaboration tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS collaboration_groups (
            group_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            created_by INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (created_by) REFERENCES STUDENTS(students_id) ON DELETE CASCADE
        )
    """)
    database.commit()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_members (
            member_id INT AUTO_INCREMENT PRIMARY KEY,
            group_id INT NOT NULL,
            student_id INT NOT NULL,
            role ENUM('member', 'admin') DEFAULT 'member',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES collaboration_groups(group_id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES STUDENTS(students_id) ON DELETE CASCADE,
            UNIQUE KEY unique_group_member (group_id, student_id)
        )
    """)
    database.commit()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS discussions (
            discussion_id INT AUTO_INCREMENT PRIMARY KEY,
            group_id INT NOT NULL,
            title VARCHAR(200) NOT NULL,
            created_by INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_pinned BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (group_id) REFERENCES collaboration_groups(group_id) ON DELETE CASCADE,
            FOREIGN KEY (created_by) REFERENCES STUDENTS(students_id) ON DELETE CASCADE
        )
    """)
    database.commit()
    
    cursor.execute("""
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
        )
    """)
    database.commit()
    
    db_connected = True
    print("Successfully connected to the database")
except Exception as e:
    print(f"Database connection error: {str(e)}")
    database = None
    cursor = None
    db_connected = False


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import et initialisation du module books
try:
    from books.books_api import books_router, init_books_module
    
    # Initialiser le module books
    init_books_module()
    
    # Enregistrer le routeur books dans l'application principale
    app.include_router(books_router)
    print("Module de recommandations de livres intégré avec succès")
except ImportError as e:
    print(f"Warning: Book recommendations module not loaded: {e}")
except Exception as e:
    print(f"Error initializing book recommendations module: {e}")


class Student(BaseModel):
    name: str
    age: int
    email: str
    department: str
    password: str

class StudentUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    email: Optional[str]
    department: Optional[str]

class Course(BaseModel):
    course_name: str
    course_field: str
    course_duration: str
    course_price: str

class StudentLogin(BaseModel):
    name: str
    email: str
    password: str

class AdminModel(BaseModel):
    name: str
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str

class ProfessorModel(BaseModel):
    name: str
    email: str
    department: Optional[str]
    password: str

class ProfessorUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    department: Optional[str]
    password: Optional[str]

class ProfessorLogin(BaseModel):
    email: str
    password: str

class AdminLogin(BaseModel):
    email: str
    password: str

# Collaboration Models
class CollaborationGroup(BaseModel):
    name: str
    description: Optional[str] = None

class CollaborationGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class Discussion(BaseModel):
    title: str
    group_id: int

class Message(BaseModel):
    content: str
    discussion_id: int

class MessageUpdate(BaseModel):
    content: str

class GroupMember(BaseModel):
    student_id: int
    role: Optional[str] = "member"

@app.get("/")
def root():
    return {
        "message": "Welcome to the Student Management API",
        "endpoints": {
            "test_db": "/test-db",
            "add_student": "/addstudent",
            "login_student": "/loginstudent",
            "student_profile": "/profile",
            "all_students": "/students",
            "add_course": "/addcourse",
            "all_courses": "/courses",
            "admin_login": "/admin/login",
            "admin_register": "/admin/register",
            "admin_students": "/admin/students",
            "admin_professors": "/admin/professors",
            "collaboration": {
                "groups": "/collaboration/groups",
                "create_group": "/collaboration/groups",
                "join_group": "/collaboration/groups/{group_id}/members",
                "discussions": "/collaboration/groups/{group_id}/discussions",
                "messages": "/collaboration/discussions/{discussion_id}/messages"
            }
        }
    }

@app.get("/test-db")
def test_db_connection():
    if not db_connected:
        return {"message": "Database connection is not available"}
    try:
        cursor.execute("SELECT 1")
        cursor.fetchone()
        return {"message": "Database connection is working"}
    except Exception as e:
        return {"message": f"Database error: {str(e)}"}

@app.post("/addstudent")
def add_student(student: Student):
    try:
        # Hash the password for security
        hashed_password = pwd_context.hash(student.password)
        
        # Check if student already exists
        check_sql = "SELECT * FROM STUDENTS WHERE email = %s"
        cursor.execute(check_sql, (student.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Student with this email already exists")
        
        # Insert student with password
        sql = "INSERT INTO STUDENTS (name, age, email, department, password) VALUES (%s, %s, %s, %s, %s)"
        values = (student.name, student.age, student.email, student.department, hashed_password)
        cursor.execute(sql, values)
        database.commit()
        print(f"Student added successfully: {student.name}, {student.email}")
        return {"message": "Student added successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error adding student: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/loginstudent")
def login_student(student: StudentLogin):
    try:
        sql = "SELECT students_id, name, email FROM STUDENTS WHERE name = %s AND email = %s"
        values = (student.name, student.email)
        cursor.execute(sql, values)
        result = cursor.fetchone()

        if result:
            return {
                "message": "Login successful",
                "student_id": result["students_id"],
                "name": result["name"],
                "role": "student"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/register")
def register_admin(admin: AdminModel):
    try:
        print(f"Attempting to register admin with email: {admin.email}")  # Debug log
        # Check if admin already exists
        cursor.execute("SELECT * FROM admins WHERE email = %s", (admin.email,))
        existing_admin = cursor.fetchone()
        print(f"Existing admin check: {existing_admin}")  # Debug log

        if existing_admin:
            print("Admin already exists")  # Debug log
            raise HTTPException(status_code=400, detail="Admin already exists")

        # Hash password
        hashed_password = pwd_context.hash(admin.password)
        print("Password hashed successfully")  # Debug log

        # Insert new admin
        sql = "INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)"
        values = (admin.name, admin.email, hashed_password)
        cursor.execute(sql, values)
        database.commit()
        print("Admin inserted successfully")  # Debug log

        # Get the newly created admin
        cursor.execute("SELECT * FROM admins WHERE email = %s", (admin.email,))
        new_admin = cursor.fetchone()
        print(f"New admin created: {new_admin}")  # Debug log

        return {
            "message": "Admin registered successfully",
            "admin_id": new_admin["admin_id"],
            "name": new_admin["name"],
            "email": new_admin["email"]
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in admin registration: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/admin/login")
def login_admin(login: AdminLogin):
    try:
        email = login.email.strip()
        print(f"Attempting login for admin with email: {email}")  # Debug log
        cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
        admin = cursor.fetchone()
        print(f"Found admin: {admin}")  # Debug log

        if not admin:
            print("Admin not found")  # Debug log
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Verify password
        print(f"Plain password: '{login.password}'")
        print(f"Hashed password: '{admin['password']}'")
        print("Password verification result:", pwd_context.verify(login.password, admin["password"]))

        if not pwd_context.verify(login.password, admin["password"]):
            print("Password verification failed")  # Debug log
            raise HTTPException(status_code=401, detail="Invalid credentials")

        print("Login successful")  # Debug log
        return {
            "message": "Login successful",
            "admin_id": admin["admin_id"],
            "name": admin["name"],
            "email": admin["email"],
            "token": "dummy-token",
            "role": "admin"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in admin login: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/admin/students")
def get_all_students():
    try:
        cursor.execute("SELECT * FROM STUDENTS")
        results = cursor.fetchall()
        return {"students": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/students")
def create_student(student: Student):
    try:
        cursor.execute("SELECT * FROM STUDENTS WHERE email = %s", (student.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Student already exists")

        # Hash the password
        hashed_password = pwd_context.hash(student.password)
        
        sql = "INSERT INTO STUDENTS (name, age, email, department, password) VALUES (%s, %s, %s, %s, %s)"
        values = (student.name, student.age, student.email, student.department, hashed_password)
        cursor.execute(sql, values)
        database.commit()
        return {"message": "Student created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/admin/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    try:
        cursor.execute("SELECT * FROM STUDENTS WHERE students_id = %s", (student_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Student not found")

        update_fields = []
        values = []
        if student.name:
            update_fields.append("name = %s")
            values.append(student.name)
        if student.age:
            update_fields.append("age = %s")
            values.append(student.age)
        if student.email:
            update_fields.append("email = %s")
            values.append(student.email)
        if student.department:
            update_fields.append("department = %s")
            values.append(student.department)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        values.append(student_id)
        sql = f"UPDATE STUDENTS SET {', '.join(update_fields)} WHERE students_id = %s"
        cursor.execute(sql, values)
        database.commit()

        return {"message": "Student updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/admin/students/{student_id}")
def delete_student(student_id: int):
    try:
        cursor.execute("SELECT * FROM STUDENTS WHERE students_id = %s", (student_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Student not found")

        cursor.execute("DELETE FROM STUDENTS WHERE students_id = %s", (student_id,))
        database.commit()
        return {"message": "Student deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/professors")
def get_all_professors():
    try:
        cursor.execute("SELECT * FROM professors")
        results = cursor.fetchall()
        return {"professors": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/professors")
def create_professor(professor: ProfessorModel):
    try:
        try:
            cursor.execute("SELECT * FROM professors WHERE email = %s", (professor.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Professor already exists")

            hashed_password = pwd_context.hash(professor.password)
            sql = "INSERT INTO professors (name, email, department, password) VALUES (%s, %s, %s, %s)"
            values = (professor.name, professor.email, professor.department, hashed_password)
            cursor.execute(sql, values)
            database.commit()
            
            # Get the newly created professor
            cursor.execute("SELECT * FROM professors WHERE email = %s", (professor.email,))
            new_professor = cursor.fetchone()
            
            # Return the new professor data
            return new_professor
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Handle outer exceptions if needed
        raise HTTPException(status_code=500, detail=f"Outer exception: {str(e)}")

@app.put("/admin/professors/{professor_id}")
def update_professor(professor_id: int, professor: ProfessorUpdate):
    try:
        cursor.execute("SELECT * FROM professors WHERE professor_id = %s", (professor_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Professor not found")

        update_fields = []
        values = []
        if professor.name:
            update_fields.append("name = %s")
            values.append(professor.name)
        if professor.email:
            update_fields.append("email = %s")
            values.append(professor.email)
        if professor.department:
            update_fields.append("department = %s")
            values.append(professor.department)
        if professor.password:
            update_fields.append("password = %s")
            values.append(pwd_context.hash(professor.password))

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        values.append(professor_id)
        sql = f"UPDATE professors SET {', '.join(update_fields)} WHERE professor_id = %s"
        cursor.execute(sql, values)
        database.commit()
        
        # Get the updated professor data
        cursor.execute("SELECT * FROM professors WHERE professor_id = %s", (professor_id,))
        updated_professor = cursor.fetchone()
        
        # Return the updated professor data instead of just a message
        return updated_professor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/admin/professors/{professor_id}")
def delete_professor(professor_id: int):
    try:
        cursor.execute("SELECT * FROM professors WHERE professor_id = %s", (professor_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Professor not found")

        cursor.execute("DELETE FROM professors WHERE professor_id = %s", (professor_id,))
        database.commit()
        return {"message": "Professor deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/addcourse")
def add_course(course: Course, professor_id: int = Query(..., description="The ID of the professor creating the course")):
    try:
        # Verify professor exists
        cursor.execute("SELECT * FROM professors WHERE professor_id = %s", (professor_id,))
        professor = cursor.fetchone()
        if not professor:
            raise HTTPException(status_code=404, detail="Professor not found")

        # Insert new course
        sql = """
            INSERT INTO courses 
            (course_name, course_field, course_duration, course_price, professor_id) 
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            course.course_name, 
            course.course_field, 
            course.course_duration, 
            course.course_price,
            professor_id
        )
        cursor.execute(sql, values)
        database.commit()
        
        # Get the newly created course
        cursor.execute("SELECT * FROM courses WHERE course_id = LAST_INSERT_ID()")
        new_course = cursor.fetchone()
        
        return {
            "message": "Course added successfully",
            "course": new_course
        }
    except Exception as e:
        print(f"Error in course creation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/courses")
def show_courses():
    try:
        cursor.execute("""
            SELECT c.*, p.name as professor_name, p.email as professor_email 
            FROM courses c
            INNER JOIN professors p ON c.professor_id = p.professor_id
        """)
        results = cursor.fetchall()
        return {"courses": results}
    except Exception as e:
        print(f"Error fetching courses: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/profile")
def get_student_profile(student_id: int = Query(..., description="The ID of the student")):
    try:
        sql = "SELECT * FROM STUDENTS WHERE students_id = %s"
        values = (student_id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()

        if result:
            return {
                "student_id": result["students_id"],
                "name": result["name"],
                "age": result["age"],
                "email": result["email"],
                "department": result["department"]
            }
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/auth/professor/login")
def login_professor(professor: ProfessorLogin):
    try:
        print(f"Attempting login for professor with email: {professor.email}")  # Debug log
        cursor.execute("SELECT professor_id, email, password FROM professors WHERE email = %s", (professor.email,))
        result = cursor.fetchone()
        print(f"Query result: {result}")  # Debug log

        if not result:
            print("Professor not found")  # Debug log
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Verify password
        print(f"Verifying password for professor: {result['email']}")  # Debug log
        if not pwd_context.verify(professor.password, result["password"]):
            print("Password verification failed")  # Debug log
            raise HTTPException(status_code=401, detail="Invalid credentials")

        print("Login successful")  # Debug log
        return {
            "message": "Login successful",
            "professor_id": result["professor_id"],
            "email": result["email"],
            "role": "professor"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in professor login: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/students/{student_id}")
def get_student(student_id: int):
    try:
        cursor.execute("SELECT * FROM STUDENTS WHERE students_id = %s", (student_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Student not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/professors/{professor_id}")
def get_professor(professor_id: int):
    try:
        cursor.execute("SELECT * FROM professors WHERE professor_id = %s", (professor_id,))
        professor = cursor.fetchone()
        if not professor:
            raise HTTPException(status_code=404, detail="Professor not found")
        return professor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===============================
# COLLABORATION ENDPOINTS
# ===============================

@app.post("/collaboration/groups")
def create_collaboration_group(group: CollaborationGroup, created_by: int = Query(..., description="Student ID creating the group")):
    """Create a new collaboration group"""
    if not db_connected:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        # Check if student exists
        cursor.execute("SELECT students_id FROM STUDENTS WHERE students_id = %s", (created_by,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Create the group
        sql = """INSERT INTO collaboration_groups (name, description, created_by) VALUES (%s, %s, %s)"""
        values = (group.name, group.description, created_by)
        cursor.execute(sql, values)
        database.commit()
        
        group_id = cursor.lastrowid
        
        # Add creator as admin member
        cursor.execute("""
            INSERT INTO group_members (group_id, student_id, role) VALUES (%s, %s, 'admin')
        """, (group_id, created_by))
        database.commit()
        
        # Return the created group
        cursor.execute("""
            SELECT cg.*, s.name as creator_name 
            FROM collaboration_groups cg 
            JOIN STUDENTS s ON cg.created_by = s.students_id 
            WHERE cg.group_id = %s
        """, (group_id,))
        new_group = cursor.fetchone()
        
        return {
            "message": "Group created successfully",
            "group": new_group
        }
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collaboration/groups")
def get_collaboration_groups(student_id: Optional[int] = Query(None, description="Filter groups by student membership")):
    """Get all collaboration groups or groups for a specific student"""
    if not db_connected:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        if student_id:
            # Get groups where student is a member
            sql = """
                SELECT cg.*, s.name as creator_name, gm.role as member_role,
                       COUNT(DISTINCT gm2.member_id) as member_count
                FROM collaboration_groups cg
                JOIN STUDENTS s ON cg.created_by = s.students_id
                JOIN group_members gm ON cg.group_id = gm.group_id AND gm.student_id = %s
                LEFT JOIN group_members gm2 ON cg.group_id = gm2.group_id
                WHERE cg.is_active = TRUE
                GROUP BY cg.group_id, gm.role
                ORDER BY cg.updated_at DESC
            """
            cursor.execute(sql, (student_id,))
        else:
            # Get all active groups
            sql = """
                SELECT cg.*, s.name as creator_name,
                       COUNT(DISTINCT gm.member_id) as member_count
                FROM collaboration_groups cg
                JOIN STUDENTS s ON cg.created_by = s.students_id
                LEFT JOIN group_members gm ON cg.group_id = gm.group_id
                WHERE cg.is_active = TRUE
                GROUP BY cg.group_id
                ORDER BY cg.updated_at DESC
            """
            cursor.execute(sql)
        
        groups = cursor.fetchall()
        return {"groups": groups}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/collaboration/groups/{group_id}/members")
def join_collaboration_group(group_id: int, member: GroupMember):
    """Add a student to a collaboration group"""
    if not db_connected:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        # Check if group exists and is active
        cursor.execute("SELECT * FROM collaboration_groups WHERE group_id = %s AND is_active = TRUE", (group_id,))
        group = cursor.fetchone()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found or inactive")
        
        # Check if student exists
        cursor.execute("SELECT students_id FROM STUDENTS WHERE students_id = %s", (member.student_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Check if student is already a member
        cursor.execute("SELECT * FROM group_members WHERE group_id = %s AND student_id = %s", 
                      (group_id, member.student_id))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Student is already a member of this group")
        
        # Add member to group
        cursor.execute("""
            INSERT INTO group_members (group_id, student_id, role) VALUES (%s, %s, %s)
        """, (group_id, member.student_id, member.role))
        database.commit()
        
        return {"message": "Successfully joined group", "group_id": group_id, "student_id": member.student_id}
    except HTTPException:
        database.rollback()
        raise
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collaboration/groups/{group_id}/members")
def get_group_members(group_id: int):
    """Get all members of a collaboration group"""
    if not db_connected:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        # Check if group exists
        cursor.execute("SELECT * FROM collaboration_groups WHERE group_id = %s", (group_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Group not found")
        
        # Get group members
        cursor.execute("""
            SELECT gm.*, s.name, s.email, s.department
            FROM group_members gm
            JOIN STUDENTS s ON gm.student_id = s.students_id
            WHERE gm.group_id = %s
            ORDER BY gm.role DESC, gm.joined_at ASC
        """, (group_id,))
        
        members = cursor.fetchall()
        return {"members": members}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/collaboration/groups/{group_id}/discussions")
def create_discussion(group_id: int, discussion: Discussion, created_by: int = Query(..., description="Student ID creating the discussion")):
    """Create a new discussion in a collaboration group"""
    if not db_connected:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        # Check if user is a member of the group
        cursor.execute("""
            SELECT * FROM group_members WHERE group_id = %s AND student_id = %s
        """, (group_id, created_by))
        if not cursor.fetchone():
            raise HTTPException(status_code=403, detail="You must be a member of the group to create discussions")
        
        # Create discussion
        cursor.execute("""
            INSERT INTO discussions (group_id, title, created_by) VALUES (%s, %s, %s)
        """, (group_id, discussion.title, created_by))
        database.commit()
        
        discussion_id = cursor.lastrowid
        
        # Return the created discussion
        cursor.execute("""
            SELECT d.*, s.name as creator_name
            FROM discussions d
            JOIN STUDENTS s ON d.created_by = s.students_id
            WHERE d.discussion_id = %s
        """, (discussion_id,))
        new_discussion = cursor.fetchone()
        
        return {
            "message": "Discussion created successfully",
            "discussion": new_discussion
        }
    except HTTPException:
        database.rollback()
        raise
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collaboration/groups/{group_id}/discussions")
def get_group_discussions(group_id: int):
    """Get all discussions for a collaboration group"""
    if not db_connected:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        # Check if group exists
        cursor.execute("SELECT * FROM collaboration_groups WHERE group_id = %s", (group_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Group not found")
        
        # Get discussions
        cursor.execute("""
            SELECT d.*, s.name as creator_name,
                   COUNT(m.message_id) as message_count
            FROM discussions d
            JOIN STUDENTS s ON d.created_by = s.students_id
            LEFT JOIN messages m ON d.discussion_id = m.discussion_id
            WHERE d.group_id = %s
            GROUP BY d.discussion_id
            ORDER BY d.is_pinned DESC, d.created_at DESC
        """, (group_id,))
        
        discussions = cursor.fetchall()
        return {"discussions": discussions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/collaboration/discussions/{discussion_id}/messages")
def create_message(discussion_id: int, message: Message, author_id: int = Query(..., description="Student ID creating the message")):
    """Create a new message in a discussion"""
    if not db_connected:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        # Check if discussion exists and user has access
        cursor.execute("""
            SELECT d.*, gm.student_id
            FROM discussions d
            JOIN group_members gm ON d.group_id = gm.group_id
            WHERE d.discussion_id = %s AND gm.student_id = %s
        """, (discussion_id, author_id))
        
        if not cursor.fetchone():
            raise HTTPException(status_code=403, detail="Access denied or discussion not found")
        
        # Create message
        cursor.execute("""
            INSERT INTO messages (discussion_id, author_id, content) VALUES (%s, %s, %s)
        """, (discussion_id, author_id, message.content))
        database.commit()
        
        message_id = cursor.lastrowid
        
        # Return the created message
        cursor.execute("""
            SELECT m.*, s.name as author_name
            FROM messages m
            JOIN STUDENTS s ON m.author_id = s.students_id
            WHERE m.message_id = %s
        """, (message_id,))
        new_message = cursor.fetchone()
        
        return {
            "message": "Message created successfully",
            "message_data": new_message
        }
    except HTTPException:
        database.rollback()
        raise
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collaboration/discussions/{discussion_id}/messages")
def get_discussion_messages(discussion_id: int, student_id: int = Query(..., description="Student ID requesting messages")):
    """Get all messages in a discussion"""
    if not db_connected:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        # Check if user has access to this discussion
        cursor.execute("""
            SELECT d.*
            FROM discussions d
            JOIN group_members gm ON d.group_id = gm.group_id
            WHERE d.discussion_id = %s AND gm.student_id = %s
        """, (discussion_id, student_id))
        
        if not cursor.fetchone():
            raise HTTPException(status_code=403, detail="Access denied or discussion not found")
        
        # Get messages
        cursor.execute("""
            SELECT m.*, s.name as author_name
            FROM messages m
            JOIN STUDENTS s ON m.author_id = s.students_id
            WHERE m.discussion_id = %s
            ORDER BY m.created_at ASC
        """, (discussion_id,))
        
        messages = cursor.fetchall()
        return {"messages": messages}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    