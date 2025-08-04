import express from 'express';
import cors from 'cors';
import multer from 'multer';
import csvRouter from './routes/upload.routes';


const app = express();
const port = 3001;

// Enable CORS (allow requests from frontend)
app.use(cors({origin:"*", methods:["POST"]}));
app.use(express.json());
app.use('/api/v1/csv', csvRouter);

// Setup multer for file uploads
// const upload = multer({ dest: 'uploads/' });

app.get('/', (req, res) => {
    res.send('Welcome to goodreads wrapped api');
});

// app.get('/wrapped/:id', (req, res) => {
//   const { id } = req.params;
//   res.json({ message: `Returning wrapped data for ID: ${id}` });
// });

app.listen(port, () => {
  console.log(`🚀 Server is running at http://localhost:${port}`);
});
