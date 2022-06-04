import React, { useEffect, useState } from 'react'
import { User } from './Users'
import ReactApexChart from 'react-apexcharts'
import {defaultOptions} from './comp-styles/ChartOptions'
import {ApexOptions} from 'apexcharts'
import StarRating from './StarRating'

type Props = {
    userInfo: User
    handleClickPanelChange: any
}

function UserInfo(props: Props) {
  const [chartOptionsW, setChartOptionsW] = useState(defaultOptions);
  const [chartOptionsT, setChartOptionsT] = useState(defaultOptions);
  const [chartSeriesW, setChartSeriesW] = useState([{x: new Date().getTime(), y: 0}]);
  const [chartSeriesT, setChartSeriesT] = useState([{x: new Date().getTime(), y: 0}]);
  const [reliability, setReliability] = useState(0.0);

  const newOptions = (color: string, performance: number[], dataLabels: boolean, title: string, smooth: boolean) => {
    var op: ApexOptions = {
      chart: {
        type: 'line',
        zoom: {
          enabled: false
        }
      },
      title: {
        text: title
      },
      stroke: {
        curve: smooth ? 'smooth' : 'straight'
      },
      colors: [color],
      yaxis: {
        title: {
          text: 'Score'
        },
        min: 0,
        max: Math.max(...performance)+0.25*Math.max(...performance),
        tickAmount: 6
      },
      grid: {
        borderColor: '#e7e7e7',
        row: {
          colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
          opacity: 0.5
        },
      },
      markers: {
        size: 0
      },
      dataLabels: {
        enabled: dataLabels
      },
      xaxis: {
        type: 'datetime'
      }
    }
    return op;
  }

  const updateOptions = () => {
    if(props.userInfo.name !== "None") {
      setChartSeriesW(props.userInfo.weekly_performance);
      setChartOptionsW(newOptions("#6495ED", props.userInfo.weekly_performance.map(({y}) => y), true, "User performance for current week", false));
      setChartSeriesT(props.userInfo.all_time_performance);
      setChartOptionsT(newOptions("#50C878", props.userInfo.all_time_performance.map(({y}) => y), false, "Total user performance", true));
    }
    else {
      setChartSeriesW([{x: 0, y: 0}]);
      setChartOptionsW(defaultOptions);
      setChartSeriesT([{x: 0, y: 0}]);
      setChartOptionsT(defaultOptions);
    }

    let r: any[] = [];
    props.userInfo.stocks.forEach(s => {
      r.push(s.reliability)
    });
    setReliability(Math.round((r.reduce((a,b) => a+b, 0) / r.length)*10) || 0)
  }

  const handleClickStock = (stock_name: string) => {
    props.handleClickPanelChange("Stocks", stock_name);
  }

  useEffect(updateOptions, [props.userInfo]);

  return (
    <div className='userBox'>
        <div className='userStats'>
          <h2 className='userName'>{props.userInfo.name}</h2>
          <StarRating num_stars={reliability}></StarRating>
          <h3 className='score'>Weekly Score: {props.userInfo.weekly_score >= 0 ? "+" : ""}{props.userInfo.weekly_score}%</h3>
          <h3 className='score'>All Time Score: {props.userInfo.total_score >= 0 ? "+" : ""}{props.userInfo.total_score}%</h3>
          <h3 className='score'>Comments in the past 7 days:</h3>
          <div className='scrollableLogUsers'>
            {
              props.userInfo.stocks.map((value: any, index: number) => (
                <div className='commentEntry' key={index}>
                <span>{new Date(value.date*1000).toLocaleDateString()}:&emsp;</span>
                {value.comment_value ? <span style={{"color": "green"}}>POSITIVE</span> : <span style={{"color": "red"}}>NEGATIVE</span>}
                <span> for </span>
                <span style={{cursor: "pointer", color: "blue", textDecoration: "underline"}} className='name text-dark' onClick={() => handleClickStock(value.stock_name)}>{value.stock_name}</span>
                </div>

              ))
            }
          </div>
        </div>
        <div className="userGraph">
          <div className="weeklyGraph">
            <ReactApexChart options={chartOptionsW} series={[{name: 'Score',data: chartSeriesW}]} type="line" height={200}/>
          </div>
          <div className="totalGraph">
            <ReactApexChart options={chartOptionsT} series={[{name: 'Score',data: chartSeriesT}]} type="line" height={200}/>
          </div>
        </div>
    </div>
  )
}

export default UserInfo