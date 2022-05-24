import React, { useEffect } from 'react'
import './comp-styles/Users-style.css'
import './comp-styles/bulma-input.scss'
import { useState } from 'react'

type Props = {
    DB: any
    user: string
}

function Users(props: Props) {

    const [text, setText] = useState("");

    const userCheck = () => {
        if(props.user) {
            setText(props.user);
        }
    }

    useEffect(userCheck, );

    const handleSearch = (e: any) => {
        if(e.key === "Enter") {
            setText(e.target.value);
        }
    }

    const getUserInfo = (text: string) => {
        for (const u_info of props.DB) {
            if(u_info.name === text) {
                return <div>{u_info.name} | {u_info.w_score} | {u_info.at_score}</div>;
            }
        }
        return <div>No User Found</div>;
    }

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
                    getUserInfo(text)
                }
            </div>
        </div>
    )
}

export default Users