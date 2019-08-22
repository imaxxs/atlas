import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Header from './Header';
import ProjectOverview from './ProjectOverview';
import JobDetails from './JobDetails';
import CommonHeader from '../common/CommonHeader';

class JobOverviewPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      tab: 'details',
    };

    this.onClickProjectOverview = this.onClickProjectOverview.bind(this);
    this.onClickJobDetails = this.onClickJobDetails.bind(this);
    this.onKeyDown = this.onKeyDown.bind(this);
  }

  onClickProjectOverview() {
    this.setState({
      tab: 'overview',
    });
  }

  onClickJobDetails() {
    this.setState({
      tab: 'details',
    });
  }

  onKeyDown() {}

  render() {
    const { tab } = this.state;

    return (
      <div>
        <CommonHeader {...this.props} />
        <div className="job-overview-container">
          <Header {...this.props} />
          <div className="job-overview-tabs-tags-container">
            <div>
              <h3
                className={tab === 'overview' ? 'active' : ''}
                onClick={this.onClickProjectOverview}
                onKeyDown={this.onKeyDown}
              >
                Project Overview
              </h3>
              <h3
                className={tab === 'details' ? 'active' : ''}
                onClick={this.onClickJobDetails}
                onKeyDown={this.onKeyDown}
              >
                Job Details
              </h3>
            </div>
            <div className="project-summary-tags-container">
              <p>tags</p>
              <span>finance</span>
              <span>marketing</span>
            </div>
          </div>
          {tab === 'overview' && <ProjectOverview {...this.props} />}
          {tab === 'details' && <JobDetails {...this.props} />}
        </div>
      </div>
    );
  }
}

JobOverviewPage.propTypes = {
  history: PropTypes.object,

};

JobOverviewPage.defaultProps = {
  history: {},
};

export default JobOverviewPage;
