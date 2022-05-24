import React from "react";

type Props = {
    DB: any,
    isWeekly: boolean,
    handleClickPanelChange: any
}

function Profiles(props: Props) {
    return (
        <div id="profile">  
            {Items(props.DB, props.isWeekly, props.handleClickPanelChange)}
        </div>
    )
}

export default Profiles

function Items(data: any, isWeekly: boolean, handleClickPanelChange: any) {

    const handleClickProfile = (e: string) => {
        console.log(e);
        handleClickPanelChange("Users", e);
    }

    return (

        <>
            {
                data.map((value: any, index: number) => (
                    <div className="entry" key={index}>
                        <div className="flex" key={index}>
                            <div className="item">            
                                <div className="info">
                                    <span className="name text-dark">{index+1}.&emsp;</span>
                                    <span style={{cursor: "pointer", color: "blue", textDecoration: "underline"}} className='name text-dark' onClick={() => handleClickProfile(value.name)}>{value.name}</span>   
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