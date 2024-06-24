import React, { useMemo } from 'react';
import {
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TableSortLabel,
} from '@mui/material';
import { format } from 'date-fns';
import { UsageData, Column } from '../types/types';
import { useSorting } from '../utils/useSorting';
import { sortData } from '../utils/sortData';

interface TableProps {
    data: UsageData[];
}

const columns: Array<{
    key: keyof UsageData;
    label: string;
    isSortable?: boolean;
}> = [
    { key: 'messageId', label: 'Message ID' },
    { key: 'timestamp', label: 'Timestamp' },
    { key: 'reportName', label: 'Report Name', isSortable: true },
    { key: 'creditsUsed', label: 'Credits Used', isSortable: true },
];

const UsageTable: React.FC<TableProps> = ({ data }) => {
    const { allSorts, stepSortingForColumn } = useSorting();

    const getSortProps = (column: Column) => {
        const direction = allSorts[column];
        return {
            active: Boolean(direction),
            direction: direction as 'asc' | 'desc' | undefined,
        };
    };

    const sortedData = useMemo(() => sortData(data, allSorts), [data, allSorts]);

    const formatTimestamp = (timestamp: string) => {
        const date = new Date(timestamp);
        return format(date, 'dd-MM-yyyy HH:mm');
    };

    return (
        <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        {columns.map(({ key, label, isSortable }) => (
                            <TableCell key={key}>
                                {isSortable ? (
                                    <TableSortLabel
                                        {...getSortProps(key as Column)}
                                        onClick={() => stepSortingForColumn(key as Column)}
                                    >
                                        {label}
                                    </TableSortLabel>
                                ) : (
                                    label
                                )}
                            </TableCell>
                        ))}
                    </TableRow>
                </TableHead>
                <TableBody>
                    {sortedData.map((item) => (
                        <TableRow key={item.messageId}>
                            <TableCell>{item.messageId}</TableCell>
                            <TableCell>{formatTimestamp(item.timestamp)}</TableCell>
                            <TableCell>{item.reportName}</TableCell>
                            <TableCell>{item.creditsUsed !== undefined ? item.creditsUsed.toFixed(2) : ''}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default UsageTable;
