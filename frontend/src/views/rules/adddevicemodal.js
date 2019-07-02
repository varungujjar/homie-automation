import React, { Component } from "react";
import Modal from 'react-bootstrap/Modal'
import { GetDevice } from "../dashboard/devices";

export class AddDeviceModal extends Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.handleShow = this.handleShow.bind(this);
    this.handleHide = this.handleHide.bind(this);
    this.state = {
      show:false,
      dataLoaded: true,
    };
  }


  getDeviceData = (props) => {
    GetDevice(props.data.id, data => {
      import(`../../components/${data.component}/${data.type}`)
        .then(component => {
          if (this._isMounted) {
            this.setState({
              modalDeviceRender: component.ModuleModal,
              modalDeviceData: data,
              dataLoaded: true,
            })
          }
        }
        ).catch(error => {
          // console.error(`"${this.props.data.component} ${this.props.data.type}" not yet supported`);
        });
    })
  }
  


  componentDidMount() {
    this._isMounted = true;
    if (this._isMounted) {
      // this.getDeviceData(this.props)
    }
  }


  componentWillUnmount() {
    this._isMounted = false;
  }

  handleShow() {
    this._isMounted = true;
    this.setState({ show: true });
    this.getDeviceData(this.props)
  }

  handleHide = () => {
    this.setState({ show: false });
    this._isMounted = false;
  };

  render() {
    const ModalBody = this.state.modalDeviceRender;
    let deviceData = this.state.modalDeviceData;

    return (
      this.state.dataLoaded == true &&
      <>
        <button variant="primary" onClick={this.handleShow} className="show-device-props">
          <img src="assets/light/images/dots.svg" />
        </button>
        <Modal
          show={this.state.show}
          onHide={this.handleHide}
          size="lg"
          aria-labelledby="contained-modal-title-vcenter"
          centered
        >
          <Modal.Header closeButton>
            <h2 className="text-bold">Devices List</h2>
          </Modal.Header>
          <Modal.Body>
            
            All your devices list here
          </Modal.Body>
        </Modal>
      </>
    )
  }
}
