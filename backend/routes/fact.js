const express = require('express');
const router = express.Router();
const { pool, poolConnect, sql } = require('../config/db');

router.get('/', async (req, res) => {
  const { q } = req.query;
  await poolConnect;
  let query = 'SELECT fact_id, fact_name, remark FROM fact';
  if (q) query += ` WHERE fact_id LIKE @q OR fact_name LIKE @q`;
  query += ' ORDER BY fact_id';
  const request = pool.request();
  if (q) request.input('q', sql.NVarChar, `%${q}%`);
  const result = await request.query(query);
  res.json(result.recordset);
});

router.post('/', async (req, res) => {
  const { fact_id, fact_name, remark } = req.body;
  await poolConnect;
  await pool.request()
    .input('fact_id', sql.VarChar, fact_id)
    .input('fact_name', sql.NVarChar, fact_name)
    .input('remark', sql.NVarChar, remark)
    .query('INSERT INTO fact VALUES (@fact_id,@fact_name,@remark)');
  res.json({ message: '新增成功' });
});

router.put('/:id', async (req, res) => {
  const { fact_name, remark } = req.body;
  await poolConnect;
  await pool.request()
    .input('fact_id', sql.VarChar, req.params.id)
    .input('fact_name', sql.NVarChar, fact_name)
    .input('remark', sql.NVarChar, remark)
    .query('UPDATE fact SET fact_name=@fact_name, remark=@remark WHERE fact_id=@fact_id');
  res.json({ message: '修改成功' });
});

router.delete('/:id', async (req, res) => {
  await poolConnect;
  await pool.request()
    .input('fact_id', sql.VarChar, req.params.id)
    .query('DELETE FROM fact WHERE fact_id=@fact_id');
  res.json({ message: '刪除成功' });
});

module.exports = router;
