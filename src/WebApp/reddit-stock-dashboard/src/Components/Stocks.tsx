import React, { useEffect, useState } from 'react'
import { ClipLoader } from 'react-spinners'
import {Comment} from './SRS_types'

type Props = {
    stock_symbol: string
    handleClickPanelChange: any
}

function Stocks(props: Props) {
    const [stockName, setStockName] = useState("");
    const [info, setStockInfo] = useState([])
    const [loading, setLoading] = useState(false)

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
        setLoading(true);
        fetch("/stock/"+text).then(
            res => res.json()
        ).then(
            info => {
                console.log(info)
                if (info.length !== 0) {
                    console.log(info)
                    setStockInfo(info); 
                    setStockName(text);
                    setLoading(false)
                }
                else {
                    setStockInfo([]);
                    setStockName("The symbol doesn't exist or there are no commets yet...");
                    setLoading(false)
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
                        <input className="input is-small is-rounded" type="text" placeholder="stock-symbol" onKeyDown={handleSearch}>
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
                        {loading ? <ClipLoader css={"margin-top: 5%; margin-left: 7pc;"} color={'#000000'} loading={loading} size={50} ></ClipLoader> : info.length !== 0 ? getStockInfoView(info, handleClickUser) : <></>}
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
                                value[0] ? <div className='entry' key={index}>
                                        <br/>
                                        <h3 className='score'>{new Date(value[0].date*1000).toLocaleDateString()}</h3>
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
                                    </div> : <></>
                            ))
                        }
                        </>
                        </div>
    );
}