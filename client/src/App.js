import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import CreateProject from "./manager/pages/project/create";
import AllProjects from "./manager/pages/project/all";
import EditProject from "./manager/pages/project/edit"
import Annotator from "./annotator/page";
import "./App.scss";

function App() {
	return (
		<div className="App">
			<Router>
				<Switch>
					<Route path="/projects">
						<AllProjects></AllProjects>
					</Route>
					<Route path="/annotate/:uid" component={Annotator}/>
					<Route path="/project/:uid" component={EditProject}/>
					<Route path="/">
						<CreateProject></CreateProject>
					</Route>
				</Switch>
				
			</Router>
		</div>
	);
}

export default App;
