import {Router, Request, Response} from 'express';
import multer from 'multer';
import { v4 as uuidv4 } from 'uuid';
import {redis} from "../lib/redis";
import axios from 'axios';
import FormData from 'form-data';


const csvRouter = Router();

//metler suetup for memory storage
const storage = multer.memoryStorage();
const upload = multer({storage});

csvRouter.get('/', (req, res) => {res.send({title: 'csv apis!'})});

csvRouter.post('/upload', upload.single("file"), async (req: Request, res: Response) => {

  console.log('Uploaded file:', req.file);
  const contents = req.file?.buffer.toString("utf-8");
  const uuid: string = uuidv4();
  await redis.setex(`wrap:${uuid}`, 60*60*24*30, contents);

  const formData = new FormData();
  formData.append('file', req.file?.buffer, req.file?.originalname);

  const fastAPIresponse = await axios.post('http://127.0.0.1:8000/parse-csv', formData, {
    headers: formData.getHeaders(),
  });

  //save stats in redis
  await redis.setex(`wrap:${uuid}:stats`, 60*60*24*30, JSON.stringify(fastAPIresponse.data));

  res.status(200).json({ message: 'File received!', id: uuid, processorResponse: fastAPIresponse.data});  
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