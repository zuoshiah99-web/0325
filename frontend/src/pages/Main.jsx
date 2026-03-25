import { useNavigate } from 'react-router-dom';

export default function Main() {
  const navigate = useNavigate();
  const user = JSON.parse(sessionStorage.getItem('user') || '{}');

  const handleLogout = () => {
    sessionStorage.clear();
    navigate('/');
  };

  const menus = [
    { label: '客戶資料維護', path: '/cust' },
    { label: '廠商資料維護', path: '/fact' },
    { label: '商品資料維護', path: '/item' },
    { label: '用戶資料維護', path: '/user' },
  ];

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={{ margin: 0 }}>三層式系統</h2>
        <div>
          <span style={{ marginRight: '16px' }}>{user.user_name}</span>
          <button style={styles.logoutBtn} onClick={handleLogout}>登出</button>
        </div>
      </div>
      <div style={styles.grid}>
        {menus.map(m => (
          <button key={m.path} style={styles.card} onClick={() => navigate(m.path)}>
            {m.label}
          </button>
        ))}
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: '100vh', background: '#f0f2f5' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 32px', background: '#1677ff', color: '#fff' },
  grid: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', padding: '60px', maxWidth: '600px', margin: '0 auto' },
  card: { padding: '40px 20px', fontSize: '18px', background: '#fff', border: 'none', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', cursor: 'pointer', transition: 'box-shadow 0.2s' },
  logoutBtn: { padding: '6px 16px', background: '#fff', color: '#1677ff', border: 'none', borderRadius: '4px', cursor: 'pointer' },
};
