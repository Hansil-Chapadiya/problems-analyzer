# LeetCode Problems Analyzer

The **LeetCode Problems Analyzer** is a web application designed to help programmers analyze and classify LeetCode problems based on their skill level, difficulty, tags, and other parameters. The app provides an intuitive interface for beginners and advanced users alike to find suitable problems, analyze their progress, and optimize their practice routines.

## Features

### For Users:
1. **Classify Problems**:
   - Filter problems by difficulty (Easy, Medium, Hard), tags (e.g., Dynamic Programming, Graphs), and skill level.
   - View problem details such as title, difficulty, and associated tags.
   - Navigate through paginated problem lists for better usability.

2. **Analyze Problems**:
   - Generate detailed analysis for a group of problems, including:
     - Acceptance rate
     - Difficulty distribution
     - Suggested tags for further practice
   - Downloadable analysis reports.

3. **Sign Up and Log In**:
   - Secure authentication for personalized recommendations and analysis history.

### For Admins:
- Manage users and their access levels.
- Monitor overall system usage and performance.

## Technology Stack

### Frontend:
- **Framework**: Next.js with React
- **Styling**: Tailwind CSS
- **Routing**: Next.js routing
- **State Management**: React hooks (e.g., `useState`, `useEffect`)

### Backend:
- **Framework**: Flask (Python)
- **Database**: MongoDB (for storing user data, problem details, and analysis results)
- **Authentication**: JWT (JSON Web Token)
- **API Hosting**: Render

### Deployment:
- **Frontend**: Vercel
- **Backend**: Render
- **Uptime Monitoring**: UptimeRobot

### Additional Tools:
- **Postman**: For API testing and development.
- **UptimeRobot**: For monitoring server availability.

## Installation

### Prerequisites
- Node.js (for frontend development)
- Python 3.8+ (for backend development)
- MongoDB (or use a cloud-based MongoDB Atlas instance)

### Steps

#### 1. Clone the repository:
```bash
# Clone the frontend repo
git clone https://github.com/Hansil-Chapadiya/problems-analyzer.git

```

#### 2. Install dependencies:

##### Frontend:
```bash
cd frontend
npm install
```

##### Backend:
```bash
cd backend
pip install -r requirements.txt
```

#### 3. Start the development servers:

##### Frontend:
```bash
npm run dev
```

##### Backend:
```bash
python app.py
```

#### 4. Configure environment variables:

- Frontend: Add a `.env.local` file in the root directory for API URLs.
- Backend: Configure a `.env` file for database connection strings, secret keys, and API keys.

## Usage

1. **User Registration and Login**:
   - Visit the `/register` page to create a new account.
   - Log in via `/signin` to access the classifier and analyzer.

2. **Classify Problems**:
   - Navigate to `/problems` and select your skill level and problem tags.
   - View the filtered problem list and click on problem titles to view details on LeetCode.

3. **Analyze Problems**:
   - Click on "Analyze All Problems" to generate insights for the selected group.

4. **Refresh Problems**:
   - Use the "Refresh Problems" button to update the list.

## Screenshots

### Classify Page:
- View problems with filters for skill and tags.

### Analyze Page:
- Display detailed insights on selected problems.

### Login/Register Page:
- Simple and secure user authentication interface.

## Future Enhancements

- Add support for custom difficulty levels and tags.
- Include detailed visualizations (e.g., graphs for performance analysis).
- Integration with LeetCode's official API for real-time updates.
- Implement a recommendation engine for personalized problem suggestions.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Commit your changes and push the branch.
4. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

- **Developer**: [Hansil-Chapadiya]
- **Email**: chapadiyahansil@gmail.com
- **GitHub**: [Your GitHub Profile](https://github.com/Hansil-Chapadiya)

---

Thank you for using **LeetCode Problems Analyzer**!
