# A Year In Books (In Progress)
 is a full-stack web app that generates personalized, shareable reading summaries from your Goodreads data. Think Spotify Wrapped, but for books. Upload your Goodreads CSV export, and the app will analyze your reading patterns and generate interactive data visualizations you can share.

### Features (so far)
Year-End Summary – Total books, pages, top authors, and most-read months  
Easy Uploads – Drag-and-drop CSV file upload  
Fast Analysis – Python microservice processes and returns results  
Temporary Data Storage – Redis (Upstash) stores processed results for ~30 days

### Current Tech Stack
Frontend: TypeScript, React, Tailwind CSS  
Backend: Node.js, Express, Redis  
Microservice: Python, FastAPI, Pandas, MongoDB *(for caching enrichment data)*

### Status
*Pipeline: CSV upload → Node.js/Express server → Python microservice (parsing & analysis) → results returned to server → database storage & frontend display.*

**Built:** The full pipeline is functional. Frontend is currently minimal as focus is on enriching analytics and visualizations.  
**In progress:** Data enrichment in Python microservice via creative API/data source combinations.  
**Planned:** Interactive charts and 3D models, metadata analysis, shareable visual summaries

#### *Note on Data Enrichment*
The Goodreads CSV export contains only basic metadata (title, author, dates, and a few reading stats). Most external book APIs provide limited coverage or inconsistent data for enrichment. As a result, generating meaningful insights requires building creative heuristics. This process takes time, but it allows for more unique and personalized summaries beyond what raw Goodreads data or public APIs can offer.
