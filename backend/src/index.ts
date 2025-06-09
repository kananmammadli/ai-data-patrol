import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import indexRouter from './routes';
import checksRouter from './routes/checks';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Routes
app.use('/', indexRouter);
app.use('/api/checks', checksRouter);

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
