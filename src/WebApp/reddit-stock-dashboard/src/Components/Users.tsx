import React, { useEffect } from 'react'
import './comp-styles/Users-style.css'
import './comp-styles/bulma-input.scss'
import { useState } from 'react'
import UserInfo from './UserInfo'


type Props = {
    user: string
    //handleClickPanelChange: any
}

export class User {
    name: string;
    weekly_score: number;
    total_score: number;
    positive_stocks: Array<string>;
    negative_stocks: Array<string>;
    weekly_performance: Array<number>;
    all_time_performance: Array<number>;

    constructor() {
        this.name = "None";
        this.weekly_score = 0;
        this.total_score = 0;
        this.positive_stocks = []
        this.negative_stocks = []
        this.weekly_performance = []
        this.all_time_performance = []
    }
}

function Users(props: Props) {

    //const [text, setText] = useState("");
    const [currentUser, setCurrentUser] = useState(new User())

    const getUserInfo = (text: string) => {
        fetch("/user/"+text).then(
            res => res.json()
        ).then(
            user => {
                if (user !== "None") {
                    let u = JSON.parse(user['user']);
                    let temp = new User();
                    temp.name = u.user_id;
                    temp.weekly_score = u.weekly_score;
                    temp.total_score = u.total_score;
                    temp.weekly_performance = JSON.parse(user['weekly_history'])
                    temp.all_time_performance = JSON.parse(user['total_history'])
                    console.log(temp.name);
                    setCurrentUser(temp);
                }
                else {
                    setCurrentUser(new User())
                }
            }
        )
        return
    }

    const userCheck = () => {
        if(props.user) {
            //setText(props.user);
            getUserInfo(props.user);
        }

    }

    const handleSearch = (e: any) => {
        if(e.key === "Enter") {
            //setText(e.target.value);
            getUserInfo(e.target.value);
        }
    }

    const showUserInfo = (userInfo: User) => {
        return <UserInfo userInfo={userInfo}></UserInfo>
    }

    useEffect(userCheck, [props.user]); // LOADING USER WHEN COMING FROM LEADERBOARDS LINK

    return (
        <div className="panel">
            <div className="searchBar">
                <div className="control is-small">
                    <input className="input is-small is-rounded" type="text" placeholder="u/username" onKeyDown={handleSearch}>
                    </input>
                </div>
            </div>
            <div className="userInfo">
                {
                    showUserInfo(currentUser)
                }
            </div>
        </div>
    )
}

export default Users