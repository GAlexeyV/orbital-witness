import ReactDOM from 'react-dom';
import React from 'react';
import './index.css';
import App from './App';

const rootElement = document.getElementById('root');

if (rootElement) {
    // @ts-ignore
    const root = ReactDOM.createRoot(rootElement);
    root.render(
        <React.StrictMode>
            <App />
        </React.StrictMode>
    );
} else {
    throw new Error("Unable to find root element with id 'root'");
}
