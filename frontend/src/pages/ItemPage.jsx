import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

export default function ItemPage() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [facts, setFacts] = useState([]);
  const [search, setSearch] = useState('');
  const [form, setForm] = useState({ item_id: '', item_name: '', fact_code: '' });
  const [editId, setEditId] = useState(null);
  const [msg, setMsg] = useState('');

  const load = async (q = '') => {
    const res = await api.get('/item', { params: q ? { q } : {} });
    setRows(res.data);
  };

  useEffect(() => {
    load();
    api.get('/fact').then(r => setFacts(r.data));
  }, []);

  const showMsg = (m) => { setMsg(m); setTimeout(() => setMsg(''), 2000); };

  const handleSave = async () => {
    try {
      if (editId) {
        await api.put(`/item/${editId}`, form);
        showMsg('修改成功');
      } else {
        await api.post('/item', form);
        showMsg('新增成功');
      }
      setForm({ item_id: '', item_name: '', fact_code: '' });
      setEditId(null);
      load(search);
    } catch (e) {
      showMsg(e.response?.data?.message || '操作失敗');
    }
  };

  const handleEdit = (row) => { setEditId(row.item_id); setForm({ ...row }); };

  const handleDelete = async (id) => {
    if (!window.confirm('確定刪除？')) return;
    await api.delete(`/item/${id}`);
    showMsg('刪除成功');
    load(search);
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <button style={styles.backBtn} onClick={() => navigate('/main')}>← 返回</button>
        <h2 style={{ margin: 0 }}>商品資料維護</h2>
      </div>
      <div style={styles.body}>
        <div style={styles.toolbar}>
          <input style={styles.input} placeholder="查詢..." value={search}
            onChange={e => setSearch(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && load(search)} />
          <button style={styles.btn} onClick={() => load(search)}>查詢</button>
          <button style={{ ...styles.btn, background: '#52c41a' }} onClick={() => { setEditId(null); setForm({ item_id: '', item_name: '', fact_code: '' }); }}>新增</button>
        </div>
        {msg && <div style={styles.msg}>{msg}</div>}
        <div style={styles.formBox}>
          <div style={styles.field}>
            <label style={styles.label}>商品代碼</label>
            <input style={styles.input} value={form.item_id} disabled={!!editId}
              onChange={e => setForm({ ...form, item_id: e.target.value })} />
          </div>
          <div style={styles.field}>
            <label style={styles.label}>商品名稱</label>
            <input style={styles.input} value={form.item_name}
              onChange={e => setForm({ ...form, item_name: e.target.value })} />
          </div>
          <div style={styles.field}>
            <label style={styles.label}>主供應商</label>
            <select style={styles.input} value={form.fact_code}
              onChange={e => setForm({ ...form, fact_code: e.target.value })}>
              <option value="">-- 請選擇 --</option>
              {facts.map(f => <option key={f.fact_id} value={f.fact_id}>{f.fact_id} {f.fact_name}</option>)}
            </select>
          </div>
          <button style={styles.btn} onClick={handleSave}>{editId ? '儲存修改' : '確認新增'}</button>
        </div>
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>商品代碼</th>
              <th style={styles.th}>商品名稱</th>
              <th style={styles.th}>主供應商</th>
              <th style={styles.th}>操作</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(row => (
              <tr key={row.item_id}>
                <td style={styles.td}>{row.item_id}</td>
                <td style={styles.td}>{row.item_name}</td>
                <td style={styles.td}>{row.fact_code}</td>
                <td style={styles.td}>
                  <button style={{ ...styles.btn, marginRight: '8px' }} onClick={() => handleEdit(row)}>修改</button>
                  <button style={{ ...styles.btn, background: '#ff4d4f' }} onClick={() => handleDelete(row.item_id)}>刪除</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: '100vh', background: '#f0f2f5' },
  header: { display: 'flex', alignItems: 'center', gap: '16px', padding: '16px 32px', background: '#1677ff', color: '#fff' },
  backBtn: { padding: '6px 12px', background: '#fff', color: '#1677ff', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  body: { padding: '24px 32px' },
  toolbar: { display: 'flex', gap: '8px', marginBottom: '16px' },
  formBox: { display: 'flex', gap: '16px', alignItems: 'flex-end', background: '#fff', padding: '16px', borderRadius: '8px', marginBottom: '16px', flexWrap: 'wrap' },
  field: { display: 'flex', flexDirection: 'column', gap: '4px' },
  label: { fontSize: '12px', color: '#666' },
  input: { padding: '6px 10px', border: '1px solid #d9d9d9', borderRadius: '4px', fontSize: '14px', minWidth: '140px' },
  btn: { padding: '6px 16px', background: '#1677ff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  table: { width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: '8px' },
  th: { padding: '12px', background: '#fafafa', borderBottom: '1px solid #f0f0f0', textAlign: 'left' },
  td: { padding: '12px', borderBottom: '1px solid #f0f0f0' },
  msg: { padding: '8px 16px', background: '#f6ffed', border: '1px solid #b7eb8f', borderRadius: '4px', marginBottom: '12px', color: '#52c41a' },
};
