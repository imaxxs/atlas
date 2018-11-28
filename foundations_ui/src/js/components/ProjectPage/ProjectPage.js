import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Toolbar from '../common/Toolbar';
import ProjectActions from '../../actions/ProjectActions';
import ProjectHeader from './ProjectHeader';
import Loading from '../common/Loading';

class ProjectPage extends Component {
  constructor(props) {
    super(props);
    this.getAllProjects = this.getAllProjects.bind(this);
    this.state = {
      isLoaded: false,
      projects: this.props.projects,
      isMount: false,
      selectProject: this.props.selectProject,
    };
  }

  async componentDidMount() {
    await this.setState({ isMount: true });
    this.getAllProjects();
  }

  componentWillUnmount() {
    this.setState({ isMount: false });
  }

  async getAllProjects() {
    const apiProjects = await ProjectActions.getProjects();
    // use is mount for async as when it returns may have been unmounted
    const { isMount } = this.state;
    if (isMount) {
      if (apiProjects != null) {
        this.setState({ projects: apiProjects, isLoaded: true });
      } else {
        this.setState({ projects: [], isLoaded: true });
      }
    }
  }

  render() {
    const { isLoaded, projects, selectProject } = this.state;
    let projectList;
    if (isLoaded) {
      if (projects.length === 0) {
        projectList = <p>No projects available</p>;
      } else {
        projectList = ProjectActions.getAllProjects(projects, selectProject);
      }
    } else {
      projectList = <Loading loadingMessage="We are currently loading your projects" />;
    }

    return (
      <div className="project-page-container">
        <div className="header">
          <Toolbar />
          <ProjectHeader numProjects={projects.length} />
        </div>
        <div className="projects-body-container">
          {projectList}
        </div>
      </div>
    );
  }
}

ProjectPage.propTypes = {
  isMount: PropTypes.bool,
  isLoaded: PropTypes.bool,
  projects: PropTypes.array,
  selectProject: PropTypes.func,
};

ProjectPage.defaultProps = {
  isMount: false,
  isLoaded: false,
  projects: [],
  selectProject: () => null,
};

export default ProjectPage;
