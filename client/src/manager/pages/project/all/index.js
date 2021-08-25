import React from "react";
import Container from "../../../components/views/Container"
import Sidebar from "../../../parts/Sidebar"
import Search from "../../../parts/Search";
import {SimpleButton} from "../../../components/inputs";
import { BiImport } from "react-icons/bi";
import "./style.scss"

const AllProjects = () => {
    return <React.Fragment>
        <Sidebar></Sidebar>
        <Container>
            <div className="projects-header">
                <h2>Projects</h2>
                <SimpleButton> <BiImport/> Import</SimpleButton>
            </div>
            <Search></Search>
        </Container>
    </React.Fragment> 

}

export default AllProjects;