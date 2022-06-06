import { newOptionsStockHistory, newOptionsBarChart } from './comp-styles/ChartOptions'
import React, { useEffect, useState } from 'react'
import ReactApexChart from 'react-apexcharts'
import { ClipLoader } from 'react-spinners'
import {Comment} from './SRS_types'
import './comp-styles/Stocks-style.css'

type Props = {
    stock_symbol: string
    handleClickPanelChange: any
}

function Stocks(props: Props) {
    const [stockName, setStockName] = useState("");
    const [info, setStockInfo] = useState([]);
    const [chartHistory, setChartHistory] = useState([]);
    const [loadingInfo, setLoadingInfo] = useState(false);
    const [loadingHistory, setLoadingHistory] = useState(false);

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
        setLoadingInfo(true);
        setLoadingHistory(true);
        fetch("/stock/"+text).then(
            res => res.json()
        ).then(
            info => {
                console.log(info)
                if (info.length !== 0) {
                    console.log(info)
                    setStockInfo(info); 
                    setStockName(text);
                    setLoadingInfo(false);
                }
                else {
                    setStockInfo([]);
                    setStockName("The symbol doesn't exist or there are no commets yet...");
                    setLoadingInfo(false);
                }
            }
        )

        fetch("/stock/"+text+"/history").then(
            res => res.json()
        ).then(
            history => {
                if (history.length !== 0) {
                    setChartHistory(history);
                    setLoadingHistory(false);
                }
                else {
                    setChartHistory([]);
                    setLoadingHistory(false);
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
                    <div className='userStats'>
                        <h1 className='userName'>{stockName}</h1>
                        {loadingInfo ? getLoadingSpinner(loadingInfo) : info.length !== 0 ? getStockInfoView(info, handleClickUser) : <></>}
                    </div>
                    <div className="userGraph">
                        <div className='barChart'>
                            {loadingInfo ? getLoadingSpinner(loadingInfo) : info.length !== 0 ? <ReactApexChart options={newOptionsBarChart()} series={[{name: "Bullish", data: [getAmountSentiment(info, true)]}, {name: "Bearish", data: [getAmountSentiment(info, false)]}]} type="bar" height={150}></ReactApexChart> : <></>}
                        </div>
                        <div className='stockChart'>
                            {loadingHistory ? getLoadingSpinner(loadingHistory) : chartHistory.length !== 0 ? <ReactApexChart options={newOptionsStockHistory('#EE4B2B', chartHistory.map(({y}) => y), "Adjusted Closed Price in the last Month")} series={[{name: 'Score',data: chartHistory}]} type="line" height={300}/> : <></>}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Stocks

const getStockInfoView = (info: Comment[][], handleClickUser: any) => {
    return (
        <div className='Log'>
                        <h3>Comments in the past days:</h3>
                        <div className='scrollableLog'>
                        {
                            info.map((value: any[], index_out: number) => (
                                value[0] ? <div className='entry' key={index_out}>
                                        <h3 className='score'>{new Date(value[0].date*1000).toLocaleDateString()}</h3>
                                        <>
                                        {
                                            value.map((value: any, index_in: number) => (
                                                <div className="entryRow" key={index_in}>
                                                    {value.comment_value ? <span style={{"color": "green"}}>BULLISH</span> : <span style={{"color": "red"}}>BEARISH</span>}
                                                    <span> by </span>
                                                    <span style={{cursor: "pointer", color: "blue", textDecoration: "underline"}} className='name text-dark' onClick={() => handleClickUser(value.user_id)}>{value.user_id}</span>
                                                </div>
                                            ))
                                        }
                                        </>
                                    </div> : <div key={index_out}></div>
                            ))
                        }
                        </div>
        </div>
    );
}

const getAmountSentiment = (info: Comment[][], sentiment: boolean) => {
    let amount = 0;
    info.forEach((value: any[]) => {
        if (value[0]) {
            value.forEach((value: any) => {
                if (sentiment === value.comment_value) {amount += 1}
            })
        }
    })
    return amount;
}

const getLoadingSpinner = (loading: boolean) => {
    return (
        <ClipLoader css={"margin-top: 5%; margin-left: 7pc;"} color={'#000000'} loading={loading} size={50} ></ClipLoader>
    );
}