export type UsageData = {
    messageId: number;
    timestamp: string;
    reportName?: string;
    creditsUsed: number;
};

export type UsageResponse = {
    message_id: number;
    timestamp: string;
    report_name?: string;
    credits_used: number;
};

export type Column = 'reportName' | 'creditsUsed';

export type SortOrder = 'asc' | 'desc' | '';

export interface SortDict {
    [field: string]: SortOrder;
}