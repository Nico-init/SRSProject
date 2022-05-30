import React, { useEffect, useState } from 'react'
import { User } from './Users'
import ReactApexChart from 'react-apexcharts'
import {defaultOptions} from './comp-styles/LineChartOptions'
import {ApexOptions} from 'apexcharts'

type Props = {
    userInfo: User
}

function UserInfo(props: Props) {

  //const [chartType, setChartType] = useState("weekly");ul
  const [chartOptions, setChartOptions] = useState(defaultOptions)
  const [chartSeries, setChartSeries] = useState([{data: [0]}])

  const newOptions = (performance: number[]) => {
    var op: ApexOptions = {
      chart: {
        type: 'line',
        zoom: {
          enabled: false
        }
      },
      yaxis: {
        title: {
          text: 'Score'
        },
        max: Math.max(...performance)
      },
      grid: {
        borderColor: '#e7e7e7',
        row: {
          colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
          opacity: 0.5
        },
      },
      markers: {
        size: 1
      },
      dataLabels: {
        enabled: true
      }
    }
    return op;
  }

  const updateOptions = () => {
    if(props.userInfo.name !== "None") {
      setChartSeries([{data: props.userInfo.weekly_performance}])
      setChartOptions(newOptions(props.userInfo.weekly_performance));
    }
    else {
      setChartSeries([{data: [0]}])
      setChartOptions(defaultOptions)
    }
  }

  useEffect(updateOptions, );

  return (
    <div className='userBox'>
        <h2 className='userName'>{props.userInfo.name}</h2>
        <br/><br/>
        <div className='userStats'>
            <h3 className='score'>Weekly Score: {props.userInfo.weekly_score}</h3>
            <h3 className='score'>All Time Score: {props.userInfo.total_score}</h3>
            <br/>
            Positive/negative stocks
        </div>
        <div className="userGraph">
          <h3 className='chartTitle'>Temp</h3>
          <ReactApexChart options={chartOptions} series={chartSeries} type="line" height={350}/>
        </div>
    </div>
  )
}

export default UserInfo