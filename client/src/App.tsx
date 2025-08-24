import { useState, useRef, useEffect } from 'react';
import './index.css';


function App() {
  const [file, setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [output, setOutput] = useState<any | null>(null);
  const [wrapId, setWrapId] = useState<string | null>(null);


  const handleUpload = async() => {
    // console.log("inhere");
    if(file==null) return;

    const formData = new FormData();
    formData.append("file", file);

    try{
      const response = await fetch("http://localhost:3001/api/v1/csv/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      setWrapId(result.id); // save uuid here
    }catch(err){
      console.log(err);
    }
  }

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  useEffect(() => {
    if(file==null) return;
    // console.log("calling function to upload");
    handleUpload();

  }, [file])

  useEffect(() =>{
    if(wrapId==null) return;
    
    const fetchData = async () =>{
      const res = await fetch(`http://localhost:3001/api/v1/csv/data/${wrapId}`);
      const text = await res.json();
      setOutput(text);
    }

    fetchData();

  }, [wrapId]);

  
  return (

      <div className="flex flex-col items-center pt-5">

        <h1 className='text-center font-bold text-3xl pt-8 pb-8 font-header'>Goodreads Wrapped</h1>

        {output === null &&
        <div className='border-3 rounded-md border-toast size-40 hover:cursor-pointer' onClick={triggerFileInput}>

          <input type="file" ref={fileInputRef} accept=".csv, text/csv" style={{ display: 'none' }}
          onChange={(e) => {
          if (e.target.files && e.target.files.length > 0) {
            setFile(e.target.files[0]);}}}/>

          {!fileInputRef.current&& (
            <p className='text-center pt-15 font-body'>click to upload csv</p>
          )}
        
        </div>}

        {output !== null &&
          <div>
            <p>{JSON.stringify(output, null, 2)}</p>
          </div>
        }

      </div> 
  )

}

export default App
