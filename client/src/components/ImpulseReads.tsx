import React from "react";
import { Book } from "./types";
import '../index.css';

export default function ImpulseReads({ reads }: { reads: Book[] }) {

    
    return(
        <div className="">
            <div className="font-body">books added tbr and read within a week!</div>
            <div className = "font-header text-3xl">{reads.length}</div>
        </div>
    );
}