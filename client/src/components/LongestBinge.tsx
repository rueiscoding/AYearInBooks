import React from "react";
import { Book } from "./types";
import '../index.css';


export default function LongestBinge({ reads }: { reads: Book[] }) {

    
    return(
        <div className="">
            <div className="font-body">longest binge session (in days)</div>
            <div className = "font-header text-3xl">{reads.length}</div>
        </div>
    );
}
