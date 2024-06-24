import { UsageData } from '../types/types';
import { Column, SortOrder, SortDict } from '../types/types';

export const compareValues = ({
                                  valueA,
                                  valueB,
                                  direction,
                              }: {
    valueA?: string | number | Date;
    valueB?: string | number | Date;
    direction: SortOrder;
}) => {
    if (valueA === undefined && valueB !== undefined) {
        return 1;
    }
    if (valueB === undefined && valueA !== undefined) {
        return -1;
    }
    if (valueA === undefined && valueB === undefined) {
        return 0;
    }

    if (valueA! < valueB!) {
        return direction === "asc" ? -1 : 1;
    }
    if (valueA! > valueB!) {
        return direction === "asc" ? 1 : -1;
    }
    return 0;
};

export const sortData = (data: Array<UsageData>, sortConfigs: SortDict): UsageData[] => {
    return [...data].sort((usageA, usageB) => {
        for (const key in sortConfigs) {
            const direction = sortConfigs[key as Column];
            if (direction) {
                const valueA = usageA[key as keyof UsageData];
                const valueB = usageB[key as keyof UsageData];
                const comparison = compareValues({ valueA, valueB, direction });
                if (comparison !== 0) {
                    return comparison;
                }
            }
        }
        return 0;
    });
};




