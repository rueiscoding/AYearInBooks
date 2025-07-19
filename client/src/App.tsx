import { useState, useRef } from 'react';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFile(file);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };


  return (

      <div className="flex flex-col items-center">

        <h1 className='text-center font-bold text-3xl pt-8 pb-8'>Goodreads Wrapped</h1>
        <div className='border-3 rounded-md border-black size-40 hover:cursor-pointer' onClick={triggerFileInput}>

          {!fileInputRef.current&& (
            <p className='text-center pt-15'>click to upload</p>
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
