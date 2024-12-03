import React, { useState } from "react";
import React, { useState } from 'react';
import axios from 'axios';
import "./home.css";

const apiUrl = 'http://localhost:4000';

function Home() {
    const [blockValues, setBlockValues] = useState([]);

    useEffect(() => {
        fetchBlockValues().then(setBlockValues);
    }, []);

    return (
        <div>
            <h1>Block Values</h1>
            <ul>
                {blockValues.map((block, index) => (
                    <li key={index}>{JSON.stringify(block)}</li>
                ))}
            </ul>
        </div>
    );
}