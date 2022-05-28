import React, { useEffect, useState } from 'react'
import { User } from './Users'
import ReactApexChart from 'react-apexcharts'
import {defaultOptions} from './comp-styles/LineChartOptions'

type Props = {
    userInfo: User
}

function UserInfo(props: Props) {

  const [chartType, setChartType] = useState("weekly");
  const [chartOptions, setChartOptions] = useState(defaultOptions)
  const [chartSeries, setChartSeries] = useState([{data: [0]}])

  const updateOptions = () => {
    let tempOptions = defaultOptions
    if(props.userInfo.name !== "None") {
      tempOptions.yaxis = {
        title: {
          text: 'Score'
        },
        max: Math.max(...props.userInfo.weekly_performance)
      };
      setChartOptions(tempOptions);
      setChartSeries([{data: props.userInfo.weekly_performance}])
    }
    else {
      setChartSeries([{data: [0]}])
      setChartOptions(defaultOptions)
    }
  }

  useEffect(updateOptions, [props.userInfo]);

  return (
    <div className='userBox'>
        <h2 className='userName'>{props.userInfo.name}</h2>
        <br/><br/>
        <div className='userStats'>
            <h3 className='score'>Weekly Score: {props.userInfo.w_score}</h3>
            <h3 className='score'>All Time Score: {props.userInfo.at_score}</h3>
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