const express = require('express');
const router = express.Router();
const { pool, poolConnect, sql } = require('../config/db');

router.get('/', async (req, res) => {
  const { q } = req.query;
  await poolConnect;
  let query = 'SELECT cust_id, cust_name, remark FROM cust';
  if (q) query += ` WHERE cust_id LIKE @q OR cust_name LIKE @q`;
  query += ' ORDER BY cust_id';
  const request = pool.request();
  if (q) request.input('q', sql.NVarChar, `%${q}%`);
  const result = await request.query(query);
  res.json(result.recordset);
});

router.post('/', async (req, res) => {
  const { cust_id, cust_name, remark } = req.body;
  await poolConnect;
  await pool.request()
    .input('cust_id', sql.VarChar, cust_id)
    .input('cust_name', sql.NVarChar, cust_name)
    .input('remark', sql.NVarChar, remark)
    .query('INSERT INTO cust VALUES (@cust_id,@cust_name,@remark)');
  res.json({ message: '新增成功' });
});

router.put('/:id', async (req, res) => {
  const { cust_name, remark } = req.body;
  await poolConnect;
  await pool.request()
    .input('cust_id', sql.VarChar, req.params.id)
    .input('cust_name', sql.NVarChar, cust_name)
    .input('remark', sql.NVarChar, remark)
    .query('UPDATE cust SET cust_name=@cust_name, remark=@remark WHERE cust_id=@cust_id');
  res.json({ message: '修改成功' });
});

router.delete('/:id', async (req, res) => {
  await poolConnect;
  await pool.request()
    .input('cust_id', sql.VarChar, req.params.id)
    .query('DELETE FROM cust WHERE cust_id=@cust_id');
  res.json({ message: '刪除成功' });
});

module.exports = router;
