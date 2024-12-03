import React from 'react';
import { useNavigate } from "react-router-dom"
import './sidebar.css';

const Sidebar = () => {
    const navigate = useNavigate();

    const homePage = () => {
        navigate("/")
    }
    // const labsPage = () => {
    //     navigate("/labs")
    // }
    // const medsPage = () => {
    //     navigate("/meds")
    // }
    // const msgsPage = () => {
    //     navigate("/msgs")
    // }
    return (
        <div className = "sidebar">
            <div className = "sidebar-content">
                <button onClick={homePage}>Home</button>
                {/* <button onClick={labsPage}>Labs</button>
                <button onClick={medsPage}>Medication</button>
                <button onClick={msgsPage}>Messages</button> */}
            </div>
        </div>
    );
};

export default Sidebar;