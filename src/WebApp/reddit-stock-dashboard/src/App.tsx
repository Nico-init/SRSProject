import React, { useState } from 'react';
import './App.css';
import './Components/comp-styles/Leaderboards-style.css'
import LeftBar from './Components/LeftBar';
import Leaderboard from './Components/Leaderboard';
import Users from './Components/Users';
import Stocks from './Components/Stocks';


function App() {

  const [collapsed, setCollapsed] = useState(true);
  const [toggled, setToggled] = useState(true);
  const [activeMainPanel, setActiveMainPanel] = useState("Leaderboards")
  const [addedSearchUser, setAddedSearchUser] = useState("")
  const [addedSearchStock, setAddedSearchStock] = useState("")

  const handleClickPanelChange = (panel: string, search: string) => {
    if(search && panel === "Users") {
      setAddedSearchUser(search);
    }
    else if (search && panel === "Stocks") {
      setAddedSearchStock(search)
    }
    setActiveMainPanel(panel);
  }

  const getActivePanel = (panel: string) => {
    switch (panel) {
      case "Leaderboards": return <Leaderboard handleClickPanelChange={handleClickPanelChange}></Leaderboard>
      case "Stocks": return <Stocks stock_symbol={addedSearchStock} handleClickPanelChange={handleClickPanelChange}></Stocks>
      case "Users": return <Users user={addedSearchUser} handleClickPanelChange={handleClickPanelChange}></Users>
      case "Settings": return  <div>Settings</div>
    }
  }

  const handleToggleSidebar = (value: boolean | ((prevState: boolean) => boolean)) => {
    setToggled(value);
  };

  return (
    <div className="App" onClick={() => handleToggleSidebar(true)}>
      <div className='SideBar'
        onMouseEnter={() => setCollapsed(!collapsed)} 
        onMouseLeave={() => setCollapsed(!collapsed)} >
      <LeftBar
        collapsed={collapsed}
        toggled={toggled}
        handleToggleSidebar={handleToggleSidebar}
        handleClickMenuIcon={handleClickPanelChange}
      ></LeftBar>
      </div>
      <div className='Main'>
        {
          getActivePanel(activeMainPanel)
        }
      </div>
    </div>
  );
}

export default App;
