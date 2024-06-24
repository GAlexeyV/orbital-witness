import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Column, SortOrder, SortDict } from "../types/types";

const toSortDict = (sortString: string | null): SortDict => {
    if (!sortString || sortString.length === 0) {
        return {};
    }

    return Object.fromEntries(
        sortString.split(",").map((sortStr) => {
            const [column, direction] = sortStr.split(":");
            return [column, direction as SortOrder];
        })
    );
};

const toSortString = (sortDict: SortDict): string =>
    Object.entries(sortDict)
        .map(([col, dir]) => (col && dir ? `${col}:${dir}` : undefined))
        .filter(Boolean)
        .join(",");

export const getNextDirection = (direction: SortOrder | undefined): SortOrder => {
    if (!direction) {
        return "asc";
    }
    if (direction === "asc") {
        return "desc";
    }
    return '';
};

export const useSorting = (): {
    allSorts: SortDict;
    stepSortingForColumn: (column: Column) => void;
} => {
    const location = useLocation();
    const navigate = useNavigate();
    const [sortString, setSortString] = useState(() => new URLSearchParams(location.search).get("sort"));

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        setSortString(params.get("sort"));
    }, [location.search]);

    const allSorts = toSortDict(sortString);

    const stepSortingForColumn = (column: Column) => {
        const nextDirection = getNextDirection(allSorts[column]);
        const newSorts = { ...allSorts, [column]: nextDirection };

        const newSortString = toSortString(newSorts);
        const params = new URLSearchParams(location.search);
        if (newSortString) {
            params.set("sort", newSortString);
        } else {
            params.delete("sort");
        }

        navigate({ search: params.toString() });

    };

    return { allSorts, stepSortingForColumn };
};

