import CrudPage from './CrudPage';

const fields = [
  { key: 'fact_id',   label: '廠商代碼' },
  { key: 'fact_name', label: '廠商名稱' },
  { key: 'remark',    label: '備註說明' },
];

export default function FactPage() {
  return <CrudPage title="廠商資料維護" endpoint="fact" fields={fields} idField="fact_id" />;
}
