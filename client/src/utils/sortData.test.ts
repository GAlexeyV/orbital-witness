import { compareValues, sortData } from './sortData';
import { UsageData, SortDict } from '../types/types';

describe('compareValues', () => {
    it('should return 1 when valueA is undefined and valueB is defined', () => {
        expect(compareValues({ valueA: undefined, valueB: 10, direction: 'asc' })).toBe(1);
    });

    it('should return -1 when valueB is undefined and valueA is defined', () => {
        expect(compareValues({ valueA: 10, valueB: undefined, direction: 'asc' })).toBe(-1);
    });

    it('should return 0 when both values are undefined', () => {
        expect(compareValues({ valueA: undefined, valueB: undefined, direction: 'asc' })).toBe(0);
    });

    it('should correctly compare numbers in ascending order', () => {
        expect(compareValues({ valueA: 10, valueB: 20, direction: 'asc' })).toBe(-1);
        expect(compareValues({ valueA: 20, valueB: 10, direction: 'asc' })).toBe(1);
        expect(compareValues({ valueA: 10, valueB: 10, direction: 'asc' })).toBe(0);
    });

    it('should correctly compare numbers in descending order', () => {
        expect(compareValues({ valueA: 10, valueB: 20, direction: 'desc' })).toBe(1);
        expect(compareValues({ valueA: 20, valueB: 10, direction: 'desc' })).toBe(-1);
        expect(compareValues({ valueA: 10, valueB: 10, direction: 'desc' })).toBe(0);
    });

    it('should correctly compare strings in ascending order', () => {
        expect(compareValues({ valueA: 'a', valueB: 'b', direction: 'asc' })).toBe(-1);
        expect(compareValues({ valueA: 'b', valueB: 'a', direction: 'asc' })).toBe(1);
        expect(compareValues({ valueA: 'a', valueB: 'a', direction: 'asc' })).toBe(0);
    });

    it('should correctly compare dates in ascending order', () => {
        const date1 = new Date('2021-01-01');
        const date2 = new Date('2022-01-01');
        expect(compareValues({ valueA: date1, valueB: date2, direction: 'asc' })).toBe(-1);
        expect(compareValues({ valueA: date2, valueB: date1, direction: 'asc' })).toBe(1);
        expect(compareValues({ valueA: date1, valueB: date1, direction: 'asc' })).toBe(0);
    });
});

describe('sortData', () => {
    const data: UsageData[] = [
        { messageId: 1, timestamp: '2021-01-01T00:00:00Z', reportName: 'Report A', creditsUsed: 100 },
        { messageId: 2, timestamp: '2020-01-01T00:00:00Z', reportName: 'Report B', creditsUsed: 200 },
        { messageId: 3, timestamp: '2022-01-01T00:00:00Z', reportName: 'Report C', creditsUsed: 50 }
    ];

    it('should sort data by a single column in ascending order', () => {
        const sortConfigs: SortDict = { creditsUsed: 'asc' };
        const sortedData = sortData(data, sortConfigs);
        expect(sortedData[0].messageId).toBe(3);
        expect(sortedData[1].messageId).toBe(1);
        expect(sortedData[2].messageId).toBe(2);
    });

    it('should sort data by a single column in descending order', () => {
        const sortConfigs: SortDict = { creditsUsed: 'desc' };
        const sortedData = sortData(data, sortConfigs);
        expect(sortedData[0].messageId).toBe(2);
        expect(sortedData[1].messageId).toBe(1);
        expect(sortedData[2].messageId).toBe(3);
    });

    it('should sort data by multiple columns', () => {
        const sortConfigs: SortDict = { reportName: 'asc', timestamp: 'desc' };
        const sortedData = sortData(data, sortConfigs);
        expect(sortedData[0].messageId).toBe(1);
        expect(sortedData[1].messageId).toBe(2);
        expect(sortedData[2].messageId).toBe(3);
    });

    it('should handle empty sort configuration', () => {
        const sortConfigs: SortDict = {};
        const sortedData = sortData(data, sortConfigs);
        expect(sortedData).toEqual(data);
    });
});
