import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

export default function Login() {
  const [userId, setUserId] = useState('');
  const [pw, setPw] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await api.post('/auth/login', { user_id: userId, pw });
      sessionStorage.setItem('user', JSON.stringify(res.data.user));
      navigate('/main');
    } catch {
      setError('帳號或密碼錯誤');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <h2 style={styles.title}>系統登入</h2>
        <form onSubmit={handleLogin}>
          <div style={styles.field}>
            <label>帳號</label>
            <input style={styles.input} value={userId} onChange={e => setUserId(e.target.value)} required />
          </div>
          <div style={styles.field}>
            <label>密碼</label>
            <input style={styles.input} type="password" value={pw} onChange={e => setPw(e.target.value)} required />
          </div>
          {error && <div style={styles.error}>{error}</div>}
          <button style={styles.btn} type="submit">登入</button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  container: { display:'flex', justifyContent:'center', alignItems:'center', height:'100vh', background:'#f0f2f5' },
  box: { background:'#fff', padding:'40px', borderRadius:'8px', boxShadow:'0 2px 8px rgba(0,0,0,0.15)', width:'320px' },
  title: { textAlign:'center', marginBottom:'24px' },
  field: { marginBottom:'16px', display:'flex', flexDirection:'column', gap:'4px' },
  input: { padding:'8px', border:'1px solid #d9d9d9', borderRadius:'4px', fontSize:'14px' },
  btn: { width:'100%', padding:'10px', background:'#1677ff', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer', fontSize:'16px' },
  error: { color:'red', marginBottom:'12px', textAlign:'center' },
};
