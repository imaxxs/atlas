import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ProjectPage from './ProjectPage/ProjectPage';
import JobListPage from './JobListPage/JobListPage';
import ProjectActions from '../actions/ProjectActions';

class App extends Component {
  constructor(props) {
    super(props);
    this.changePage = this.changePage.bind(this);
    this.selectProject = this.selectProject.bind(this);
    this.state = {
      page: '',
      selectedProject: {},
      jobs: [],
      projects: [],
    };
  }

  changePage(newPage) {
    this.setState({ page: newPage });
  }

  selectProject(project) {
    const projectJobs = ProjectActions.getJobsForProject(project.name);
    this.setState({ selectedProject: project, jobs: projectJobs, page: 'jobList' });
  }

  render() {
    const {
      page, selectedProject, jobs, projects,
    } = this.state;

    let curPage = <ProjectPage selectProject={this.selectProject} projects={projects} />;

    if (page === 'jobList') {
      curPage = <JobListPage project={selectedProject} projectName={selectedProject.name} jobs={jobs} />;
    }

    return (
      <div className="App">
        {curPage}
      </div>
    );
  }
}

App.propTypes = {
  selectedProject: PropTypes.object,
  page: PropTypes.string,
  jobs: PropTypes.array,
  projects: PropTypes.array,
};

App.defaultProps = {
  page: '',
  selectedProject: { name: 'local_deployment' },
  jobs: [],
  projects: [],
};

export default App;
