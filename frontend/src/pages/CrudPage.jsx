import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

export default function CrudPage({ title, endpoint, fields, idField }) {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [search, setSearch] = useState('');
  const [form, setForm] = useState({});
  const [editId, setEditId] = useState(null);
  const [msg, setMsg] = useState('');

  const load = async (q = '') => {
    const res = await api.get(`/${endpoint}`, { params: q ? { q } : {} });
    setRows(res.data);
  };

  useEffect(() => { load(); }, []);

  const showMsg = (m) => { setMsg(m); setTimeout(() => setMsg(''), 2000); };

  const handleSave = async () => {
    try {
      if (editId) {
        await api.put(`/${endpoint}/${editId}`, form);
        showMsg('修改成功');
      } else {
        await api.post(`/${endpoint}`, form);
        showMsg('新增成功');
      }
      setForm({});
      setEditId(null);
      load(search);
    } catch (e) {
      showMsg(e.response?.data?.message || '操作失敗');
    }
  };

  const handleEdit = (row) => {
    setEditId(row[idField]);
    setForm({ ...row });
  };

  const handleDelete = async (id) => {
    if (!window.confirm('確定刪除？')) return;
    await api.delete(`/${endpoint}/${id}`);
    showMsg('刪除成功');
    load(search);
  };

  const handleNew = () => { setEditId(null); setForm({}); };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <button style={styles.backBtn} onClick={() => navigate('/main')}>← 返回</button>
        <h2 style={{ margin: 0 }}>{title}</h2>
      </div>

      <div style={styles.body}>
        {/* 查詢 */}
        <div style={styles.toolbar}>
          <input style={styles.input} placeholder="查詢..." value={search}
            onChange={e => setSearch(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && load(search)} />
          <button style={styles.btn} onClick={() => load(search)}>查詢</button>
          <button style={{ ...styles.btn, background: '#52c41a' }} onClick={handleNew}>新增</button>
        </div>

        {msg && <div style={styles.msg}>{msg}</div>}

        {/* 表單 */}
        <div style={styles.formBox}>
          {fields.map(f => (
            <div key={f.key} style={styles.field}>
              <label style={styles.label}>{f.label}</label>
              <input style={styles.input}
                value={form[f.key] || ''}
                disabled={f.key === idField && !!editId}
                onChange={e => setForm({ ...form, [f.key]: e.target.value })} />
            </div>
          ))}
          <button style={styles.btn} onClick={handleSave}>{editId ? '儲存修改' : '確認新增'}</button>
        </div>

        {/* 清單 */}
        <table style={styles.table}>
          <thead>
            <tr>{fields.map(f => <th key={f.key} style={styles.th}>{f.label}</th>)}
              <th style={styles.th}>操作</th></tr>
          </thead>
          <tbody>
            {rows.map(row => (
              <tr key={row[idField]}>
                {fields.map(f => <td key={f.key} style={styles.td}>{row[f.key]}</td>)}
                <td style={styles.td}>
                  <button style={{ ...styles.btn, marginRight: '8px' }} onClick={() => handleEdit(row)}>修改</button>
                  <button style={{ ...styles.btn, background: '#ff4d4f' }} onClick={() => handleDelete(row[idField])}>刪除</button>
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
  table: { width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: '8px', overflow: 'hidden' },
  th: { padding: '12px', background: '#fafafa', borderBottom: '1px solid #f0f0f0', textAlign: 'left' },
  td: { padding: '12px', borderBottom: '1px solid #f0f0f0' },
  msg: { padding: '8px 16px', background: '#f6ffed', border: '1px solid #b7eb8f', borderRadius: '4px', marginBottom: '12px', color: '#52c41a' },
};
