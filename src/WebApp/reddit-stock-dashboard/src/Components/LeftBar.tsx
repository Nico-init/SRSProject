import React from 'react'
import { ProSidebar, Menu, MenuItem, SidebarHeader, SidebarFooter, SidebarContent} from 'react-pro-sidebar';
import { Icons } from './Icons';
import 'react-pro-sidebar/dist/css/styles.css';


const LeftBar = ({collapsed, toggled, handleToggleSidebar, handleClickMenuIcon}: {collapsed: boolean, toggled: boolean, handleToggleSidebar: ((value: boolean) => void) | undefined, handleClickMenuIcon: ((value: string) => void)}) => { 
  return (
        <ProSidebar
            collapsed={collapsed} 
            toggled={toggled}
            breakPoint="md"
            onToggle={handleToggleSidebar} >
            
            <SidebarHeader>
            <div
            style={{
                padding: '24px',
                textTransform: 'uppercase',
                fontWeight: 'bold',
                fontSize: 14,
                letterSpacing: '1px',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
            }}
            >
            Reddit Stocks Dashboard
            </div>
            </SidebarHeader>
            
            <SidebarContent>
              <Menu iconShape='circle'>
              <MenuItem onClick={() => handleClickMenuIcon("Leaderboards")} icon={<Icons.LeaderboardsTabIcon isSelected={false}/>}>Leaderboards</MenuItem>
              <MenuItem onClick={() => handleClickMenuIcon("Stocks")} icon={<Icons.StocksTabIcon isSelected={false}/>}>Stocks</MenuItem>
              <MenuItem onClick={() => handleClickMenuIcon("Users")} icon={<Icons.UsersTabIcon isSelected={false}/>}>Users</MenuItem>
              </Menu>
            </SidebarContent>

            <SidebarFooter>
            <div>
              <Menu iconShape='circle'>
                <MenuItem onClick={() => handleClickMenuIcon("Settings")} icon={<Icons.SettingsTabIcon isSelected={false}/>}>Settings</MenuItem>
              </Menu>
            </div>
            </SidebarFooter>
        </ProSidebar>
  )
}

export default LeftBar;