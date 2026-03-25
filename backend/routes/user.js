const express = require('express');
const router = express.Router();
const { pool, poolConnect, sql } = require('../config/db');

router.get('/', async (req, res) => {
  const { q } = req.query;
  await poolConnect;
  let query = 'SELECT user_id, user_name, pw FROM [user]';
  if (q) query += ` WHERE user_id LIKE @q OR user_name LIKE @q`;
  query += ' ORDER BY user_id';
  const request = pool.request();
  if (q) request.input('q', sql.NVarChar, `%${q}%`);
  const result = await request.query(query);
  res.json(result.recordset);
});

router.post('/', async (req, res) => {
  const { user_id, user_name, pw } = req.body;
  await poolConnect;
  await pool.request()
    .input('user_id', sql.VarChar, user_id)
    .input('user_name', sql.NVarChar, user_name)
    .input('pw', sql.VarChar, pw)
    .query('INSERT INTO [user] VALUES (@user_id,@user_name,@pw)');
  res.json({ message: '新增成功' });
});

router.put('/:id', async (req, res) => {
  const { user_name, pw } = req.body;
  await poolConnect;
  await pool.request()
    .input('user_id', sql.VarChar, req.params.id)
    .input('user_name', sql.NVarChar, user_name)
    .input('pw', sql.VarChar, pw)
    .query('UPDATE [user] SET user_name=@user_name, pw=@pw WHERE user_id=@user_id');
  res.json({ message: '修改成功' });
});

router.delete('/:id', async (req, res) => {
  await poolConnect;
  await pool.request()
    .input('user_id', sql.VarChar, req.params.id)
    .query('DELETE FROM [user] WHERE user_id=@user_id');
  res.json({ message: '刪除成功' });
});

module.exports = router;
