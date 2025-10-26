import Header from './components/Header';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import AddTask from './pages/CreateTask';
import Tasks from './pages/Tasks';


export default function App() {
  return (
    <>
      <Header />

      <main className='ml-4 mt-1'>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/tasks" element={<Tasks />} />
          <Route path="/add/task" element={<AddTask />} />
        </Routes>
      </main>
    </>
  );
}
