import {Router} from 'express';
import multer from 'multer';
import { v4 as uuidv4 } from 'uuid';
import {redis} from "../lib/redis";



const csvRouter = Router();

//metler suetup for memory storage
const storage = multer.memoryStorage();
const upload = multer({storage});

csvRouter.get('/', (req, res) => {res.send({title: 'csv apis!'})});

csvRouter.post('/upload', upload.single("file"), async (req, res) => {

  console.log('Uploaded file:', req.file);
  const contents = req.file?.buffer.toString("utf-8");
  const uuid: string = uuidv4();
  await redis.setex(`wrap:${uuid}`, 60*60*24*30, contents);
  res.status(200).json({ message: 'File received!', id: uuid});  
});

csvRouter.get('/data/:id', async (req, res) => {
  const {id} = req.params;
  const data = await redis.get<string>(`wrap:${id}`);
  if(data == null){
    return res.status(404).send("No file found in database.");
  }
  res.send(data);
});

export default csvRouter;