# MailPro Backend

## Project Documentation

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sekhsokhadam-commits/mailpro-backend.git
   cd mailpro-backend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

### Usage
- To start the server:
  ```bash
  npm start
  ```
- The backend will be running on [http://localhost:3000](http://localhost:3000)

### API Endpoints
- **GET /api/users** - Get a list of users.
- **POST /api/users** - Create a new user.
- **GET /api/users/:id** - Get user by ID.
- **PUT /api/users/:id** - Update user information.
- **DELETE /api/users/:id** - Delete user.

### Security Information
- Ensure to use HTTPS for all API requests.
- Use environment variables for sensitive information (e.g., API keys, database credentials).
- Implement CORS to restrict access to your API.

### License
This project is licensed under the MIT License.