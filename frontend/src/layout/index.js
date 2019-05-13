import React from "react";
import { SideNav, MobileNav } from "./common/nav";
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom';

import { Dashboard } from "./dashboard";
import { Automation } from "./rules";
import { Settings } from "./settings";
import { Horizon } from "../components/horizon";
import { Weather } from "../components/weather";
import { Home } from "../components/home";

function NoMatch({ location }) {
  return (
    <div>
      <h3>
        No match for <code>{location.pathname}</code>
      </h3>
    </div>
  );
}


export const Layout = () => {
  return (
    <>
    <Router>
        <div className="layout-sidenav">
          <SideNav></SideNav>
        </div>
        <div className="layout-highlight">
                        <Home></Home>
                        <Weather></Weather>
                        <Horizon></Horizon>
        </div>
        <div className="layout-body">
        <div className="wrapper">
        <Switch>
            <Route exact path="/" component={()=><Dashboard name={"Dashboard"} icon="home"/>} />
            <Route path="/rules" component={()=> <Automation name={"Rules"} icon="list-alt"/>} />
            <Route path="/settings" component={()=> <Settings name={"Settings"} icon="cog"/>} />
            <Route component={NoMatch} />
          </Switch>
          </div>
          </div>

        <MobileNav></MobileNav>
       
      </Router>
    </>
  )

}
