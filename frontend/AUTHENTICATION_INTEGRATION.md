# Authentication Integration

This document explains how the frontend and backend authentication systems are connected.

## Overview

The authentication system uses JWT tokens for secure user authentication. Users can register, login, and access protected routes.

## Components

### Frontend Components

1. **SignIn Component** (`src/components/SignIn.tsx`)
   - Handles user login
   - Validates credentials with backend
   - Stores JWT tokens in localStorage
   - Redirects to protected pages after successful login

2. **SignUp Component** (`src/components/SignUp.tsx`)
   - Handles user registration
   - Validates form inputs
   - Sends registration data to backend
   - Redirects to login page after successful registration

3. **Navbar Component** (`src/components/Navbar.tsx`)
   - Shows authentication status
   - Displays user information when logged in
   - Provides logout functionality

4. **ProtectedRoute Component** (`src/components/ProtectedRoute.tsx`)
   - Wraps protected pages
   - Redirects unauthenticated users to login page

### Backend Endpoints

- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user information

### Authentication Utilities (`src/utils/auth.ts`)

- **authAPI**: Handles API calls to backend
- **tokenUtils**: Manages JWT tokens in localStorage
- **userUtils**: Manages user information in localStorage

## Authentication Flow

### Registration Flow
1. User fills out signup form
2. Frontend validates form data
3. API call to `/auth/register`
4. On success, redirect to login page
5. On error, display error message

### Login Flow
1. User fills out login form
2. API call to `/auth/login`
3. On success:
   - Store JWT token in localStorage
   - Store user info in localStorage
   - Redirect to protected page
4. On error, display error message

### Protected Routes
1. ProtectedRoute component checks for valid token
2. If authenticated, render the protected component
3. If not authenticated, redirect to login page

### Logout Flow
1. User clicks logout button
2. API call to `/auth/logout`
3. Clear tokens and user info from localStorage
4. Redirect to home page

## Usage

### Testing the Authentication

1. Start the backend server:
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Test the flow:
   - Navigate to `/signup` to create an account
   - Navigate to `/signin` to login
   - Try accessing protected routes like `/trainee-begin`

### Pre-configured Test Users

The backend includes test users:
- Username: `admin`, Password: `123`
- Username: `user`, Password: `password`

## Configuration

### API Base URL
The API base URL is configured in `src/utils/auth.ts`:
```typescript
const API_BASE_URL = 'http://localhost:8000';
```

Change this to match your backend URL in production.

### CORS Configuration
The backend is configured to allow all origins for development. Update the CORS settings in `backend/main.py` for production.

## Security Considerations

1. **Token Storage**: Tokens are stored in localStorage for simplicity. Consider using httpOnly cookies for production.
2. **CORS**: Configured to allow all origins for development. Restrict in production.
3. **HTTPS**: Use HTTPS in production for secure token transmission.
4. **Token Expiration**: Tokens expire after 30 minutes. Implement refresh token logic for better UX.

## Error Handling

The system includes comprehensive error handling:
- Network errors (backend not running)
- Authentication errors (invalid credentials)
- Validation errors (form validation)
- Authorization errors (expired tokens)

All errors are displayed to the user with appropriate messages. 