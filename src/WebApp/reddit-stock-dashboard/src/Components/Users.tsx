import React, { useEffect } from 'react'
import './comp-styles/Users-style.css'
import './comp-styles/bulma-input.scss'
import { useState } from 'react'
import UserInfo from './UserInfo'
import { ClipLoader } from 'react-spinners'


type Props = {
    user: string
    handleClickPanelChange: any
}

export class User {
    name: string;
    weekly_score: number;
    total_score: number;
    stocks: Array<any>;
    weekly_performance: Array<{x: number, y: number}>;
    all_time_performance: Array<{x: number, y: number}>;

    constructor() {
        this.name = "None";
        this.weekly_score = 0;
        this.total_score = 0;
        this.stocks = []
        this.weekly_performance = []
        this.all_time_performance = []
    }
}

function Users(props: Props) {

    //const [text, setText] = useState("");
    const [currentUser, setCurrentUser] = useState(new User())
    const [loading, setLoading] = useState(false)

    const getUserInfo = (text: string) => {
        setLoading(true)
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
                    temp.weekly_performance = JSON.parse(user['weekly_history']);
                    temp.all_time_performance = JSON.parse(user['total_history']);
                    temp.stocks = JSON.parse(user['relevant_comments']);
                    console.log(temp.name);
                    setCurrentUser(temp);
                    setLoading(false);
                }
                else {
                    setLoading(false);
                    setCurrentUser(new User());
                }
            }
        )
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
        return <UserInfo userInfo={userInfo} handleClickPanelChange={props.handleClickPanelChange}></UserInfo>
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
                    loading ? <ClipLoader css={"margin-top: 5%;"} color={'#000000'} loading={loading} size={50} ></ClipLoader> : showUserInfo(currentUser)
                }
            </div>
        </div>
    )
}

export default Users