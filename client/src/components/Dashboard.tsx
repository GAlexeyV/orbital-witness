import React, { useEffect, useState } from 'react';
import Table from './Table';
import BarChart from './Chart';
import { fetchData } from '../api/usageApi';
import { UsageData } from '../types/types';

const Dashboard: React.FC = () => {
    const [data, setData] = useState<UsageData[]>([]);

    useEffect(() => {
        const getData = async () => {
            const usageData = await fetchData();
            setData(usageData);
        };

        getData();
    }, []);

    return (
        <div style={{ margin: '100px' }}>
            <h1>Credit Usage Dashboard</h1>

            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <div style={{ width: 'calc(100% - 200px)', margin: '20px' }}>
                    <BarChart data={data} />
                </div>
                <div style={{ width: 'calc(100% - 200px)', marginTop: '20px'  }}>
                    <Table data={data} />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;



