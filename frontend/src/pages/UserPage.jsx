import CrudPage from './CrudPage';

const fields = [
  { key: 'user_id',   label: '用戶代碼' },
  { key: 'user_name', label: '用戶名稱' },
  { key: 'pw',        label: '用戶密碼' },
];

export default function UserPage() {
  return <CrudPage title="用戶資料維護" endpoint="user" fields={fields} idField="user_id" />;
}
