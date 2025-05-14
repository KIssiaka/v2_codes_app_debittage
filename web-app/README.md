### Step 1: Set Up Your Development Environment

1. **Install Node.js**: Download and install Node.js from [nodejs.org](https://nodejs.org/). This will also install npm (Node Package Manager).

2. **Install Git**: If you haven't already, install Git from [git-scm.com](https://git-scm.com/).

3. **Set Up a Code Editor**: Use a code editor like Visual Studio Code, Atom, or Sublime Text.

### Step 2: Create the Project Structure

1. **Create a New Directory**: Open your terminal and create a new directory for your project.

   ```bash
   mkdir my-web-app
   cd my-web-app
   ```

2. **Initialize a Git Repository**:

   ```bash
   git init
   ```

### Step 3: Set Up the Backend with Node.js

1. **Create a Backend Directory**:

   ```bash
   mkdir backend
   cd backend
   ```

2. **Initialize a Node.js Project**:

   ```bash
   npm init -y
   ```

3. **Install Express**:

   ```bash
   npm install express
   ```

4. **Create a Basic Server**:

   Create a file named `server.js` in the `backend` directory:

   ```javascript
   // backend/server.js
   const express = require('express');
   const app = express();
   const PORT = process.env.PORT || 5000;

   app.get('/', (req, res) => {
       res.send('Hello World!');
   });

   app.listen(PORT, () => {
       console.log(`Server is running on http://localhost:${PORT}`);
   });
   ```

5. **Run the Server**:

   ```bash
   node server.js
   ```

   You should see "Server is running on http://localhost:5000" in your terminal. Open this URL in your browser to see "Hello World!".

### Step 4: Set Up the Frontend with React

1. **Create a Frontend Directory**:

   In the root of your project, create a new React app:

   ```bash
   npx create-react-app frontend
   ```

2. **Navigate to the Frontend Directory**:

   ```bash
   cd frontend
   ```

3. **Start the React App**:

   ```bash
   npm start
   ```

   This will start the React development server, and you should see the default React app in your browser at `http://localhost:3000`.

### Step 5: Connect Frontend and Backend

1. **Modify the React App**:

   Open `frontend/src/App.js` and modify it to fetch data from your backend:

   ```javascript
   import React, { useEffect, useState } from 'react';

   function App() {
       const [message, setMessage] = useState('');

       useEffect(() => {
           fetch('http://localhost:5000/')
               .then(response => response.text())
               .then(data => setMessage(data));
       }, []);

       return (
           <div>
               <h1>Message from Backend:</h1>
               <p>{message}</p>
           </div>
       );
   }

   export default App;
   ```

2. **CORS Configuration** (Optional):

   If you encounter CORS issues, you can install the `cors` package in your backend:

   ```bash
   cd backend
   npm install cors
   ```

   Then, modify your `server.js` to use CORS:

   ```javascript
   const cors = require('cors');
   app.use(cors());
   ```

### Step 6: Finalize and Test

1. **Run Both Servers**:

   - Make sure your backend server is running (`node server.js`).
   - Make sure your React app is running (`npm start` in the `frontend` directory).

2. **Test the Application**: Open your browser and navigate to `http://localhost:3000`. You should see the message fetched from your backend.

### Step 7: Version Control

1. **Add Files to Git**:

   ```bash
   git add .
   git commit -m "Initial commit"
   ```

### Conclusion

You now have a basic web application with a Node.js backend and a React frontend. You can expand this project by adding more routes, connecting to a database, implementing user authentication, and more. Happy coding!