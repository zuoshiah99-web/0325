import CrudPage from './CrudPage';

const fields = [
  { key: 'cust_id',   label: '客戶代碼' },
  { key: 'cust_name', label: '客戶名稱' },
  { key: 'remark',    label: '備註說明' },
];

export default function CustPage() {
  return <CrudPage title="客戶資料維護" endpoint="cust" fields={fields} idField="cust_id" />;
}
