import React, { useEffect, useState } from 'react'
import Profiles from './Profiles';
import CSS from 'csstype'
import {ClipLoader} from 'react-spinners'

type Props = {
    handleClickPanelChange: any
}

function Leaderboard(props: Props) {

    const [isWeekly, setWeekly] = useState(true)
    const [usersByWeekly, setUsersByWeekly] = useState([{}])
    const [usersByTotal, setUsersByTotal] = useState([{}])
    const [loading, setLoading] = useState(false)


    useEffect(() => {
        setLoading(true);
        fetch("/all_users").then(
            res => res.json()
        ).then(
            users => {
                setUsersByWeekly(JSON.parse(users.weekly))
                setUsersByTotal(JSON.parse(users.total))
                console.log(users)
                setLoading(false)
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

        {loading ? <ClipLoader css={"margin-top: 5%;"} color={'#000000'} loading={loading} size={50} ></ClipLoader> : <Profiles isWeekly={isWeekly} users={isWeekly ? usersByWeekly : usersByTotal} handleClickPanelChange={props.handleClickPanelChange}></Profiles>}
        </div>
    )

}

export default Leaderboard;

const buttonStylePressed: CSS.Properties = {
    backgroundColor: "#2C3131", color: "#F3F3F2"
}

const buttonStyleNotPressed: CSS.Properties = {
    color: "#2C3131", backgroundColor: "#F3F3F2"
}