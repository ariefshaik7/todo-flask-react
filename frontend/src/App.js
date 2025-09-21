import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';
import Login from './Login';
import Register from './Register';
import './App.css';

// Create an Axios instance that will automatically add the auth token to headers
const api = axios.create({
  baseURL: 'http://localhost:5001/api',
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['x-access-token'] = token;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// Main component for the To-Do List
function TodoList() {
  const [todos, setTodos] = useState([]);
  const [task, setTask] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/todos')
      .then(response => {
        setTodos(response.data);
      })
      .catch(error => {
        console.error('Error fetching todos:', error);
        if (error.response && error.response.status === 401) {
          handleLogout(); // Token is invalid or expired
        } else {
          setError('Could not fetch to-do items.');
        }
      });
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!task.trim()) return;
    api.post('/todos', { task })
      .then(response => {
        setTodos([...todos, response.data]);
        setTask('');
      }).catch(err => console.error(err));
  };

  const toggleComplete = (id, completed) => {
    api.put(`/todos/${id}`, { completed: !completed })
      .then(response => {
        setTodos(todos.map(todo => (todo.id === id ? response.data : todo)));
      }).catch(err => console.error(err));
  };

  const handleDelete = (id) => {
    api.delete(`/todos/${id}`)
      .then(() => {
        setTodos(todos.filter(todo => todo.id !== id));
      }).catch(err => console.error(err));
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>My To-Do List</h1>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </div>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit} className="todo-form">
        <input
          type="text"
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="Add a new task..."
        />
        <button type="submit">Add</button>
      </form>
      <ul className="todo-list">
        {todos.map(todo => (
          <li key={todo.id} className={todo.completed ? 'completed' : ''}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleComplete(todo.id, todo.completed)}
            />
            <span>{todo.task}</span>
            <button onClick={() => handleDelete(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

// Main App component to handle routing
function App() {
  const token = localStorage.getItem('token');
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={token ? <TodoList /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}
export default App;