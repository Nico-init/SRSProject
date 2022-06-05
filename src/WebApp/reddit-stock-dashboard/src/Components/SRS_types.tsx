export class Comment {
    comment_id: number;
    user_id: string;
    comment_value: boolean;
    realiability: number;
    stock_name: string;
    stock_value: number;
    date: string;

    constructor() {
        this.comment_id = 0;
        this.user_id = "None";
        this.comment_value = false;
        this.realiability = 0;
        this.stock_name = "";
        this.stock_value = 0;
        this.date = ""
    }
}

export class User {
    name: string;
    weekly_score: number;
    total_score: number;
    stocks: Array<Comment>;
    weekly_performance: Array<number>;
    all_time_performance: Array<number>;

    constructor() {
        this.name = "None";
        this.weekly_score = 0;
        this.total_score = 0;
        this.stocks = [new Comment()]
        this.weekly_performance = []
        this.all_time_performance = []
    }
}