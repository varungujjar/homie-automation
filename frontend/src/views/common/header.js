import React from "react";

export const Header = (props) => {
    return (
        <div className="header mb-4">
            <div className="wrapper">
            <div className="float-left">
                <h1><i className={`fal fa-${props.icon}`}></i> {props.name}</h1>
            </div>
            <div className="float-right text-right">
            </div>
            <div className="clearfix"></div>
            </div>
        </div>
    )
}
