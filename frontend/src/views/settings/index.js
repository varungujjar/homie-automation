import React, { Component } from "react";
import { Formik } from 'formik';
import { Header } from "../common/header";
import { System } from "./system";
import { Components } from "./components";
import { Rooms } from "./rooms";
import { Devices } from "./devices";
import PropTypes from 'prop-types'
import SelectTimezone, { getTimezoneProps } from 'react-select-timezone'



export const TabHeads = (props) => {
    const tabs = {"Components":"fa-box-open","Rooms":"fa-person-booth","Devices":"fa-toggle-off","Network":"fa-network-wired","System":"fa-cog"};
    return(
             <ul className="nav nav-tabs" id="myTab" role="tablist">
                        {
                            Object.keys(tabs).map((key,index)=>{
                                return(
                                    <li className="nav-item" key={index}>
                                        <a className={`nav-link ${props.disabled ? "disabled" : null} ${key==props.active ? "active" : null} `} id={`${key}-tab`} data-toggle="tab" href={`#${key}`} role="tab" aria-controls={`${key}`} aria-selected="true"><i className={`fal ${Object.values(tabs)[index]}`}></i> {key}</a>
                                    </li>
                                )
                            })
                        }
                </ul>
    )
}


export const Settings = (props) => {
        return (
            <>   
                <Header name={props.name} icon={props.icon}></Header>
                <TabHeads active="Components" />
                <div className="tab-content" id="myTabContent">
                    <Components active="1"/>
                    <Rooms/>
                    <Devices/>
                    <System/>
                </div>
            </>
           )
}

