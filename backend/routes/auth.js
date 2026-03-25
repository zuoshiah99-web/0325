const express = require('express');
const router = express.Router();
const { pool, poolConnect, sql } = require('../config/db');

// POST /api/auth/login
router.post('/login', async (req, res) => {
  const { user_id, pw } = req.body;
  try {
    await poolConnect;
    const result = await pool.request()
      .input('user_id', sql.VarChar, user_id)
      .input('pw', sql.VarChar, pw)
      .query('SELECT user_id, user_name FROM [user] WHERE user_id=@user_id AND pw=@pw');
    if (result.recordset.length === 0) {
      return res.status(401).json({ message: '帳號或密碼錯誤' });
    }
    res.json({ user: result.recordset[0] });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;
