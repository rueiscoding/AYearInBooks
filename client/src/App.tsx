import { useState, useRef, useEffect } from 'react';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [wrapId, setWrapId] = useState<string | null>(null);


  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFile(file);
    }

  };

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
      const text = await res.text();
      console.log("CSV contents", text);
    }

    fetchData();

  }, [wrapId]);

  
  return (

      <div className="flex flex-col items-center">

        <h1 className='text-center font-bold text-3xl pt-8 pb-8'>Goodreads Wrapped</h1>
        <div className='border-3 rounded-md border-black size-40 hover:cursor-pointer' onClick={triggerFileInput}>

          {!fileInputRef.current&& (
            <p className='text-center pt-15'>click to upload csv</p>
          )}
        

          <input type="file" accept=".csv" ref={fileInputRef} onChange={handleFileChange} className="hidden"/>
          {file && (
            <p className="text-center pt-15">cooking your stats!</p>
          )}
        </div>

      </div> 
  )

}

export default App
