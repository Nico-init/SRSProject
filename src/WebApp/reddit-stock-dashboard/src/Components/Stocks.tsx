import React, { useEffect, useState } from 'react'
import {Comment} from './SRS_types'

type Props = {
    stock_symbol: string
    handleClickPanelChange: any
}

function Stocks(props: Props) {
    const [stockName, setStockName] = useState("");
    const [info, setStockInfo] = useState([[new Comment()]])

    const stockCheck = () => {
        if(props.stock_symbol) {
            getStockInfo(props.stock_symbol);
            setStockName(props.stock_symbol);
        }
    }

    const handleSearch = (e: any) => {
        if(e.key === "Enter") {
            getStockInfo(e.target.value);
        }
    }

    const getStockInfo = (text: string) => {
        fetch("/stock/"+text).then(
            res => res.json()
        ).then(
            info => {
                console.log(info)
                if (info.length !== 0) {
                    console.log(info)
                    setStockInfo(info); 
                    setStockName(text);
                }
                else {
                    setStockInfo([]);
                    setStockName("The symbol doesn't exist or there are no commets yet...");
                }
            }
        )
        return
    }

    const handleClickUser = (user: string) => {
        props.handleClickPanelChange("Users", user)
    }

    useEffect(stockCheck, [props.stock_symbol]);

    return (
        <div className="panel">
                <div className="searchBar">
                    <div className="control is-small">
                        <input className="input is-small is-rounded" type="text" placeholder="u/username" onKeyDown={handleSearch}>
                        </input>
                    </div>
                </div>
                <div className="userInfo">
                    <div className='userBox'>
                    <br></br>
                    <div className='userStats'>
                        <h1 className='userName'>{stockName}</h1>
                        <br/><br/>
                        <br/>   
                        {info.length !== 0 ? getStockInfoView(info, handleClickUser) : <></>}
                    </div>
                    <div className="userGraph">
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Stocks

const getStockInfoView = (info: Comment[][], handleClickUser: any) => {
    return (
        <div className='scrollableLog'>
                            <h3>Comments in the past 7 days:</h3>
                        <>
                        {
                            info.map((value: any[], index: number) => (
                                <div className='entry' key={index}>
                                    <br/>
                                    <h3 className='score'>{value[0].date}</h3>
                                    <>
                                    {
                                        value.map((value: any, index: number) => (
                                            <div className="entry" key={index}>
                                                {value.comment_value ? <span style={{"color": "green"}}>POSITIVE</span> : <span style={{"color": "red"}}>NEGATIVE</span>}
                                                <span> by </span>
                                                <span style={{cursor: "pointer", color: "blue", textDecoration: "underline"}} className='name text-dark' onClick={() => handleClickUser(value.user_id)}>{value.user_id}</span>
                                            </div>
                                        ))
                                    }
                                    </>
                                </div>
                            ))
                        }
                        </>
                        </div>
    );
}