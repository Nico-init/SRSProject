import React, { useState } from 'react';
import './App.css';
import './Components/comp-styles/Leaderboards-style.css'
import LeftBar from './Components/LeftBar';
import Leaderboard from './Components/Leaderboard';
import Users from './Components/Users';
import { DB } from "./Components/test-database";


function App() {

  const [collapsed, setCollapsed] = useState(true);
  const [toggled, setToggled] = useState(true);
  const [activeMainPanel, setActiveMainPanel] = useState("Leaderboards")

  const handleClickPanelChange = (panel: string) => {
    setActiveMainPanel(panel);
  }

  const getActivePanel = (panel: string) => {
    switch (panel) {
      case "Leaderboards": return <Leaderboard DB={DB} handleClickPanelChange={handleClickPanelChange}></Leaderboard>
      case "Stocks": return <div>Stocks</div>
      case "Users": return <Users DB={DB}></Users>
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
