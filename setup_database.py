# setup_database.py
import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Connect to MySQL without specifying database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Sunil@123',
            port=3306
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS face_recognition")
            print("Database 'face_recognition' created successfully")
            
            # Use the database
            cursor.execute("USE face_recognition")
            
            # Create student table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS student (
                Student_ID INT PRIMARY KEY AUTO_INCREMENT,
                Name VARCHAR(100) NOT NULL,
                Roll_No VARCHAR(50) NOT NULL,
                Department VARCHAR(100),
                Semester VARCHAR(50),
                Email VARCHAR(100),
                Phone VARCHAR(20),
                Address TEXT,
                Photo_sample VARCHAR(255),
                Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_query)
            print("Table 'student' created successfully")
            
            # Insert sample data
            insert_query = """
            INSERT INTO student (Name, Roll_No, Department, Semester, Email, Phone) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            sample_data = [
                ('John Doe', '2024001', 'Computer Science', '4th', 'john.doe@example.com', '1234567890'),
                ('Jane Smith', '2024002', 'Computer Science', '4th', 'jane.smith@example.com', '1234567891'),
                ('Mike Johnson', '2024003', 'Information Technology', '3rd', 'mike.johnson@example.com', '1234567892')
            ]
            
            cursor.executemany(insert_query, sample_data)
            conn.commit()
            print("Sample data inserted successfully")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    create_database()