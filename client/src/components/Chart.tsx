import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    TimeScale
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Bar } from 'react-chartjs-2';
import { UsageData } from '../types/types';


ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    TimeScale
);

interface BarChartProps {
    data: UsageData[];
}

const BarChart: React.FC<BarChartProps> = ({ data }) => {
    const calculateCreditsPerDate = () => {
        const creditsPerDateMap = new Map<string, number>();

        data.forEach((item) => {
            const date = item.timestamp.split('T')[0];
            if (creditsPerDateMap.has(date)) {
                creditsPerDateMap.set(date, creditsPerDateMap.get(date)! + item.creditsUsed);
            } else {
                creditsPerDateMap.set(date, item.creditsUsed);
            }
        });

        const chartData = Array.from(creditsPerDateMap, ([date, credits]) => ({ date, credits }));
        return chartData;
    };

    const chartData = calculateCreditsPerDate();
    const dates = chartData.map((item) => item.date);

    const dataObject = {
        labels: dates,
        datasets: [
            {
                label: 'Credits Consumed',
                backgroundColor: 'rgba(75,192,192,0.2)',
                borderColor: 'rgba(75,192,192,1)',
                borderWidth: 1,
                hoverBackgroundColor: 'rgba(75,192,192,0.4)',
                hoverBorderColor: 'rgba(75,192,192,1)',
                data: chartData.map((item) => item.credits),
            },
        ],
    };

    return (
        <div>
            <h2>Credits Consumed Per Day</h2>
            <div style={{ height: '600px', width: '100%' }}>
                <Bar
                    data={dataObject}
                    options={{
                        scales: {
                            x: {
                                type: 'time',
                                time: {
                                    unit: 'day',
                                    tooltipFormat: 'P',
                                },
                                title: {
                                    display: true,
                                    text: 'Date',
                                },
                            },
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Credits Used',
                                },
                            },
                        },
                    }}
                />
            </div>
        </div>
    );
};

export default BarChart;
