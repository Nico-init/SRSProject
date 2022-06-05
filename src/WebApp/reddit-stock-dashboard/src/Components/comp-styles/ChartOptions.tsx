import { ApexOptions } from 'apexcharts'

export const defaultOptions: ApexOptions = {
  chart: {
    type: 'line',
    zoom: {
      enabled: false
    }
  },
  yaxis: {
    title: {
      text: 'Score'
    }
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
  },
  xaxis: {
    type: 'datetime'
  }
};

export const newOptionsStockHistory = (color: string, performance: number[], title: string) => {
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
      curve: 'smooth'
    },
    colors: [color],
    yaxis: {
      title: {
        text: 'Adj Closed Price'
      },
      min: 0,
      max: Math.max(...performance)*1.75,
      tickAmount: 10
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
      enabled: false
    },
    xaxis: {
      type: 'datetime'
    }
  }
  return op;
}

export const newOptionsBarChart = () => {
  var op: ApexOptions = {
    chart: {
      type: 'bar',
      height: 200,
      stacked: true,
      stackType: '100%'
    },
    plotOptions: {
      bar: {
        horizontal: true,
      },
    },
    stroke: {
      width: 1,
      colors: ['#fff']
    },
    title: {
      text: 'Bullish/Bearish mentions in the past 7 days'
    },
    xaxis: {
      labels: {
        show: false
      }
    },
    yaxis: {
      labels: {
        show: false
      }
    },
    tooltip: {
      y: {
        formatter: function (val) {
          return val + "K"
        }
      }
    },
    fill: {
      opacity: 1
    
    },
    legend: {
      position: 'top',
      horizontalAlign: 'left',
      offsetX: 40
    }
    };
  return op;
}


