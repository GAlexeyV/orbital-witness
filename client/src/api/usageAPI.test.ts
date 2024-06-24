import axios from 'axios';
import { fetchData } from './usageApi';
import { UsageData, UsageResponse } from '../types/types';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('fetchData', () => {
    it('should fetch and transform usage data correctly', async () => {
        const mockResponseData: { usage: UsageResponse[] } = {
            usage: [
                {
                    message_id: 123,
                    timestamp: '2023-01-01T00:00:00Z',
                    report_name: 'Report 1',
                    credits_used: 10,
                },
                {
                    message_id: 456,
                    timestamp: '2023-01-02T00:00:00Z',
                    report_name: 'Report 2',
                    credits_used: 20,
                },
            ],
        };

        mockedAxios.get.mockResolvedValueOnce({ data: mockResponseData });

        const result: UsageData[] = await fetchData();

        expect(result).toEqual([
            {
                messageId: 123,
                timestamp: '2023-01-01T00:00:00Z',
                reportName: 'Report 1',
                creditsUsed: 10,
            },
            {
                messageId: 456,
                timestamp: '2023-01-02T00:00:00Z',
                reportName: 'Report 2',
                creditsUsed: 20,
            },
        ]);

        expect(mockedAxios.get).toHaveBeenCalledWith('http://0.0.0.0:8000/usage');
    });

    it('should handle errors and return an empty array', async () => {
        mockedAxios.get.mockRejectedValueOnce(new Error('Network Error'));

        const result: UsageData[] = await fetchData();

        expect(result).toEqual([]);
        expect(mockedAxios.get).toHaveBeenCalledWith('http://0.0.0.0:8000/usage');
    });
});
