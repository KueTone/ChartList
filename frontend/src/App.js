import React, { useState, useEffect } from "react";
import { fetchBlockValues } from "./services/api";

function App() {
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

export default App;
