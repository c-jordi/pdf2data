import React from "react";
import Container from "../../../components/views/Container"
import Sidebar from "../../../parts/Sidebar"
import Header from "./Header"
import Search from "./Search"
import Catalog from "./Catalog"

import "./style.scss"

const AllProjects = () => {
    return <React.Fragment>
        <Sidebar></Sidebar>
        <Container>
            <Header></Header>
            <Search></Search>
            <Catalog></Catalog>
        </Container>
    </React.Fragment> 

}

export default AllProjects;