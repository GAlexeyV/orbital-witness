import axios from 'axios';
import {UsageData, UsageResponse} from "../types/types"


export const fetchData = async (): Promise<UsageData[]> => {
    try {
        const response = await axios.get<{ usage: UsageResponse[] }>('http://0.0.0.0:8000/usage'); // Replace with your API URL

        const data = response.data.usage.map((usageResponse) => toUsageData(usageResponse));
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return [];
    }
};

const toUsageData = ({
                     message_id,
                     timestamp,
                     report_name,
                     credits_used,
                 }: UsageResponse): UsageData => ({
    messageId: message_id,
    timestamp: timestamp,
    reportName: report_name,
    creditsUsed: credits_used,
});
