# Database Migration Guide

## Overview

Your UrTraining backend has been successfully migrated from in-memory storage to PostgreSQL database persistence. This guide explains the changes made and how to use the new database-backed system.

## Changes Made

### 1. Database Configuration
- **New file**: `app/database.py` - Database connection and session management
- **Connection string**: Uses the PostgreSQL service defined in your `docker-compose.yml`
- **Environment variables**: Database URL can be configured via `.env` file

### 2. Database Models
- **New file**: `app/models/database_models.py` - SQLAlchemy ORM models
- **Tables created**:
  - `users` - User accounts with authentication
  - `training_profiles` - User training preferences and information
  - `active_sessions` - JWT token session management
  - `courses` - Training courses/programs
  - `user_course_progress` - User progress tracking

### 3. CRUD Operations
- **New file**: `app/crud.py` - Database operations replacing in-memory functions
- **Operations**: Create, Read, Update, Delete for all entities
- **Session management**: Proper database session handling

### 4. Updated Routes
- **Authentication** (`app/routes/auth.py`): Now uses database for user authentication and session management
- **Users** (`app/routes/users.py`): All user operations now persist to database
- **Sample data**: Automatic initialization with admin and test users

### 5. Database Initialization
- **Automatic setup**: Tables are created on application startup
- **Sample data**: Default admin and user accounts are created
- **Script**: `init_db.py` for manual database setup

## Setup Instructions

### 1. Create Environment File
Create a `.env` file in your project root:

```env
# Database Configuration
DATABASE_URL=postgresql://uruser:urpassword@db:5432/urtraining

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production-please
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

### 2. Start the Application
Run your existing docker-compose setup:

```bash
docker-compose up --build
```

The application will:
1. Start the PostgreSQL database service
2. Create all necessary tables automatically
3. Initialize sample data (admin and regular user)
4. Start the FastAPI backend

### 3. Default Users
Two users are created automatically:

**Admin User:**
- Username: `admin`
- Password: `123`
- Email: `admin@example.com`
- Role: Administrator

**Regular User:**
- Username: `user`
- Password: `password`
- Email: `user@example.com`
- Role: Regular user

## API Changes

### Authentication
All authentication endpoints remain the same but now use database storage:
- `POST /auth/login` - Login with database user verification
- `POST /auth/register` - Create new user in database
- `POST /auth/logout` - Revoke session from database
- `GET /auth/me` - Get current user from database

### Session Management
- JWT tokens are now stored in the database with expiration tracking
- Active sessions can be viewed and managed
- Automatic cleanup of expired sessions

### User Management
All user endpoints now persist data:
- `GET /api/users` - List all users from database
- `POST /api/users` - Create user profile in database
- `GET /api/users/{id}` - Get user from database
- `PUT /api/users/{id}` - Update user in database
- `DELETE /api/users/{id}` - Delete user from database

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_admin BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Training Profiles Table
```sql
CREATE TABLE training_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id),
    gender VARCHAR(10),
    age INTEGER,
    height_cm INTEGER,
    weight_kg FLOAT,
    training_goals JSON,
    training_level VARCHAR(20),
    frequency_last_3_months VARCHAR(30),
    training_location VARCHAR(20),
    location_details VARCHAR(30),
    session_duration VARCHAR(20),
    joint_back_problems BOOLEAN,
    chronic_conditions BOOLEAN,
    health_details TEXT,
    strength_training INTEGER,
    cardio INTEGER,
    hiit INTEGER,
    yoga_pilates INTEGER,
    functional_training INTEGER,
    stretching INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## Manual Database Operations

### Initialize Database Manually
If you need to set up the database manually:

```bash
# Run the initialization script
docker-compose exec backend python init_db.py
```

### Access Database Directly
Connect to PostgreSQL:

```bash
# Connect to database
docker-compose exec db psql -U uruser -d urtraining

# List tables
\dt

# View users
SELECT * FROM users;

# View training profiles
SELECT * FROM training_profiles;
```

## Benefits of Database Migration

1. **Data Persistence**: Data survives application restarts
2. **Scalability**: Can handle multiple users and concurrent requests
3. **Data Integrity**: ACID compliance and foreign key constraints
4. **Backup/Recovery**: Standard database backup procedures
5. **Performance**: Indexed queries and optimized operations
6. **Multi-user Support**: Proper session and user management

## Monitoring and Maintenance

### Database Health
- Monitor PostgreSQL logs: `docker-compose logs db`
- Check application logs: `docker-compose logs backend`
- Monitor database connections and performance

### Backup Procedures
```bash
# Create database backup
docker-compose exec db pg_dump -U uruser urtraining > backup.sql

# Restore from backup
docker-compose exec -T db psql -U uruser urtraining < backup.sql
```

### Session Cleanup
The application automatically cleans up expired sessions, but you can also:

```python
# Manual cleanup via API or database
DELETE FROM active_sessions WHERE expires_at < NOW();
```

## Troubleshooting

### Database Connection Issues
1. Ensure PostgreSQL service is running: `docker-compose ps`
2. Check database logs: `docker-compose logs db`
3. Verify connection settings in `.env` file
4. Ensure database user has proper permissions

### Migration Issues
1. Check if tables exist: Connect to database and run `\dt`
2. Verify sample data: `SELECT * FROM users;`
3. Check application startup logs for errors

### Authentication Problems
1. Verify users exist in database
2. Check password hashing compatibility
3. Ensure JWT secret is properly configured

## Next Steps

Your application now has a robust database backend. Consider these improvements:

1. **Production Security**: Change default passwords and JWT secret
2. **Database Optimization**: Add indexes for frequently queried fields
3. **Backup Strategy**: Implement regular automated backups
4. **Monitoring**: Add database performance monitoring
5. **Migrations**: Implement database migration system for future schema changes

The migration is complete and your application should now be running with full database persistence! 