import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import CreateProject from "./pages/project/create";
import Annotate from "./pages/project/annotate"
import AllProjects from "./pages/project/all";
import "./App.scss";

function App() {
	return (
		<div className="App">
			<Router>
				<Switch>
					<Route path="/projects">
						<AllProjects></AllProjects>
					</Route>
					<Route path="/annotate">
						<Annotate></Annotate>
					</Route>
					<Route path="/">
						<CreateProject></CreateProject>
					</Route>
				</Switch>
				
			</Router>
		</div>
	);
}

export default App;
