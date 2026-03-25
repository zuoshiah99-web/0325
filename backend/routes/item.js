const express = require('express');
const router = express.Router();
const { pool, poolConnect, sql } = require('../config/db');

router.get('/', async (req, res) => {
  const { q } = req.query;
  await poolConnect;
  let query = 'SELECT item_id, item_name, fact_code FROM item';
  if (q) query += ` WHERE item_id LIKE @q OR item_name LIKE @q`;
  query += ' ORDER BY item_id';
  const request = pool.request();
  if (q) request.input('q', sql.NVarChar, `%${q}%`);
  const result = await request.query(query);
  res.json(result.recordset);
});

router.post('/', async (req, res) => {
  const { item_id, item_name, fact_code } = req.body;
  await poolConnect;
  await pool.request()
    .input('item_id', sql.VarChar, item_id)
    .input('item_name', sql.NVarChar, item_name)
    .input('fact_code', sql.VarChar, fact_code)
    .query('INSERT INTO item VALUES (@item_id,@item_name,@fact_code)');
  res.json({ message: '新增成功' });
});

router.put('/:id', async (req, res) => {
  const { item_name, fact_code } = req.body;
  await poolConnect;
  await pool.request()
    .input('item_id', sql.VarChar, req.params.id)
    .input('item_name', sql.NVarChar, item_name)
    .input('fact_code', sql.VarChar, fact_code)
    .query('UPDATE item SET item_name=@item_name, fact_code=@fact_code WHERE item_id=@item_id');
  res.json({ message: '修改成功' });
});

router.delete('/:id', async (req, res) => {
  await poolConnect;
  await pool.request()
    .input('item_id', sql.VarChar, req.params.id)
    .query('DELETE FROM item WHERE item_id=@item_id');
  res.json({ message: '刪除成功' });
});

module.exports = router;
