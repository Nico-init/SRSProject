import React, { useEffect, useState } from 'react'

type Props = {
    stock_symbol: string
}

function Stocks(props: Props) {

    const [text, setText] = useState("");

    const stockCheck = () => {
        if(props.stock_symbol) {
            setText(props.stock_symbol);
        }
    }

    useEffect(stockCheck, );

    const handleSearch = (e: any) => {
        if(e.key === "Enter") {
            setText(e.target.value);
        }
    }

    /*const getStockInfo = (text: string) => {
        for (const u_info of props.DB) {
            if(u_info.name === text) {
                return <div>{u_info.name} | {u_info.w_score} | {u_info.at_score}</div>;
            }
        }
        return <div>No User Found</div>;
    }*/

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
                    text
                }
            </div>
        </div>
  )
}

export default Stocks