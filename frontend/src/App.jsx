import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Main from './pages/Main';
import CustPage from './pages/CustPage';
import FactPage from './pages/FactPage';
import ItemPage from './pages/ItemPage';
import UserPage from './pages/UserPage';

function RequireAuth({ children }) {
  return sessionStorage.getItem('user') ? children : <Navigate to="/" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/main" element={<RequireAuth><Main /></RequireAuth>} />
        <Route path="/cust" element={<RequireAuth><CustPage /></RequireAuth>} />
        <Route path="/fact" element={<RequireAuth><FactPage /></RequireAuth>} />
        <Route path="/item" element={<RequireAuth><ItemPage /></RequireAuth>} />
        <Route path="/user" element={<RequireAuth><UserPage /></RequireAuth>} />
      </Routes>
    </BrowserRouter>
  );
}
