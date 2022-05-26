import React, { useEffect, useState } from 'react'
import Profiles from './Profiles';
import CSS from 'csstype'

type Props = {
    DB: any,
    handleClickPanelChange: any
}

function Leaderboard(props: Props) {

    const [isWeekly, setWeekly] = useState(true)
    const [users, setUsers] = useState([{}]) // DATA FROM THE BACKEND

    useEffect(() => {
        fetch("/all_users").then(
            res => res.json()
        ).then(
            users => {
                setUsers(users["users"])
                console.log(users["users"])
            }
        )
    }, [])

    const handleClick = (e: any) => {
        if (e.target.dataset.id === "7") {
            setWeekly(true);
        }
        else if (e.target.dataset.id === "0") { 
            setWeekly(false);
        }
    }

    return (
        <div className="board">
        <h2 className="panelName">Leaderboard</h2>

        <div className="duration">
            <button style={isWeekly ? buttonStylePressed : buttonStyleNotPressed} onClick={handleClick} data-id='7'>Weekly</button>
            <button style={!isWeekly ? buttonStylePressed : buttonStyleNotPressed} onClick={handleClick} data-id='0'>All-Time</button>
        </div>

        <Profiles isWeekly={isWeekly} DB={sort(users, isWeekly)} handleClickPanelChange={props.handleClickPanelChange}></Profiles>

        </div>
    )

}

export default Leaderboard;

function sort(data: any, isWeekly: boolean) {
    return data.sort((a: any, b: any) => {
        if (isWeekly) {
            if ( a.w_score === b.w_score){
                return b.w_score - a.w_score;
            } else{
                return b.w_score - a.w_score;
            }
        }
        else {
            if ( a.at_score === b.at_score){
                return b.at_score - a.at_score;
            } else{
                return b.at_score - a.at_score;
            }
        }
    })
}

const buttonStylePressed: CSS.Properties = {
    backgroundColor: "#2C3131", color: "#F3F3F2"
}

const buttonStyleNotPressed: CSS.Properties = {
    color: "#2C3131", backgroundColor: "#F3F3F2"
}