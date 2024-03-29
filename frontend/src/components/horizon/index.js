import React, {Component} from "react";
import { socket } from "../../system/socketio";
import { DeviceModal } from "../../views/common/devicemodal";


export class ModuleList extends Component {
    constructor(props) {
        super(props);
        this._isMounted = false;
        this.defaultIfAndProperties = {"type": "component", "condition": "=", "id": this.props.data.id, "properties": {'astral':{"above_horizon":this.props.data.properties.astral.above_horizon}}};
        if(this.props.values){
            this.deviceValues = this.props.values;
        }
        this.state = {
            edit:false
        }   
        this.deviceData = this.props.data;
        if(this.deviceValues){
            this.state = {
                selectedProperty:this.deviceValues.properties.astral.above_horizon ? this.deviceValues.properties.astral.above_horizon : this.deviceData.properties.astral.above_horizon,
            }
        }
    }

    componentDidMount() {
        this._isMounted = true;
        if (this._isMounted) {
        }
    }    

    onSelectProperty = (selectedProperty) => {
        this.setState({
            selectedProperty: selectedProperty.currentTarget.value
        })
        this.deviceData.properties.astral.above_horizon = selectedProperty.currentTarget.value
        this.deviceValues.properties.astral.above_horizon = selectedProperty.currentTarget.value;
        this.props.setFieldValue(this.deviceValues.properties.astral.above_horizon)
    } 

    
    componentWillUnmount() {
        this._isMounted = false;
    }


    render(){
        return (
            <div>
                <div className={`card card-outline-default ${this.deviceValues && !this.state.edit ? "has-edit-hover" : ""}`}>
                    <div className="edit-overlay v-center" onClick={() => this.setState({ edit: true })}>
                        <span className="text-lg icon-1x icon-edit"></span>
                    </div>
                    {
                        
                            <div className="p-all-less">
                                <span className={`icon-1x icon-left ${this.deviceData.properties.astral.above_horizon == "true" ? "icon-bg-warning icon-sunrise " : "icon-bg-dark icon-moon"}`}></span>
                                <div className="text-bold">{this.deviceData.properties.astral.above_horizon == "true" ? ("Sun Above Horizon") : ("Sun Below Horizon")}</div>
                                <div className="text-secondary">
                                    {this.deviceData.properties.astral.above_horizon == "true" ? ("On Sunrise") : ("On Sunset")}
                                </div>
                            </div>
                    }
                    {
                        this.deviceValues && this.state.edit &&
                        (() => {
                            if (this.props.dataType == "if" || this.props.dataType == "and") {
                                return (
                                    <>
                                        <div className="p-all-less">
                                            <select name="" value={this.state.selectedProperty} onChange={this.onSelectProperty} className="form-control">
                                                <option value="false">On Sunset</option>
                                                <option value="true">On Sunrise</option>
                                            </select>
                                        </div>
                                        <div className="card-footer bg-dark text-center b-t"><span className="link" onClick={() => this.setState({ edit: false })}>Done</span></div>
                                    </>
                                )
                            }
                        })()
                    }
                    {
                        this.props.addDefaultProperties && (this.props.dataType == "if" || this.props.dataType == "and") && (
                            <button type="button" className="text-lg icon-bg-light icon-shadow icon-1x icon-add float-right" variant="primary" onClick={() => { this.props.addDefaultProperties(this.defaultIfAndProperties) }}></button>
                        )
                    }
                    {
                        this.deviceValues && !this.state.edit && (
                            <button type="button" className="text-lg icon-bg-light icon-shadow icon-1x icon-remove float-right" variant="primary" onClick={() => { this.props.deleteDefaultProperties(this.props.indexMap, this.props.dataType) }}></button>
                        )
                    }
                </div>
            </div>
        )
    }
}


export const ModuleModal = (props) => {
    return(
        <div>
             {JSON.stringify(props.data)}
        </div>
    )
}


export const Module = (props) => {
    const device = props.data;
    return (
        <div className="slider-slide">
            <div className={`card card-module-height card-shadow item ${device.online ? "" : "offline"}`}>
                <div className="offline-icon text-danger"></div>
                <div className="card-body">
                        <DeviceModal data={device}/> 
                        <span className={`icon-1x icon-bg-default ${device.properties.astral.above_horizon == "true" ? "icon-sunrise icon-bg-warning " : "icon-moon"}`}></span>
                        <div className="text-status ">{device.properties.astral.above_horizon == "true" ? ("Above Horizon") : ("Below Horizon")}</div>
                        <div className="text-secondary title-case mt-2">{device.properties.astral.next_astral} in {device.properties.astral.next_time.number} {device.properties.astral.next_time.unit}</div>
                        <div className="clearfix"></div>
                
                </div>
            </div>
        </div>
    )
}



export class Horizon extends Component {
    constructor(props) {
        super(props);
        this._isMounted = false;
        this.state = {
            deviceId:0,
            aboveHorizon: null,
            astralTimeDigit: 0,
            astralTimeDigitUnit: null,
            astralNext: null,
            dataLoaded: false
        }
    }



    componentDidMount() {
        this._isMounted = true;
        if (this._isMounted) {  
        fetch("/api/components/horizon")
            .then(response => response.json())
            .then((result) => {
                    this.setState({
                        deviceId:result.id,
                        aboveHorizon: result.properties.astral.above_horizon,
                        astralTimeDigit: result.properties.astral.next_time.number,
                        astralTimeDigitUnit: result.properties.astral.next_time.unit,
                        astralNext: result.properties.astral.next_astral,
                        dataLoaded: true
                    });
                   
                socket.on(this.state.deviceId, data => {
                    // console.log(data);
                    if (this._isMounted) {
                        this.setState({
                            aboveHorizon: data.properties.astral.above_horizon,
                            astralTimeDigit: data.properties.astral.next_time.number,
                            astralTimeDigitUnit: data.properties.astral.next_time.unit,
                            astralNext: data.properties.astral.next_astral,
                            dataLoaded: true
                        });
                    }
                }); 
               
            })
            .catch((error) => {
                console.error(error)
            })
        }      
    }


    componentWillUnmount() {
        this._isMounted = false;
    }


    render() {
        let data = this.state;
        if (data.dataLoaded == true) {
            return (
                        <>
                        <span className={`icon-3x text-info icon-left ${this.state.aboveHorizon == "true" ? "icon-sunrise " : "icon-moon"}`}></span>
                        <div className="clearfix"></div>
                        <h2 className="mt-1 text-white">{this.state.aboveHorizon == "true" ? ("Above Horizon") : ("Below Horizon")}</h2>
                        <span className="text-secondary">  {this.state.astralNext.charAt(0).toUpperCase() + this.state.astralNext.slice(1)} in Next {this.state.astralTimeDigit} {this.state.astralTimeDigitUnit}</span>
                       
                        </>
            )
        }
        return (null)
    }
}