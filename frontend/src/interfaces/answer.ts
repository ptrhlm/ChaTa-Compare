export interface IAnswer {
    id: number | null;

    // Only one of these is present at time
    decision: number | null;
    score: number | null;
}
