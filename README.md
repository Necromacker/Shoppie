# Buymax AI E-commerce Chatbot

A comprehensive e-commerce chatbot solution that enhances the shopping experience by enabling efficient product search, exploration, and purchase processes.

## Features

- User authentication and session management
- AI-powered product search and recommendations
- Real-time chat interface with product visualization
- Secure API endpoints for product data
- Chat history tracking and analysis
- Responsive design for all devices

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python with Flask
- **Database**: PostgreSQL
- **AI**: Google's Gemini AI
- **Authentication**: JWT (JSON Web Tokens)
- **Styling**: Custom CSS with modern design principles

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Node.js and npm (for frontend development)
- Google Cloud account with Gemini API access

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/buymax-ai.git
   cd buymax-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   # Create a PostgreSQL database named 'buymax_db'
   createdb buymax_db
   
   # Run the schema.sql file
   psql -d buymax_db -f database/schema.sql
   
   # Generate mock data
   python database/mock_data.py
   ```

5. Create a `.env` file in the root directory with the following variables:
   ```
   FLASK_SECRET_KEY=your-secret-key
   JWT_SECRET=your-jwt-secret
   DB_PASSWORD=your-db-password
   GEMINI_API_KEY=your-gemini-api-key
   ```

6. Start the backend server:
```bash
   python server.py
   ```

7. Open the frontend in your browser:
   - Open `index.html` in your web browser
   - Or serve it using a local server

## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /login` - User login

### Products
- `GET /products` - Get all products (with optional filters)
  - Query parameters:
    - `category`: Filter by category
    - `search`: Search in name and description
    - `min_price`: Minimum price filter
    - `max_price`: Maximum price filter

### Chat
- `POST /chat` - Send a message to the AI
- `GET /chat/history` - Get chat history

## Project Structure

```
buymax-ai/
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
├── database/
│   ├── schema.sql
│   └── mock_data.py
├── buymax-ai/
│   ├── api.py
│   └── Buymax.py
├── server.py
├── requirements.txt
└── README.md
```

## Security Features

- Password hashing using bcrypt
- JWT-based authentication
- CORS protection
- Input validation and sanitization
- Secure session management

## Error Handling

The application implements comprehensive error handling:
- Input validation
- Database connection errors
- API rate limiting
- Authentication failures
- Network errors

## Future Improvements

1. Add product recommendations based on chat history
2. Implement real-time notifications
3. Add support for multiple languages
4. Integrate payment processing
5. Add admin dashboard for analytics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
