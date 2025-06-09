import express from 'express';
import { Router } from 'express';

const router: Router = express.Router();

// Health check route
router.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

export default router;
