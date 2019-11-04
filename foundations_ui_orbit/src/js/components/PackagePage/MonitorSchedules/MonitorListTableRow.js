import React, { Component } from "react";
import PropTypes from "prop-types";
import CommonActions from "../../../actions/CommonActions";


class MonitorListTableRow extends Component {
  constructor(props) {
    super(props);
    this.onClick = this.onClick.bind(this);
    this.isSelectedRow = this.isSelectedRow.bind(this);
  }

  onClick() {
    const { onClick, monitorName } = this.props;

    onClick(monitorName);
  }

  isSelectedRow() {
    const { selectedRow, monitorName } = this.props;
    return monitorName === selectedRow;
  }

  render() {
    const {
      monitorName,
      status,
      user
    } = this.props;

    const selectedClass = this.isSelectedRow() ? "selected-row" : "";

    function addStatus(rowStatus) {
      if (rowStatus === "paused") {
        return <div className="status-icon status-paused-orange" />;
      }

      if (rowStatus === "active") {
        return <div className="status-icon status-green" />;
      }
    }

    const statusIcon = addStatus(status);

    return (
      <div className={`monitor-table-row ${selectedClass}`} onClick={this.onClick}>
        <div className="monitor-table-cell">{monitorName}</div>
        <div className="monitor-user-table-cell">{user}</div>
        <div className="monitor-status-table-cell">{statusIcon}</div>
      </div>
    );
  }
}

MonitorListTableRow.propTypes = {
  monitorName: PropTypes.string,
  status: PropTypes.string,
  user: PropTypes.string,
  onClick: PropTypes.func,
  selectedRow: PropTypes.string
};

MonitorListTableRow.defaultProps = {
  monitorName: "Invalid monitor name",
  status: "Invalid contract name",
  user: "",
  onClick: () => {},
  selectedRow: ""
};


export default MonitorListTableRow;
