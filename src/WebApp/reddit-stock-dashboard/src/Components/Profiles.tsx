import React from "react";

type Props = {
    DB: any,
    isWeekly: boolean
}

function Profiles(props: Props) {
    return (
        <div id="profile">  
            {Items(props.DB, props.isWeekly)}
        </div>
    )
}

export default Profiles

function Items(data: any, isWeekly: boolean) {
    return (

        <>
            {
                data.map((value: any, index: any) => (
                    <div className="entry">
                        <div className="flex" key={index}>
                            <div className="item">            
                                <div className="info">
                                    <span className='name text-dark'>{value.name}</span>   
                                </div>                 
                            </div>
                            <div className="item">
                                {isWeekly ? <span>{value.w_score}</span> : <span>{value.at_score}</span>} 
                            </div>
                        </div>
                        <hr className="rounded"></hr>
                    </div>
                ))
            }
        </>

        
    )
}